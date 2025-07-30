import json
from socket import timeout

import requests
from halo import Halo


class Backend:
    def __init__(self, context):
        self.ctx = context
        self.base_url = "https://cli-api.wavecount.net"
        self.access_token = (
            self.ctx.obj["access_token"] if "access_token" in self.ctx.obj else ""
        )
        self.headers = {"Authorization": "Bearer {}".format(self.access_token)}

    def _call_api(
        self,
        path,
        method="get",
        params={},
        data={},
        running_message="wait a moment ...",
        done_message="",
    ):
        endpoint = self.base_url + path
        timeoutInSec = 10
        spinner = Halo(spinner="dots3", text_color="cyan").start(text=running_message)
        try:
            if method == "post":
                res = requests.post(
                    url=endpoint,
                    json=data,
                    params=params,
                    headers=self.headers,
                    timeout=timeoutInSec,
                )
            elif method == "delete":
                res = requests.delete(
                    url=endpoint,
                    headers=self.headers,
                    timeout=timeoutInSec,
                )
            elif method == "get":
                res = requests.get(
                    url=endpoint,
                    params=params,
                    headers=self.headers,
                    timeout=timeoutInSec,
                )
            elif method == "patch":
                res = requests.patch(
                    url=endpoint, json=data, headers=self.headers, timeout=timeoutInSec
                )
            else:
                raise BaseException("Method is not valid")
            if res.status_code == 200:
                spinner.succeed(text="voila! {}".format(done_message))
                return res
            elif res.status_code == 204:
                spinner.succeed("voila! {}".format(done_message))
            elif (
                res.status_code == 400
                or res.status_code == 401
                or res.status_code == 404
                or res.status_code == 409
                or res.status_code == 422
            ):
                spinner.fail(text="oops!! {}".format(res.json()["error"]["message"]))
                exit()
            else:
                raise BaseException(res.json())
        except requests.ConnectionError as e:
            spinner.fail(
                text="oops!! Connection Error. Make sure you are connected to Internet."
            )
            exit()
        except requests.Timeout as e:
            spinner.fail(text="oops!! Timeout Error")
            exit()
        except requests.RequestException as e:
            spinner.fail(text="oops!! General Error")
            exit()
        except KeyboardInterrupt:
            spinner.fail(text="Someone closed the program")
            exit()

    def login(self, data):
        path = "/api/auth/login"
        result = self._call_api(
            path=path,
            method="post",
            data=data,
            running_message="Authenticating ...",
            done_message="Authenticated",
        )
        return result.json()

    def sync_cache(self):
        path = "/api/v2/auth/sync"
        result = self._call_api(
            path=path,
            method="get",
            running_message="Syncing ...",
            done_message="Synchronized",
        )
        return result.json()

    def register_device(self, data):
        path = "/api/devices"
        result = self._call_api(
            path=path, method="post", data=data, running_message="Registering ..."
        )
        return result.json()

    def get_error_flags(self):
        path = "/api/errors"
        result = self._call_api(
            path=path,
            method="get",
            running_message="Fetching ...",
            done_message="Fetched",
        )
        return result.json()

    def get_devices_list(self, where={}):
        params = {"where": json.dumps(where)}
        path = "/api/devices"
        result = self._call_api(
            path=path,
            params=params,
            running_message="Getting Devices List ...",
            done_message="Got Devices List",
        )
        return result.json()

    def get_device_info(self, device_id: str):
        path = "/api/devices/{0}/info".format(device_id)
        result = self._call_api(
            path=path,
            running_message="Getting Device Info ...",
            done_message="Got Device Info",
        )
        return result.json()

    def update_devices(self, desired_version, where={}, when=None, is_forced=False):
        params = {
            "desiredVersion": desired_version,
            "where": json.dumps(where),
            "when": when,
            "isForced": is_forced,
        }
        path = "/api/devices/update"
        result = self._call_api(path=path, params=params, running_message="Running")
        return result.json()

    def failed_update_devices(self):
        path = "/api/devices/failed-update"
        result = self._call_api(path=path, running_message="Running")
        return result.json()

    def reboot_devices(self, where={}):
        params = {"where": json.dumps(where)}
        path = "/api/devices/reboot"
        result = self._call_api(path=path, params=params, running_message="Running ...")
        return result.json()

    def reset_service(self, where={}):
        params = {"where": json.dumps(where)}
        path = "/api/devices/reset"
        result = self._call_api(path=path, params=params, running_message="Running ...")
        return result.json()

    def delete_device(self, device_id):
        path = "/api/devices/{0}".format(device_id)
        return self._call_api(
            path=path,
            method="delete",
            running_message="Deleting device {0} ...".format(device_id),
        )

    def request_device_logs(
        self, is_forced, device_id=None, serial_number=None, targets=None, period=None
    ):
        path = "/api/logs/request"
        query_params = {
            "isForced": is_forced,
            "deviceId": device_id,
            "serialNumber": serial_number,
            "targets": targets,
            "period": json.dumps(period),
        }
        result = self._call_api(
            path=path,
            method="get",
            params=query_params,
            running_message="Preparing logs ...",
            done_message="Prepared",
        )
        return result.json()

    def download_device_logs(self, blob_name):
        path = "/api/logs/download"
        query_patams = {"blobName": blob_name}
        result = self._call_api(
            path=path,
            params=query_patams,
            running_message="Downloading logs ...",
            done_message="Downloaded",
        )
        return result.content

    def update_contract(self, customerName: str, contract_id: int):
        path = "/api/contracts/{0}".format(customerName)
        data = {"contractID": contract_id}
        result = self._call_api(method="patch", path=path, data=data)
        return result.content

    def get_company_info(self, customerName: str):
        path = "/api/customers/{0}".format(customerName)
        result = self._call_api(method="get", path=path)
        return result.json()

    def reset_hash_time(self, datetime: str, where):
        params = {"where": json.dumps(where)}
        path = "/api/devices/reset-hash-time"
        result = self._call_api(
            method="post",
            path=path,
            params=params,
            data={"datetime": datetime},
            running_message="Running ...",
        )
        return result.json()

    def get_connectivity_events(self, device_id=None, serial_number=None, limit=None):
        params = {"deviceId": device_id, "serialNumber": serial_number, "limit": limit}
        path = "/api/events/connectivity"
        result = self._call_api(
            method="get",
            path=path,
            params=params,
            running_message="Running ...",
        )
        return result.json()
