from json import load, dump
import os
import datetime

RD = {
    "0": '0️⃣',
    '1': "1️⃣",
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣',
    '10': '🔟'
}
IRD = {
    '0️⃣': '0',
    '1️⃣': '1️',
    '2️⃣': '2️',
    '3️⃣': '3️',
    '4️⃣': '4️',
    '5️⃣': '5️',
    '6️⃣': '6️',
    '7️⃣': '7️',
    '8️⃣': '8️',
    '9️⃣': '9️'
}


def existKey(_key: str, _dict: dict) -> (bool):
    try:
        return _key in list(_dict.keys())
    except Exception:
        return False


def handleArgs(content):
    args = []
    message = ""
    found_message = False
    for word in content.split():
        if word.startswith("#"):
            found_message = True
        if found_message:
            message += word+" "
        else:
            args.append(word)
    a = []
    text = ""
    found = False
    for arg in args:
        if arg.startswith("\"") and not arg.endswith("\n"):
            found = True
        if found:
            text += arg+" "
            if arg.endswith("\"") and not arg.startswith("\""):
                a.append(text[1:-2])
                text = ""
                found = False
        else:
            a.append(arg)
    if len(text) > 0:
        a = a + text.split()
    return a, message.rstrip()[1:]


def getCurrentTime():
    currentDT = datetime.datetime.now()
    return currentDT.strftime("date: %d/%m/%Y, %H:%M:%S")


def getTimeKey():
    currentDT = datetime.datetime.now()
    return currentDT.strftime("%d%H%M%S")


class Json:
    def load(pathfile="", encoding='utf-8'):
        try:
            with open(pathfile, "r", encoding=encoding) as f:
                data = load(f)
                return data
        except IOError:
            print(f"cannot load {pathfile}")
            return False

    def loadWrite(pathfile="", default={}, encoding='utf-8'):
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

    def write(pathfile="", default={}, encoding="utf-8", **kv):
        try:
            cur_path = ""
            for path in pathfile.split("/")[:-1]:
                cur_path += path+"/"
                try:
                    os.mkdir(cur_path)
                except Exception:
                    pass
            with open(pathfile, 'w', encoding=encoding) as f:
                dump(default, f, indent=4, ensure_ascii=False, **kv)
                return True
        except IOError:
            print(f"cannot write {pathfile}")
