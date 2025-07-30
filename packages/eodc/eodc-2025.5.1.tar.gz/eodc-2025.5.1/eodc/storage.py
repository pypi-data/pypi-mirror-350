import json
import time

import requests

from eodc import settings


def recall_files_from_tape(
    file_paths: list[str], interval_seconds: int = 60, timeout_seconds: int = 600
):
    """
    Starts staging (thaws) the files in file_paths via the Chiller API and then
    polls the returned link until either,
    an ERROR has occured or the State is Finished.
    Afterwards checks the requested files against those that have been staged.

    Blocks until error, timeout or finished staging.

    Parameters:
        file_paths (List[str]):
            The paths of the requested files, which might be on tape
        interval_seconds (int):
            The number of tries for polling
        timeout_seconds (int):
            The total amount of
    Returns:
        Missing File List(List[str]):
            a list of all file paths of files that have been requested,
            but haven't been staged (if empty, all files have been staged)

    """
    data = "\n".join(file_paths)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(
        str(settings.CHILLER_URL) + "/upload", data=data, headers=headers
    )

    polling_url = response.content.decode()

    polling_url = polling_url.rstrip("\n")

    while timeout_seconds > 0:
        response = requests.get(polling_url, verify=False)

        if response:
            if (
                str(json.loads(response.content.decode())["State"]).lower()
                == "finished"
            ):
                staged_files_path = json.loads(response.content.decode())["StagedFiles"]

                with open(staged_files_path) as file:
                    staged_files = file.readlines()

                staged_files = [line.strip() for line in staged_files]
                missing_files = set(file_paths) - set(staged_files)

                return list(missing_files)

            elif json.loads(response.content.decode())["State"] == "ERROR":
                raise RuntimeError("Files could not be staged.")

        if timeout_seconds > interval_seconds:
            time.sleep(interval_seconds)

        timeout_seconds -= interval_seconds

    raise TimeoutError("Too much time has elapsed, timeout reached.")
