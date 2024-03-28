import requests
import json
import getdata
import prompt
import util
import time
from json import JSONDecodeError
import os


GEMINI_URL = "https://aigc.sankuai.com/v1/google/models/gemini-pro:streamGenerateContent"
WENXIN_URL = "https://aigc.sankuai.com/v1/baidu/native/chat/completions_pro"
# 拆分成每ONCE_COUNT条数据一次，避免context过长
# 文心一言有时候不返回数组，而是给出解析，此时将数量改为5可以成功
# 有时候返回的数组长度不对，也需要适当减少，就可以返回成功
ONCE_COUNT = 10

# 如果失败，多尝试几次就可以


# 修改model，设定访问哪个模型
# MODEL = 'gemini'
MODEL = 'wenxin'


def gemini(data):
    
    myprompt = prompt.prompt + json.dumps([item['text'] for item in data], ensure_ascii=False)
    
    # print('promot ', myprompt)
    
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 1730123061183467594"
    }
    params={
       
            "contents": {
                "role": "user",
                "parts": {
                    "text": myprompt
                }
            },
            "safety_settings": {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            "generation_config": {
                "temperature": 0.9,
                "topP": 1.0,
                
            }
       
    }
    r = requests.post(GEMINI_URL, headers=headers, data=json.dumps(params))
    if r.status_code == 200:
        # print(r.text)
        try:
        # 把返回的数据拼接为答案
            obj = json.loads(r.text)
            answer = ''
        
            for i in obj:
                answer += i['candidates'][0]['content']['parts'][0]['text']
            arr = json.loads(answer)
            if(type(arr) == list):
                if(len(arr) == len(data)):
                    return arr
                else:
                    print('结果长度不一致，answer为',answer)
            else:
                print('结果不是列表，answer为',answer)
            
        except JSONDecodeError:
            print('json解析失败', answer)
        except Exception as e:
            print("出错了: ", e)
    else:
        print('请求出错了 ', r.text)
    return []   


def wenxin(data):
    myprompt = prompt.prompt + json.dumps([item['text'] for item in data], ensure_ascii=False)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 1730123061183467594",
        "security": "true"
    }
    params={
       
            "model": "ERNIE-Bot-4.0",
            "messages": [
                {
                    "role": "user",
                    "content": myprompt
                }
            ]
            # "stream": 'true'
       
    }
    r = requests.post(WENXIN_URL, headers=headers, data=json.dumps(params))
    if r.status_code == 200:
        try:
            obj = json.loads(r.text)
            if(obj['finish_reason'] == 'normal'):
                result = obj['result']
                subindex = result.find('\n')
                if(subindex >= 0):
                    # 文心一言可能有多余的解释，只取第一个\n之前的
                    result = result[0:subindex]
                # print('获取到的数据 ',result)
                answer = json.loads(result)
                if(type(answer) == list and len(answer) == len(data)):
                    return answer
                else:
                    print('结果长度不一致，answer为',answer)
            else:
                print('结束原因不是normal， 结束原因为', obj['finish_reason'], 'prompt为 ', myprompt)
        except JSONDecodeError:
            print('json解析失败', r.text)
        except Exception as e:
            print("出错了: ", e)
    else:
        print('请求出错了 ', r.text)
    return []  

def getByMonth(date, startIndex = 0):
    data = getdata.getDataByTime(date)[startIndex:]
    print('开始获取',date,'的数据')
    arr = util.chunks(data, ONCE_COUNT)
    answer = []
    index = 0
    for item in arr:
        # print('开始请求第', index, '组')
        # 睡眠5秒，避免请求频率过高
        index+=1
        time.sleep(5)
        result = gemini(item) if MODEL == 'gemini' else wenxin(item)
        if len(result) != 0:
            answer += result
        else:
            break
                 
    if(len(answer) != len(data)):
        print(date, ' 只获取到了部分数据，目前进度为：',len(answer)+startIndex)
    else:
        print('成功获取到', date, '的情绪数据，结束')
    for i in range(0,len(answer)):
        data[i]['emotion'] = answer[i]
    filePath = './结果文件/' + MODEL + os.sep + date + '.csv'
    # 如果startIndex为0，那么就意味着从0开始，如果文件存在，则需要删除
    if(startIndex == 0 and os.path.exists(filePath)):
        os.remove(filePath)
    util.writeCsv(filePath, data[0: len(answer)])
    
def getByYear(year):
    for month in ['03','04','05','06','07','08','09','10', '11','12']: 
        date = year + month + '01'
        print('开始获取', date, '的情绪数据')
        getByMonth(date)
        
    
if __name__ == "__main__":
    # 整年整年获取情绪指数
    # getByYear('2023')
    
    # 如果某几个月请求失败了，则重新请求这几个月，
    # for date in ['20231201']:
    #     getByMonth(date)
    
    # #对请求失败的月份，手动记录失败的index，传入startIndex为进度+1    
    getByMonth('20230801',21)
