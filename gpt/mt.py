import requests
import json
import getdata
import prompt
import util
import time
from json import JSONDecodeError


GEMINI_URL = "https://aigc.sankuai.com/v1/google/models/gemini-pro:streamGenerateContent"
# 拆分成每ONCE_COUNT条数据一次，避免context过长
ONCE_COUNT = 10

def gemini(data):
    
    myprompt = prompt.prompt + json.dumps(data, ensure_ascii=False)
    
    
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
        try:
        # 把返回的数据拼接为答案
            obj = json.loads(r.text)
            answer = ''
        
            for i in obj:
                answer += i['candidates'][0]['content']['parts'][0]['text']
            arr = json.loads(answer)
            if type(arr) == list:
                return arr      
            else:
                print('请求出错了 ', r.text)
        except JSONDecodeError:
            print('json解析失败', answer)
        except Exception as e:
            print("出错了: ", e)
    return []  

    
def getByYear(year):
    for month in ['03','06','09','10','11','12']: 
        date = year + month + '01'
        
        data = getdata.getDataByTime(date)
        arr = util.chunks(data, ONCE_COUNT)
        answer = []
        for item in arr:
            # 睡眠5秒，避免请求频率过高
            time.sleep(5)
            answer = answer+ gemini(item)
        
        if(len(answer) != len(data)):
            print(date, '结果长度不一致，请重试')
            continue
        print('成功获取到', date, '的情绪数据')
        for i in range(0,len(data)):
            data[i]['emotion'] = answer[i]
        util.writeCsv(date, data)
    
if __name__ == "__main__":
    # 整年整年获取情绪指数
    getByYear('2023')