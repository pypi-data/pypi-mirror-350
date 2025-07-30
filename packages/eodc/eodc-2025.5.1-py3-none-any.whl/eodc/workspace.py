import json
import os
import subprocess as sp
import uuid
from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Optional, TypedDict, Union

import boto3
import fsspec
import pystac
from azure.storage.blob import BlobServiceClient
from minio import Minio, MinioAdmin
from pydantic import SecretStr
from pystac import Item, Link
from pystac.extensions.eo import Band, EOExtension
from pystac.stac_io import DefaultStacIO
from typing_extensions import Self

raster_band = [
    Band.create(
        name="raster-result", description="Raster Result", common_name="raster-result"
    )
]

EODC_CEPH_URL = "https://objectstore.eodc.eu:2222"


class StorageType(Enum):
    MINIO = "minio"
    AZURE = "azure"
    CEPH = "ceph"


class WorkspaceAdapter(DefaultStacIO):
    """
    The WorkspaceAdapter is an abstract class that defines the minimum
    interface for interacting with workspaces. It abstracts away the
    underlying storage system, so that the EODC API can be used with
    different providers.

    It also implements the DefaultStacIO interface, which allows it to
    be used with the pystac library.
    """

    storage_type: StorageType

    @staticmethod
    def create_adapter(
        storage_type: StorageType = StorageType.CEPH,
        parameters: dict[str, Any] = {},
    ) -> Self:
        """
        This function is a factory method that creates an instance of the
        WorkspaceAdapter based on the given parameters.

        Returns none if the storage type is not supported.
        """
        if storage_type == StorageType.MINIO:
            return MinIOAdapter(
                url=parameters["url"],
                access_key=parameters["access_key"],
                secret_key=parameters["secret_key"],
                mc_bin_path=parameters["mc_bin_path"],
            )
        elif storage_type == StorageType.AZURE:
            return AzureAdapter(
                connection_string=parameters["connection_string"],
            )
        elif storage_type == StorageType.CEPH:
            return CephAdapter(
                url=parameters["url"],
                access_key=parameters["access_key"],
                secret_key=parameters["secret_key"],
            )
        else:
            return None

    @abstractmethod
    def get_credentials(self) -> dict[str, Any]:
        """
        This method returns the credentials needed to connect to the storage.

        The credentials are returned as a dictionary, where the keys are the
        names of the credentials and the values are the credentials themselves.

        This is useful for debugging and for passing the credentials to other
        parts of the system.

        returns:
            dict[str, Any]: A dictionary containing the credentials.
        """
        pass

    @abstractmethod
    def create_user_workspace(
        self, workspace_name: str = "", user_name: str = "", **kwargs
    ) -> None:
        """
        This method creates a new workspace for a user.
        Depending on the storage system, this may involve creating a new bucket,
        creating a new container, or however else the storage system represents
        workspaces.

        returns:
            None
        """
        pass

    @abstractmethod
    def delete_user_workspace(self, workspace_name: str = "") -> None:
        """
        This method deletes a workspace for a user.

        Depending on the storage system, this may involve deleting a bucket,
        deleting a container, or however else the storage system represents
        workspaces.

        If the workspace does not exist, this method should raise an error.
        If the workspace is not empty, this method should raise an error.

        returns:
            None
        """
        pass

    @abstractmethod
    def workspace_exists(self, workspace_name: str = "") -> bool:
        """
        This method checks if a workspace exists with the current adapter.

        returns:
            bool: True if the workspace exists, False otherwise.
        """
        pass

    @abstractmethod
    def list_workspaces(self) -> list[str]:
        """
        This method lists all the workspaces that exist with the current adapter.

        returns:
            list[str]: A list of workspace names.
        """
        pass

    @abstractmethod
    def list_workspace_files(self, workspace_name: str = "") -> list[str]:
        """
        This method lists all the files in a workspace.

        returns:
            list[str]: A list of file names/paths.
        """
        pass

    @abstractmethod
    def upload_file(
        self, workspace_name: str = "", file_path: str = "", path_in_workspace: str = ""
    ) -> None:
        """
        This method uploads a file to a workspace.

        The file is uploaded to the workspace with the given name, and is placed
        in the workspace at the given path.

        parameters:
            file_path (str): The path to the file to be uploaded.
            path_in_workspace (str): The path in the workspace where the file
            should be placed.

        returns:
            None
        """
        pass

    @abstractmethod
    def upload_stream(
        self, workspace_name: str = "", stream: Any = None, file_name: str = ""
    ) -> None:
        """
        This method uploads a stream to a workspace.

        The stream is uploaded to the workspace with the given name, and is placed
        in the workspace at the given path.

        returns:
            None
        """
        pass

    @abstractmethod
    def delete_file(self, workspace_name: str = "", file_name: str = "") -> None:
        """
        This method deletes a file from a workspace.

        The file is deleted from the workspace with the given name.

        returns:
            None
        """
        pass

    @abstractmethod
    def download_file(
        self, workspace_name: str = "", file_name: str = "", path: str = ""
    ) -> None:
        """
        This method downloads a file from a workspace.

        The file is downloaded from the workspace with the given name, and is placed
        in the given path.

        returns:
            None
        """
        pass

    @abstractmethod
    def download_stream(self, workspace_name: str = "", file_name: str = "") -> Any:
        """
        This method downloads a stream from a workspace.

        The stream is downloaded from the workspace with the given name
        and returned.

        returns:
            Any: The stream that was downloaded.
        """
        pass

    @abstractmethod
    def get_fsspec(self, workspace_name: str = "") -> Any:
        """
        This method returns an fsspec filesystem object for the given workspace.

        This object can be used to interact with the workspace using the fsspec
        library.

        returns:
            Any: An fsspec filesystem object.
        """
        pass

    @abstractmethod
    def get_signed_url(
        self, bucket_name, object_key, method="GET", expiration_time=3600
    ):
        """
        This method returns a signed URL for the given object in the given bucket.

        The signed URL can be used to access the object without needing to authenticate.

        returns:
            str: The signed URL.
        """
        pass

    def upload_path(
        self,
        workspace_name: str = "",
        path: str = "",
        path_in_workspace: str = "",
        recursive: bool = False,
    ):
        """
        This method uploads a path to a workspace.

        The path is uploaded to the workspace with the given name, and is placed
        in the workspace at the given path.

        parameters:
            workspace_name (str): Workspace name to upload to.
            path (str): The path to the file to be uploaded.
            path_in_workspace (str): The path in the workspace where
            the file should be placed.
            recursive (bool): Whether to upload the path recursively.

        returns:
            None
        """
        path_in_workspace = path_in_workspace.removesuffix("/")
        files = Path(path).rglob("*") if recursive else Path(path).glob("*")

        for file in files:
            if not file.is_file():
                continue
            relative_path = "/".join(os.path.relpath(file, path).split("/")[:-1])
            new_path_in_workspace = os.path.join(path_in_workspace, relative_path)

            self.upload_file(
                workspace_name,
                str(file),
                "" if new_path_in_workspace == "/" else new_path_in_workspace,
            )

    def list_stac_collections(self, workspace_name: str = ""):
        """
        This method looks for stac collection json files in the workspace, specifically
        results from EODC openEO batch jobs, this makes reloading results easier.

        returns:
            tuple made from collection_id string and the
            corresponding pystac collection objects
        """
        json_collection_id_files = [
            (
                file.split("/")[0],
                self.get_collection(
                    workspace_name=workspace_name, collection_id=file.split("/")[0]
                ),
            )
            for file in self.list_workspace_files(workspace_name=workspace_name)
            if file.endswith("_collection.json")
        ]

        return json_collection_id_files

    def get_collection(self, workspace_name: str = "", collection_id: str = ""):
        collection: pystac.Collection = pystac.read_file(
            href=f"/{workspace_name}/{collection_id}/STAC/{collection_id}_collection.json",
            stac_io=self,
        )

        return collection

    def _wrap_urls_modifier(
        self,
        item: pystac.Item,
        bucket_name,
        collection_name,
        url_modifier=None,
        **kwargs,
    ):
        # Get the signed URL for the item

        object_key = f"{collection_name}/{item.id}.tif"
        if not url_modifier:
            modified_url = self.get_signed_url(
                bucket_name, object_key=object_key, **kwargs
            )
        else:
            modified_url = url_modifier(bucket_name, object_key, **kwargs)

        # Update the item's href with the signed URL

        item_dict = item.to_dict(transform_hrefs=False)
        item_dict["assets"]["raster-result"]["href"] = modified_url

        return pystac.Item.from_dict(item_dict, preserve_dict=False)

    def get_stac_items(
        self, workspace_name, collection_id, url_modifier=None, **kwargs
    ) -> list[Item]:
        collection: pystac.Collection = self.get_collection(
            workspace_name=workspace_name, collection_id=collection_id
        )

        items: list[Item] = [
            pystac.Item.from_file(
                href=self._modify_href(item, workspace_name, collection_id),
                stac_io=self,
            )
            for item in collection.get_item_links()
        ]

        for item in items:
            eo = EOExtension.ext(item, add_if_missing=True)
            eo.apply(bands=raster_band)
            # re = RasterExtension.ext(item, add_if_missing=True)

        return [
            self._wrap_urls_modifier(
                item, workspace_name, collection_id, url_modifier, **kwargs
            )
            for item in items
        ]

    # Implement the abstract methods from DefaultStacIO
    def read_text(self, source: Union[str, Link], *args: Any, **kwargs: Any) -> str:
        bucket_name, object_key = self.parse_workspace_STAC_source(source)
        data = self.download_stream(bucket_name, object_key).read().decode("utf-8")
        return data

    def write_text(
        self, dest: Union[str, Link], txt: str, *args: Any, **kwargs: Any
    ) -> None:
        pass

    def parse_workspace_STAC_source(self, source: Union[str, Link]) -> tuple[str, str]:
        """ """
        split_source = source.split("/")

        workspace_name = split_source[1]
        object_key = "/".join(split_source[2:])

        return workspace_name, object_key

    def _modify_href(self, href: Link, bucket_name: str, collection_name: str):
        id = str(href.target).split("/")[-1].split(".")[0]

        return f"/{bucket_name}/{collection_name}/STAC/items/{id}.json"


