import sys
import os
import time
import re
import json
import shutil

queue = sys.argv[1]
_list = re.split('，|,', queue)
ROOT_PATH = os.path.abspath('.')
sleep_time = 0

def check_sleep(_settings_dict):
    if _settings_dict["game"]["farmingMode"] == "Take a break":
        mins = _settings_dict["game"]["itemAmount"]
        global sleep_time
        sleep_time = 60*mins
        print("=====开始休息=====")
        return True
    else:
        return False

newdir = ROOT_PATH+'/backend/'
for filename in os.listdir(newdir):
    if filename.endswith("json"):
        os.remove(os.path.join(newdir, filename))
count = 0
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
                    _settings = open(_file,encoding='utf-8')
                    if not check_sleep(json.load(_settings)):
                        _settings.close()
                        os.rename(_file,newdir+'settings%s.json' % count)
                    else:
                        _settings.close()
                        os.rename(_file,newdir+'settings%s_%s.json' % (count,sleep_time))
                except Exception as e:
                    print("没找到正确任务配置")
                    print(e)
                    print("================")
                    break
                count += 1
os.system('python backend/main.py')


