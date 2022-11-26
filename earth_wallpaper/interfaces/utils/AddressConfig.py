from PySide6.QtCore import QStandardPaths
import os
import json
import logging


logger = logging.getLogger(__name__)

addrJson = "addr.json"
latitude = "latitude"
longitude = "longitude"
address = "address"


class AddressConfig(object):

    def get_addr(self):
        addr_json_config = self.record_file_path()
        if os.path.exists(addr_json_config):
            with open(addr_json_config, 'r') as f:
                addr_json = json.load(f)
                return addr_json
        else:
            addr_json = {address: "北京市", latitude: "39.906217", longitude: "116.3912757"}
            json_data = json.dumps(addr_json, indent=4, ensure_ascii=False)
            f = open(addr_json_config, 'w')
            f.write(json_data)
            f.close()
            return addr_json

    @staticmethod
    def record_file_path() -> str:
        config = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        return os.path.join(config, 'earth-wallpaper/' + addrJson)