class MinIOAdapter(WorkspaceAdapter):
    """
    The system on which this is running needs to have the mc (Minio Client)
    CLI tool installed

    This Adapter implements the MinIO API for the EODC Tenant, for local workspaces
    our API needs to be more extensive than for external workspaces, as we need to
    create and delete workspaces, as well as manage users and policies. For external
    workspaces, we only need to manage files.

    Workspaces are implemented as buckets, and files are implemented as objects.
    """

    alias: str

    minio_client: Minio
    minio_admin_client: MinioAdmin

    def __init__(
        self,
        url: str,
        access_key: Union[str, SecretStr],
        secret_key: Union[str, SecretStr],
        mc_bin_path: Any = None,
        alias: str = "MINIO_EODC",
    ):
        self.storage_type = StorageType.MINIO

        self.alias = alias

        self.access_key = (
            access_key if isinstance(access_key, SecretStr) else SecretStr(access_key)
        )
        self.secret_key = (
            secret_key if isinstance(secret_key, SecretStr) else SecretStr(secret_key)
        )

        self.minio_client = Minio(
            url,
            access_key=self.access_key.get_secret_value(),
            secret_key=self.secret_key.get_secret_value(),
            secure=True,
        )

        if mc_bin_path == "":
            mc_bin_path = None

        self.minio_admin_client = MinioAdmin(target=self.alias, binary_path=mc_bin_path)

        sp.run(
            f"mc config host add {self.alias} https://{url}/ \
            {access_key.get_secret_value()} {secret_key.get_secret_value()}",
            capture_output=True,
            shell=True,
        )

    def get_fsspec(self, workspace_name: str = ""):
        return fsspec.filesystem(
            "s3",
            anon=False,
            key=self.minio_client._access_key,
            secret=self.minio_client._secret_key,
            client_kwargs={
                "endpoint_url": self.minio_client._endpoint_url,
                "region_name": self.minio_client._region,
            },
            bucket=workspace_name,
        )

    def register_user(self, user_name: str) -> dict[str, str]:
        generated_secret_key: uuid.UUID = uuid.uuid4()
        self.minio_admin_client.user_add(user_name, str(generated_secret_key))
        return {"access_key": user_name, "secret_key": str(generated_secret_key)}

    def register_user_with_secret_key(self, user_name: str, secret_key: str):
        self.minio_admin_client.user_add(user_name, str(secret_key))
        return {"access_key": user_name, "secret_key": str(secret_key)}

    def remove_user(self, user_name: str):
        self.minio_admin_client.user_remove(user_name)

    def create_user_workspace(
        self, workspace_name: str = "", user_name: str = "", cwd: str = ""
    ) -> None:
        self._create_workspace(workspace_name=workspace_name)
        self._grant_workspace_to_user(
            workspace_name=workspace_name, user_name=user_name, cwd=cwd
        )

    def delete_user_workspace(self, workspace_name: str = ""):
        self._remove_workspace_policy(workspace_name=workspace_name)
        self._delete_workspace(workspace_name=workspace_name)

    def workspace_exists(self, workspace_name: str = "") -> bool:
        return self.minio_client.bucket_exists(workspace_name)

    def list_workspaces(self) -> list[str]:
        buckets = self.minio_client.list_buckets()
        return [bucket.name for bucket in buckets]

    def create_policy(self, policy_builder: "S3PolicyBuilder"):
        self.minio_admin_client.policy_add(
            policy_name=policy_builder.policy_name,
            policy_file=policy_builder.write_policy_file(
                policy_name=policy_builder, path=os.getcwd()
            ),
        )
        return policy_builder.policy_name

    def grant_policy_to_user(self, user_name: str, policy_name: str):
        self.minio_admin_client.policy_set(policy_name=policy_name, user=user_name)

    def grant_policy_to_group(self, group_name: str, policy_name: str):
        self.minio_admin_client.policy_set(policy_name=policy_name, group=group_name)

    def grant_new_policy_to_user(
        self, user_name: str, policy_builder: "S3PolicyBuilder"
    ):
        self.minio_admin_client.policy_set(
            policy_name=self.create_policy(policy_builder=policy_builder),
            user=user_name,
        )

    def grant_new_policy_to_group(
        self, group_name: str, policy_builder: "S3PolicyBuilder"
    ):
        self.minio_admin_client.policy_set(
            policy_name=self.create_policy(policy_builder=policy_builder),
            group=group_name,
        )

    def list_workspace_files(self, workspace_name: str = ""):
        return [
            obj.object_name for obj in self.minio_client.list_objects(workspace_name)
        ]

    def update_workspace(self, workspace_name: str = "", **kwargs):
        if "user_name" in kwargs.keys():
            self._grant_workspace_to_user(
                workspace_name=workspace_name,
                user_name=kwargs["user_name"],
                cwd=os.getcwd(),
            )

    def revoke_policy_from_user(self, policy_name: str, user_name: str):
        self.minio_admin_client.policy_unset(policy_name=policy_name, user=user_name)

    def revoke_policy_from_group(self, policy_name: str, group_name: str):
        self.minio_admin_client.policy_unset(policy_name=policy_name, group=group_name)

    def remove_policy(self, policy_name: str):
        for user in self.minio_admin_client.user_list():
            if "policyName" in user.keys() and policy_name in user["policyName"].split(
                ","
            ):
                self.revoke_policy_from_user(
                    policy_name=policy_name, user_name=user["accessKey"]
                )
        for group in self.minio_admin_client.group_list()[0]["groups"]:
            group_info = self.minio_admin_client.group_info(group)
            if "groupPolicy" in group_info.keys() and policy_name in group_info[
                "groupPolicy"
            ].split(","):
                self.revoke_policy_from_group(policy_name=policy_name, group_name=group)
        self.minio_admin_client.policy_remove(policy_name=policy_name)

    def list_users(self):
        return self.minio_admin_client.user_list()

    def list_groups(self):
        return self.minio_admin_client.group_list()

    def group_info(self, group_name: str):
        return self.minio_admin_client.group_info(group_name=group_name)

    def upload_file(self, workspace_name: str = "", file_path: str = ""):
        self.minio_client.fput_object(
            bucket_name=workspace_name,
            object_name=file_path.split("/")[-1],
            file_path=file_path,
        )

    def upload_stream(
        self, workspace_name: str = "", stream: Any = None, file_name: str = ""
    ):
        self.minio_client.put_object(
            bucket_name=workspace_name, object_name=file_name, data=stream
        )

    def delete_file(self, workspace_name: str = "", file_name: str = ""):
        self.minio_client.remove_object(
            bucket_name=workspace_name, object_name=file_name
        )

    def download_file(
        self, workspace_name: str = "", file_name: str = "", path: str = ""
    ):
        self.minio_client.fget_object(
            bucket_name=workspace_name, object_name=file_name, file_path=path
        )

    def download_stream(self, workspace_name: str = "", file_name: str = ""):
        return self.minio_client.get_object(
            bucket_name=workspace_name, object_name=file_name
        )

    def _remove_workspace_policy(self, workspace_name: str = ""):
        policy_name: str = f"BASIC_{workspace_name.upper()}"
        self.remove_policy(policy_name=policy_name)

    def _grant_workspace_to_user(
        self, workspace_name: str = "", user_name: str = "", cwd: str = ""
    ):
        policy_name: str = self._create_workspace_full_access_policy(
            workspace_name=workspace_name, cwd=cwd
        )
        self.minio_admin_client.policy_set(policy_name=policy_name, user=user_name)

    def _delete_workspace(self, workspace_name: str = ""):
        """
        raises S3Error
        """
        self.minio_client.remove_bucket(workspace_name)

    def _create_workspace_full_access_policy(
        self, workspace_name: str = "", cwd: str = ""
    ) -> str:
        policy_name: str = f"BASIC_{workspace_name.upper()}"
        policy_builder = S3PolicyBuilder(policy_name=policy_name)
        self.minio_admin_client.policy_add(
            policy_name=policy_name,
            policy_file=policy_builder.add_workspaces_full_privileges(
                workspace_names=[workspace_name]
            ).write_policy_file(policy_name=policy_name, path=cwd),
        )
        return policy_name

    def _create_workspace(self, workspace_name: str = ""):
        """
        raises S3Error
        """
        self.minio_client.make_bucket(workspace_name)


