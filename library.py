from json import load, dump
from datetime import datetime
import os

def getCurrentTime():
    currentDT = datetime.datetime.now()
    return currentDT.strftime("date: %d/%m/%Y, %H:%M:%S")

class Json:
    def load(self, pathfile="", encoding='utf-8'):
        try:
            with open(pathfile, "r", encoding=encoding) as f:
                data = load(f)
                return data
        except IOError:
            print(f"cannot load {pathfile}")
            return False

    def loadWrite(self, pathfile="", default={}, encoding='utf-8'):
        try:
            with open(pathfile, "r", encoding=encoding) as f:
                data = load(f)
                return data
        except IOError:
            cur_path = ""
            for path in pathfile.split("/")[:-1]:
                cur_path += path+"/"
                try:
                    os.mkdir(cur_path)
                except Exception:
                    pass
            with open(pathfile, 'w', encoding=encoding) as f:
                dump(default, f, indent=4, ensure_ascii=False)
                return default

    def write(self, pathfile="", default={}, encoding="utf-8"):
        try:
            cur_path = ""
            for path in pathfile.split("/")[:-1]:
                cur_path += path+"/"
                try:
                    os.mkdir(cur_path)
                except Exception:
                    pass
            with open(pathfile, 'w', encoding=encoding) as f:
                dump(default, f, indent=4, ensure_ascii=False)
                return True
        except IOError:
            print(f"cannot write {pathfile}")
