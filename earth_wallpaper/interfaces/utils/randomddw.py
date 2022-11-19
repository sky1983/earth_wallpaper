from PySide6.QtCore import QStandardPaths
import os
import json
import datetime
import random

record = "ddwrecord.json"


class RandomDdw(object):

    def getDdwFile(self,ddwDir):
        files = os.listdir(ddwDir)
        files = list(filter(self.ddw_filter, files))
        today = datetime.date.today()
        todayStr = today.strftime("%Y-%m-%d")
        tempRecord = os.path.join(QStandardPaths.writableLocation(QStandardPaths.ConfigLocation),
                                        "earth-wallpaper/") + record
        if os.path.exists(tempRecord):
            with open(tempRecord, 'r') as f:
                recordJson = json.load(f)
                print(recordJson['currentDDW'])
                print(recordJson['recordDate'])
                if todayStr == recordJson['recordDate']:
                    return ddwDir + "/" + recordJson['currentDDW']
                files = list(filter(lambda seq: self.ddw_filter_current(recordJson['currentDDW'],seq),files))
                ddwFile = random.choice(files)
                self.writeJson(tempRecord, ddwFile, todayStr)
                return ddwDir + "/" + ddwFile
        else:
            ddwFile = random.choice(files)
            self.writeJson(tempRecord, ddwFile, todayStr)
            return ddwDir + "/" + ddwFile

    def writeJson(self,tempRecord,file,today):
        print("当前文件位置：" + tempRecord)
        recordJson = {"currentDDW": file, "recordDate": today}
        jsondata = json.dumps(recordJson, indent=4, ensure_ascii=False)
        f = open(tempRecord, 'w')
        f.write(jsondata)
        f.close()

    def ddw_filter(self,f):
        if f[-4:] in ['.ddw']:
            return True
        else:
            return False


    def ddw_filter_current(self,currentDDW, f):
        if f == currentDDW:
            return False
        else:
            return True

