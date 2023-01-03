import sys
import os
import time
import re
import json

queue = sys.argv[1]
_list = re.split('，|,', queue)
ROOT_PATH = os.path.abspath('.')

def check_sleep(_settings_dict):
    if _settings_dict["game"]["farmingMode"] == "Take a break":
        mins = _settings_dict["game"]["itemAmount"]
        time.sleep(60*mins)
        return True
    else:
        return False


for i in _list:
    if i != '':
        if '任务' not in i:
            print("未找到可执行任务")
            break
        else:
            num = i.split("任务")[-1]
            if not num.isnumeric():
                print("任务名异常")
                break
            else:
                dir = ROOT_PATH+'/backend/farm_queue/'
                _file = dir + 'settings' + str(num) + '.json'
                newdir = ROOT_PATH+'/backend/'
                try:
                    if os.path.exists(newdir+'settings.json'):
                        os.remove(newdir+'settings.json')
                    os.rename(_file,newdir+'settings.json')
                except:
                    print("没找到正确任务配置")
                    break
                _settings = open(f"{ROOT_PATH}/backend/settings.json",encoding='utf-8')
                if not check_sleep(json.load(_settings)):
                    os.system('python backend/main.py')


