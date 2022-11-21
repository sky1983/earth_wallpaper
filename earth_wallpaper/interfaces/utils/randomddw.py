from PySide6.QtCore import QStandardPaths
import os
import json
import datetime
import random

record = "ddwrecord.json"


class RandomDdw(object):

    def get_ddw_file(self, ddw_dir):
        files = os.listdir(ddw_dir)
        files = list(filter(self.ddw_filter, files))
        today = datetime.date.today()
        today_str = today.strftime("%Y-%m-%d")
        temp_record = self.record_file_path()
        if os.path.exists(temp_record):
            with open(temp_record, 'r') as f:
                record_json = json.load(f)
                print(record_json['currentDDW'])
                print(record_json['recordDate'])
                if today_str == record_json['recordDate']:
                    return ddw_dir + "/" + record_json['currentDDW']
                files = list(filter(lambda seq: self.ddw_filter_current(record_json['currentDDW'], seq), files))
                ddw_file = random.choice(files)
                self.write_json(temp_record, ddw_file, today_str)
                return ddw_dir + "/" + ddw_file
        else:
            ddw_file = random.choice(files)
            self.write_json(temp_record, ddw_file, today_str)
            return ddw_dir + "/" + ddw_file

    @staticmethod
    def write_json(self, temp_record, file, today):
        print("当前文件位置：" + temp_record)
        record_json = {"currentDDW": file, "recordDate": today}
        json_data = json.dumps(record_json, indent=4, ensure_ascii=False)
        f = open(temp_record, 'w')
        f.write(json_data)
        f.close()

    @staticmethod
    def ddw_filter(self, f):
        if f[-4:] in ['.ddw']:
            return True
        else:
            return False

    @staticmethod
    def ddw_filter_current(self, current_ddw, f):
        if f == current_ddw:
            return False
        else:
            return True

    @staticmethod
    def record_file_path() -> str:
        config = QStandardPaths.writableLocation(QStandardPaths.ConfigLocation)
        return os.path.join(config, 'earth-wallpaper/' + record)
