import json
from types import SimpleNamespace
from pyinim.cloud.types.token import Token
from pyinim.cloud.types.devices import Devices

API_CLOUD_BASEURL = "https://api.inimcloud.com"


class CloudResolver:
    def __init__(self, username, password, client_id):
        self.password = password
        self.username = username
        self.client_id = client_id

    def get_token_url(self):
        data = {
            "Node": "inimhome",
            "Name": "it.inim.inimutenti",
            "ClientIP": "",
            "Method": "RegisterClient",
            "ClientId": "",
            "Token": "",
            "Params": {
                "Username": f"{self.username}",
                "Password": f"{self.password}",
                "ClientId": f"{self.client_id}",
                "ClientName": "Galaxy+S8+edge",
                "ClientInfo": json.dumps(
                    {
                        "name": "com.inim.alienmobile",
                        "version": "3.1.0",
                        "device": "hero2lte",
                        "brand": "samsung",
                        "platform": "android",
                        "osversion": "Oreo+v8.0,+API+Level:+26",
                    }
                ),
                "Role": "1",
                "Brand": "0",
            },
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def get_devices_extended_url(self, token):
        data = {
            "Params": {
                "Info": 4223,
            },
            "Node": "",
            "Name": "Inim Home",
            "ClientIP": "",
            "Method": "GetDevicesExtended",
            "Token": token,
            "ClientId": self.client_id,
            "Context": "intrusion",
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def get_request_poll_url(self, token, device_id):
        # DeviceId gets rendered without quotes in the original, so keeping it an int/string type instead of forcing str quotes.
        data = {
            "Params": {
                "DeviceId": int(device_id),
                "Type": 5,
            },
            "Node": "",
            "Name": "Inim Home",
            "ClientIP": "",
            "Method": "RequestPoll",
            "Token": token,
            "ClientId": self.client_id,
            "Context": "intrusion",
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def get_activate_scenario_url(self, token, device_id, scenario_id):
        data = {
            "Name": "it.inim.inimutenti",
            "ClientIP": "",
            "Method": "ActivateScenario",
            "ClientId": self.client_id,
            "Token": token,
            "Params": {
                "DeviceId": str(device_id),
                "ScenarioId": str(scenario_id),
            },
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def get_set_zone_bypass_url(self, token, device_id, zone_id, code, mode, value):
        data = {
            "Node": "inimhome",
            "Name": "it.inim.inimutenti",
            "ClientIP": "",
            "Method": "InsertZone",
            "Token": token,
            "ClientId": self.client_id,
            "Params": {
                "ZoneId": int(zone_id),
                "Mode": int(mode),
                "DeviceId": str(device_id),
                "Code": str(code),
                "Value": int(value),
            },
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def get_insert_areas_url(self, token, device_id, area_ids, mode, code):
        data = {
            "Node": "inimhome",
            "Name": "it.inim.inimutenti",
            "ClientIP": "",
            "Method": "InsertAreas",
            "Token": token,
            "ClientId": self.client_id,
            "Params": {
                "AreaIds": area_ids,
                "Mode": int(mode),
                "DeviceId": str(device_id),
                "Code": str(code),
            },
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def str_to_token(self, data: str):
        token: Token = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return token

    def str_to_devices(self, data: str, device_id: str):
        devices: Devices = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        update = {device_id: getattr(devices.Data, device_id)}
        devices.Data = dict()
        devices.Data.update(**update)

        return devices

    def str_to_devices_list(self, data: str) -> dict[str, Devices]:
        devices: Devices = json.loads(data)
        return devices
