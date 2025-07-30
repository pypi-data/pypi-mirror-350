import asyncio
import json
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
from urllib.parse import urljoin

import requests
from hera.exceptions import NotFound, Unauthorized, exception_from_server_response
from hera.workflows import Parameter, Workflow, WorkflowsService
from hera.workflows.models import WorkflowStopRequest, WorkflowTemplateRef
from hera.workflows.service import valid_host_scheme
from pystac import Collection, Item

from eodc import settings

logger = logging.getLogger(__name__)


@dataclass
class FaasProcessorDetails:
    name: str
    workflow_template_name: str


class FaasProcessor(Enum):
    Force = FaasProcessorDetails("force", "faas-force")
    Sen2Like = FaasProcessorDetails("sen2like", "faas-sen2like")
    OpenEO = FaasProcessorDetails("openeo", "faas-openeo-executor")
    Snap = FaasProcessorDetails("snap", "faas-snap")
    custom = FaasProcessorDetails("custom", "")


LABEL_VALIDATION_REGEX = r"(([A-Za-z0-9][-A-Za-z0-9_.]*)?[A-Za-z0-9])?"


class FaasProcessorBase(ABC):
    @classmethod
    def get_instance(cls, processor_details, name=None):
        return cls(processor_details=processor_details)

    def __init__(self, processor_details: FaasProcessorDetails) -> None:
        # The URL for hera needs to end with a slash,
        # otherwise urlparse cuts the `/dev` part
        host = (
            settings.FAAS_URL + "/"
            if not settings.FAAS_URL.endswith("/")
            else settings.FAAS_URL
        )
        self.workflows_service = WorkflowsService(
            host=host,
            verify_ssl=False,
            namespace=settings.NAMESPACE,
            token=settings.ARGO_WORKFLOWS_TOKEN,
        )

        self.processor_details = processor_details

        try:
            self.workflows_service.get_info()
        except ConnectionError:
            raise Exception(
                f"Could not establish connection to argo workflows server "
                f"at {settings.FAAS_URL} in namespace {settings.NAMESPACE}"
            )

        try:
            self.workflows_service.list_workflows()
        except Unauthorized:
            raise Exception(
                f"Unauthorized to access content the argo workflows server "
                f"at {settings.FAAS_URL} in namespace {settings.NAMESPACE}"
            )

        if self.processor_details.name == "custom":
            logger.info(
                """Using the custom process only allows for Argo Workflows to
                        to be submitted directly. No ArgoWorkflow Templates will be
                        available."""
            )
        else:
            try:
                self.workflows_service.get_workflow_template(
                    processor_details.workflow_template_name,
                    namespace=settings.NAMESPACE,
                )
            except NotFound:
                raise Exception(
                    f"Could not initialise faas module {self.processor_details.name}"
                    f"as the workflow template"
                    f"{self.processor_details.workflow_template_name} could"
                    f"not be found in namespace {settings.NAMESPACE}"
                )

    # TODO Rename to submit_workflow_template to free up the name for submit_workflow.
    def submit_workflow(self, **kwargs):
        if self.processor_details == FaasProcessor.custom:
            return Exception(
                "Argo Workflow Templates are not available when using"
                "FaasProcessor.custom"
            )

        if (
            "user_id" in kwargs
            and re.match(LABEL_VALIDATION_REGEX, kwargs["user_id"]) is None
        ):
            raise ValueError("invalid user_id")
        if (
            "job_id" in kwargs
            and re.match(LABEL_VALIDATION_REGEX, kwargs["job_id"]) is None
        ):
            raise ValueError("invalid user_id")

        arguments = [Parameter(name=k, value=v) for k, v in kwargs.items()]

        workflow = Workflow(
            workflow_template_ref=WorkflowTemplateRef(
                name=self.processor_details.workflow_template_name
            ),
            workflows_service=self.workflows_service,
            namespace=settings.NAMESPACE,
            generate_name=f"{self.processor_details.name}-",
            arguments=arguments,
        )

        workflow.create()

        logger.info(
            f"Submitted {self.processor_details.name.upper()} workflow: {workflow.name}"
        )
        return workflow.name

    # Required for OpenEO sync jobs
    async def wait_for_completion(self, workflow_name, poll_interval=30):
        wf = self.workflows_service.get_workflow(
            workflow_name, namespace=settings.NAMESPACE
        )

        # keep polling for workflow status until completed,
        # at the interval dictated by the user
        # While the workflow is still initialising, this comes back as None,
        # so have to accept that here too!
        while wf.status.phase in ("Pending", "Running", None):
            await asyncio.sleep(poll_interval)
            wf = self.workflows_service.get_workflow(
                workflow_name, namespace=settings.NAMESPACE
            )
        return wf

    # Required when we want to halt code and wait.
    def block_wait_for_completion(self, workflow_name, poll_interval=30):
        wf = self.workflows_service.get_workflow(
            workflow_name, namespace=settings.NAMESPACE
        )

        # keep polling for workflow status until completed,
        # at the interval dictated by the user
        # While the workflow is still initialising, this comes back as None,
        # so have to accept that here too!
        while wf.status.phase in ("Pending", "Running", None):
            time.sleep(poll_interval)
            wf = self.workflows_service.get_workflow(
                workflow_name, namespace=settings.NAMESPACE
            )
        return wf

    def get_workflow_status(self, workflow_name: str) -> dict:
        # TODO: Limit this response to only the required fields
        workflow_response = self.workflows_service.get_workflow(
            name=workflow_name, namespace=settings.NAMESPACE
        )
        return dict(workflow_response.status)

    def stop_workflow(self, name):
        req = WorkflowStopRequest(name=name, namespace=settings.NAMESPACE)
        try:
            self.workflows_service.stop_workflow(
                name, req=req, namespace=settings.NAMESPACE
            )
            logger.info(f"Successfully stopped workflow {name}.")
        except NotFound:
            logger.warning(f"Could not stop workflow {name}.")

    def get_logs(self, workflow_name) -> list[str]:
        assert valid_host_scheme(
            self.workflows_service.host
        ), "The host scheme is required for service usage"
        resp = requests.get(
            url=urljoin(
                self.workflows_service.host, "api/v1/workflows/{namespace}/{name}/log"
            ).format(name=workflow_name, namespace=settings.NAMESPACE),
            params={
                "podName": None,
                "logOptions.container": "main",
                "logOptions.follow": None,
                "logOptions.previous": None,
                "logOptions.sinceSeconds": None,
                "logOptions.sinceTime.seconds": None,
                "logOptions.sinceTime.nanos": None,
                "logOptions.timestamps": None,
                "logOptions.tailLines": None,
                "logOptions.limitBytes": None,
                "logOptions.insecureSkipTLSVerifyBackend": None,
                "grep": None,
                "selector": None,
            },
            headers={"Authorization": f"Bearer {self.workflows_service.token}"},
            data=None,
            verify=self.workflows_service.verify_ssl,
        )

        if resp.ok:
            raw_logs = resp.content.decode("utf8").split("\n")
            return [
                json.loads(log)["result"]["content"]
                for log in raw_logs
                if log != "" and "content" in json.loads(log)["result"].keys()
            ]

        raise exception_from_server_response(resp)

    @abstractmethod
    def get_output_stac_items(self):
        raise NotImplementedError()