class CephAdapter(WorkspaceAdapter):
    """
    This Adapter implements the Ceph API for the Workspaces API.

    Workspaces are implemented as buckets, and files are implemented
    as objects.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        return self

    def __init__(
        self,
        url: str,
        access_key: Union[str, SecretStr],
        secret_key: Union[str, SecretStr],
    ):
        self.storage_type = StorageType.CEPH
        self.access_key = (
            access_key if isinstance(access_key, SecretStr) else SecretStr(access_key)
        )
        self.secret_key = (
            secret_key if isinstance(secret_key, SecretStr) else SecretStr(secret_key)
        )
        self.url = url
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key.get_secret_value(),
            aws_secret_access_key=self.secret_key.get_secret_value(),
            endpoint_url=url,
        )

        self.s3_session = boto3.Session(
            aws_access_key_id=self.access_key.get_secret_value(),
            aws_secret_access_key=self.secret_key.get_secret_value(),
        )

        handlers = self.s3_client.meta.events._emitter._handlers

        handlers_to_unregister = handlers.prefix_search("before-parameter-build.s3")
        handler_to_unregister = handlers_to_unregister[0]
        self.s3_client.meta.events._emitter.unregister(
            "before-parameter-build.s3", handler_to_unregister
        )

    def get_credentials(self):
        return {
            "url": self.url,
            "access_key": self.access_key.get_secret_value(),
            "secret_key": self.secret_key.get_secret_value(),
        }

    def list_workspaces(self) -> list[str]:
        return [bucket["Name"] for bucket in self.s3_client.list_buckets()["Buckets"]]

    def create_user_workspace(
        self, workspace_name: str = "", user_name: str = "", tenant_name: str = ""
    ) -> None:
        self.s3_client.create_bucket(Bucket=workspace_name)
        self._workspace_acl_private(workspace_name)
        self.grant_workspace_to_user(user_name, workspace_name, tenant_name=tenant_name)

    def _workspace_acl_private(self, workspace_name: str = ""):
        self.s3_client.put_bucket_acl(ACL="private", Bucket=workspace_name)

    def delete_user_workspace(self, workspace_name: str = ""):
        self.s3_client.delete_bucket(Bucket=workspace_name)

    def workspace_exists(self, workspace_name: str = "") -> bool:
        return workspace_name in self.list_workspaces()

    def list_workspace_files(
        self, workspace_name: str = "", tenant_name: str = None, verbose=False
    ):
        tenant_name = f"{tenant_name}:" if tenant_name else ""
        files = self.s3_client.list_objects(Bucket=f"{tenant_name}{workspace_name}")
        if "Contents" not in files:
            return []
        return [file["Key"] if not verbose else file for file in files["Contents"]]

    def get_tenant(self):
        """
        This is an experimental function,
        but in most cases of populated Tenants it should
        return the proper tenant name.

        Returns:
            Tenant Name: str
        """
        first_or_default_bucket = self.s3_client.list_buckets()["Buckets"][0]["Name"]
        return self.s3_client.list_objects(Bucket=first_or_default_bucket)["Contents"][
            0
        ]["Owner"]["ID"].split("$")[-1]

    def upload_file(
        self,
        workspace_name: str = "",
        file_path: str = "",
        path_in_workspace: str = "",
        tenant_name: str = "    ",
    ):
        tenant_name = f"{tenant_name}:" if tenant_name else ""
        path_in_workspace = path_in_workspace.removesuffix("/")
        self.s3_client.upload_file(
            file_path,
            f"{tenant_name}{workspace_name}",
            os.path.join(path_in_workspace, file_path.split("/")[-1]),
        )

    def upload_openeo_results():
        pass

    def upload_stream(
        self, workspace_name: str = "", stream: Any = None, file_name: str = ""
    ):
        self.s3_client.put_object(Bucket=workspace_name, Key=file_name, Body=stream)

    def delete_file(self, workspace_name: str = "", file_name: str = ""):
        self.s3_client.delete_object(Bucket=workspace_name, Key=file_name)

    def download_file(
        self, workspace_name: str = "", file_name: str = "", path: str = ""
    ):
        self.s3_client.download_file(workspace_name, file_name, path)

    def download_stream(self, workspace_name: str = "", file_name: str = ""):
        return self.s3_client.get_object(Bucket=workspace_name, Key=file_name)["Body"]

    def get_workspace(self, workspace_name: str = ""):
        return self.s3_client.get_bucket(workspace_name)

    def get_fsspec(self, workspace_name: str = ""):
        return fsspec.filesystem(
            "s3",
            anon=False,
            key=self.get_credentials()["access_key"],
            secret=self.get_credentials()["secret_key"],
            client_kwargs={
                "endpoint_url": self.get_credentials()["url"],
            },
            bucket=workspace_name,
        )

    def get_signed_url(
        self, bucket_name, object_key, method="GET", expiration_time=3600
    ):
        method = f"{method.lower()}_object"
        signed_url = self.s3_client.generate_presigned_url(
            ClientMethod=method,
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration_time,
        )

        return signed_url

    # Policies
    def grant_policy_to_workspace(
        self, workspace_name: str = "", policy_string: str = ""
    ):
        self.s3_client.put_bucket_policy(Bucket=workspace_name, Policy=policy_string)

    def grant_workspace_to_user(
        self, user_name: str, workspace_name: str = "", tenant_name=""
    ):
        policy_str = (
            S3PolicyBuilder(f"BASIC_{workspace_name.upper()}_{tenant_name}_{user_name}")
            .add_users_full_privileges(
                workspace_name, tenant_users=[(tenant_name, user_name)]
            )
            .build()
        )
        self.grant_policy_to_workspace(
            workspace_name=workspace_name, policy_string=json.dumps(policy_str)
        )

    def describe_workspace_policy(self, workspace_name: str = ""):
        return json.loads(
            self.s3_client.get_bucket_policy(Bucket=workspace_name)["Policy"]
        )

    def set_workspace_public_readonly_access(
        self, workspace_name: str, object_names: list[str] = ["*"]
    ):
        self._workspace_acl_private(workspace_name=workspace_name)
        public_readonly_access = (
            S3PolicyBuilder(policy_name="PublicReadOnly")
            .add_entry(
                bucket_name=workspace_name,
                object_names=object_names,
                privileges=["s3:ListBucket", "s3:GetObject"],
                tenant_users="*",
            )
            .build()
        )
        self.grant_policy_to_workspace(
            workspace_name=workspace_name,
            policy_string=json.dumps(public_readonly_access),
        )


class AzureAdapter(WorkspaceAdapter):
    """
    This Adapter implements the Azure API for the Workspaces API.

    Workspaces are implemented as containers, and files are implemented
    as blobs.

    File Paths are just blobnames seperated by forward slashes '/'
    """

    def __init__(
        self,
        connection_string: Union[str, SecretStr],
    ):
        self.storage_type = StorageType.AZURE
        self.connection_string = (
            connection_string
            if isinstance(connection_string, SecretStr)
            else SecretStr(connection_string)
        )

        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.connection_string.get_secret_value()
        )

    def get_credentials(self):
        return {"connection_string": self.connection_string.get_secret_value()}

    def create_user_workspace(
        self, workspace_name: str = "", user_name: str = "", **kwargs
    ):
        self.blob_service_client.create_container(workspace_name)

    def delete_user_workspace(self, workspace_name: str = ""):
        self.blob_service_client.delete_container(workspace_name)

    def get_fsspec(self, workspace_name: str = ""):
        return fsspec.filesystem(
            "az",
            anon=False,
            key=self.blob_service_client.credential.token["access_token"],
            client_kwargs={
                "account_url": self.blob_service_client.url,
                "container": workspace_name,
            },
        )

    def get_signed_url(
        self, bucket_name, object_key, method="GET", expiration_time=3600
    ):
        return ""

    def workspace_exists(self, workspace_name: str = "") -> bool:
        return self.blob_service_client.get_container_client(
            container=workspace_name
        ).exists()

    def list_workspaces(self) -> list[str]:
        return [
            container.name for container in self.blob_service_client.list_containers()
        ]

    def list_workspace_files(self, workspace_name: str = ""):
        return [
            blob.name
            for blob in self.blob_service_client.get_container_client(
                container=workspace_name
            ).list_blobs()
        ]

    def upload_file(
        self, workspace_name: str = "", file_path: str = "", path_in_workspace: str = ""
    ) -> None:
        blob_path = str(
            Path(path_in_workspace).joinpath(file_path.split("/")[-1]),
        )
        with open(file_path, "rb") as data:
            self.blob_service_client.get_blob_client(
                container=workspace_name,
                blob=blob_path,
            ).upload_blob(data)

    def upload_stream(
        self, workspace_name: str = "", stream: Any = None, file_name: str = ""
    ):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).upload_blob(stream)

    def delete_file(self, workspace_name: str = "", file_name: str = ""):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).delete_blob()

    def download_file(
        self, workspace_name: str = "", file_name: str = "", path: str = ""
    ):
        self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).download_blob().readinto(open(path, "wb"))

    def download_stream(self, workspace_name: str = "", file_name: str = ""):
        return self.blob_service_client.get_blob_client(
            container=workspace_name, blob=file_name
        ).download_blob()


class S3PolicyBuilder:
    """
    The s3 policy builder is a handy tool for building s3 policies in a structured way.
    It allows for the creation of policies that can be used to grant or deny access to
    various resources in an s3 bucket. The policy builder can be used to create policies
    for workspaces, objects and users.


    CEPH:

    When using this builder with ceph, the policy builder can be used to create policies
    attached to workspaces and objects, as ceph does not support user policies.

    This means you add user specific privileges to the policy, and then
    you grant it to the workspace. For this use all functions that look like:
    'add_user_..._privileges'


    If the user parameter is '*', the policy will be granted to all users.
    """

    class PolicyEntry(TypedDict):
        Effect: bool
        Action: list[str]
        Resource: list[str]
        Condition: Optional[dict[str, Any]]

    class Policy(TypedDict):
        Version: str
        Statement: list["S3PolicyBuilder.PolicyEntry"]

    policy_name: str = ""

    policy: Policy = {"Version": "2012-10-17", "Statement": []}

    @classmethod
    def make_policy_entry(
        cls,
        resource_names: list[str],
        actions: list[str],
        conditions: dict[str, Any] = None,
        tenant_users: str = list[tuple[str, str]],
        allow: bool = True,
    ) -> PolicyEntry:
        if isinstance(tenant_users, list):
            user_names = [
                f"arn:aws:iam::{tenant}:user/{user}" if tenant is not None else user
                for tenant, user in tenant_users
            ]
            principal = {"AWS": user_names} if user_names is not None else {}
        else:
            principal = "*" if tenant_users == "*" else {}

        return {
            "Sid": "Policy",
            "Effect": "Allow" if allow else "Deny",
            **({"Principal": principal}),
            "Action": [action for action in actions],
            "Resource": [f"arn:aws:s3:::{resource}" for resource in resource_names],
            **({"Condition": conditions} if conditions is not None else {}),
        }

    def __init__(self, policy_name: str):
        self.policy = {"Version": "2012-10-17", "Statement": []}
        self.policy_name = policy_name

    def build(self) -> Policy:
        return self.policy

    def write_policy_file(self, policy_name: str, path: str) -> str:
        abs_path = os.path.abspath(os.path.join(path, f"{policy_name}.json"))

        with open(abs_path, "w") as f:
            json.dump(self.policy, f)

        return abs_path

    def add_users_read_privileges(
        self,
        workspace_name: str = "",
        tenant_users: list[tuple[str, str]] = None,
    ) -> Self:
        assert tenant_users is not None, "Users must be specified"
        return self.add_entry(
            bucket_name=workspace_name,
            object_names=["*"],
            privileges=[
                "s3:ListBucket",
                "s3:GetObject",
            ],
            tenant_users=tenant_users,
            allow=True,
        )

    def add_users_write_privileges(
        self,
        workspace_name: str = "",
        tenant_users: list[tuple[str, str]] = None,
    ) -> Self:
        assert tenant_users is not None, "Users must be specified"
        return self.add_entry(
            bucket_name=workspace_name,
            object_names=["*"],
            privileges=[
                "s3:PutObject",
            ],
            tenant_users=tenant_users,
            allow=True,
        )

    def add_users_delete_privileges(
        self, workspace_name: str = "", tenant_users: list[tuple[str, str]] = None
    ) -> Self:
        assert tenant_users is not None, "Users must be specified"
        return self.add_entry(
            bucket_name=workspace_name,
            object_names=["*"],
            privileges=[
                "s3:DeleteObject",
            ],
            tenant_users=tenant_users,
            allow=True,
        )

    def add_users_full_privileges(
        self, bucket_name: str, tenant_users: list[tuple[str, str]] = None
    ) -> Self:
        assert tenant_users is not None, "Users must be specified"
        return self.add_entry(
            bucket_name=bucket_name,
            object_names=["*"],
            privileges=[
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
            ],
            tenant_users=tenant_users,
            allow=True,
        )

    def add_entry(
        self,
        bucket_name: str,
        object_names: list[str] = ["*"],
        privileges: Union[str, list[str]] = "s3:*",
        conditions: dict[str, Any] = None,
        tenant_users: list[tuple[str, str]] = None,
        allow: bool = True,
    ) -> Self:
        self.policy["Statement"].append(
            S3PolicyBuilder.make_policy_entry(
                resource_names=[
                    bucket_name,
                    *[f"{bucket_name}/{object_name}" for object_name in object_names],
                ],
                actions=privileges,
                conditions=conditions,
                tenant_users=tenant_users,
                allow=allow,
            )
        )
        return self


class WorkspaceError(Exception):
    pass
