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
        sleep_time = 60*mins
        print("=====开始休息=====")
        for i in range(sleep_time):
            time.sleep(1)
            print("need sleep %d" % (sleep_time-i))
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
                except Exception as e:
                    print("没找到正确任务配置")
                    print(e)
                    print("================")
                    break
                _settings = open(f"{ROOT_PATH}/backend/settings.json",encoding='utf-8')
                if not check_sleep(json.load(_settings)):
                    os.system('python backend/main.py')