class CustomWorkflow(FaasProcessorBase):
    @classmethod
    def get_instance(cls):
        return cls(processor_details=FaasProcessor.custom.value)

    # Overwrite submit_workflow, just take a hera workflow and try to create it.
    def submit_workflow(self, workflow: Workflow):
        resp = workflow.create()

        return resp.metadata.name

    def get_output_stac_items(self, parameters: Any) -> list[Item]:
        raise NotImplementedError()


class FaasWorkflow(FaasProcessorBase):
    @classmethod
    def get_instance(cls, name):
        processor_map = {
            "force": FaasProcessor.Force.value,
            "sen2like": FaasProcessor.Sen2Like.value,
            "snap": FaasProcessor.Snap.value,
        }
        if name.lower() in processor_map:
            return cls(processor_details=processor_map[name.lower()])

    def submit_workflow(
        self,
        user_id: str,
        job_id: str,
        sen2like_parameters: Any = None,
        force_parameters: Any = None,
        snap_parameters: Any = None,
    ):
        if sen2like_parameters:
            return super().submit_workflow(
                sen2like_parameters=sen2like_parameters.json(),
                user_id=user_id,
                job_id=job_id,
            )
        if force_parameters:
            return super().submit_workflow(
                force_parameters=force_parameters.json(),
                user_id=user_id,
                job_id=job_id,
            )
        if snap_parameters:
            return super().submit_workflow(
                snap_parameters=snap_parameters.json(),
                user_id=user_id,
                job_id=job_id,
            )

    def get_output_stac_items(self, parameters: Any) -> list[Item]:
        """Not needed."""
        return None


class OpenEO(FaasProcessorBase):
    @classmethod
    def get_instance(cls):
        return cls(processor_details=FaasProcessor.OpenEO.value)

    def submit_workflow(
        self,
        openeo_parameters: Any,
        openeo_user_id: str,
        openeo_job_id: str,
    ):
        return super().submit_workflow(
            openeo_executor_parameters=openeo_parameters.json(),
            openeo_user_id=openeo_user_id,
            openeo_job_id=openeo_job_id,
        )

    def get_output_stac_items(self, openeo_parameters: Any) -> list[Item]:
        collection_file = list(openeo_parameters.stac_path.glob("*_collection.json"))[0]
        openeo_output_collection = Collection.from_file(str(collection_file))
        stac_items = [
            Item.from_file(link.get_absolute_href())
            for link in openeo_output_collection.get_item_links()
        ]

        return stac_items

    def _get_workflows_for_job_id(
        self, openeo_job_id, filter_workflow_status_phase: Optional[tuple[str]] = None
    ) -> list[Workflow]:
        # filter_workflow_status_phase wants to be an iterable
        # of strings like ("Running", "Pending")
        workflows = self.workflows_service.list_workflows(
            namespace=settings.NAMESPACE,
            label_selector=f"openeo_job_id={openeo_job_id}",
        ).items
        if filter_workflow_status_phase is not None:
            workflows_with_label_filtered = [
                workflow
                for workflow in workflows
                if workflow.status.phase in filter_workflow_status_phase
            ]
        else:
            workflows_with_label_filtered = workflows
        return workflows_with_label_filtered

    def stop_openeo_job(self, openeo_job_id):
        associated_unfinished_workflows = self._get_workflows_for_job_id(
            openeo_job_id=openeo_job_id,
            filter_workflow_status_phase=("Running", "Pending"),
        )
        logger.info(
            f"Stopping OpenEO job {openeo_job_id} with "
            f"{len(associated_unfinished_workflows)} unfinished sub-workflows."
        )

        # Need to stop all sub-jobs too!
        for workflow in associated_unfinished_workflows:
            if workflow.status.phase in ("Running", "Pending"):
                workflow_name = workflow.metadata.name
                super().stop_workflow(workflow_name)
        logger.info(f"Successfully stopped OpenEO job {openeo_job_id}.")
