import os
from prompt import glm_prompt
import util
from zhipuai import ZhipuAI
import json
import getdata
from json import JSONDecodeError

# 智谱有时候比较容易返回多余信息，调整prompt也没用，但是稍微调整ONCE_COUNT后，再次尝试可能就好了

# https://open.bigmodel.cn/overview

api_key = "2eea1e60eb1e1ab5e334712c700b3329.lWcoBNc0oojNOOgW"


ONCE_COUNT=5
MODEL='zhipu'



def zhipu(data):
    client = ZhipuAI(api_key=api_key)
    pstr = glm_prompt
    for i in range(0, len(data)):
        text = data[i]['text']
        pstr = pstr + '文本：' + text
        if(i != len(data) - 1):
            pstr += '\n'
    # myprompt = glm_prompt + json.dumps([item['text'] for item in data], ensure_ascii=False)
    print(pstr)
    res = client.chat.completions.create(model="glm-3-turbo",
                top_p=0.7,
                temperature=0.9,
                stream=False,
                max_tokens=2000,
                messages=[ {
                    "role": "user",
                    "content": pstr
                }]
            )
    message = res.choices[0].message.content
    # message可能没有用[]包起来，需要增加
    if not message[0] == '[':
        message = '[' + message + ']'
    print('message ', message)
    try:
        result = json.loads(message)
        if(type(result) == list):
            if(len(result) == len(data)):
                return result
            else:
                print('结果长度不一致，answer为',message,' prompt长度为：',len(data))
                print('prompt为：',pstr)
        else:
            print('结果不是列表，answer为',message)
    except Exception as e:
        print("出错了: ", e)
    return []
        
        
    
    
def getByMonth(date, startIndex = 0):
    data = getdata.getDataByTime(date)[startIndex:]
    arr = util.chunks(data, ONCE_COUNT)
    answer = []
    index = 0
    for item in arr:
        # print('开始请求第', index, '组')
        index+=1
        result = zhipu(item)
        if len(result) != 0:
            answer += result
        else:
            break
                 
    if(len(answer) != len(data)):
        print(date, ' 只获取到了部分数据，目前进度为：',len(answer)+startIndex)
    else:
        print('成功获取到', date, '的情绪数据')
    for i in range(0,len(answer)):
        data[i]['emotion'] = answer[i]
    filePath = './结果文件/' + MODEL + os.sep + date + '.csv'
    # 如果startIndex为0，那么就意味着从0开始，如果文件存在，则需要删除
    if(startIndex == 0 and os.path.exists(filePath)):
        os.remove(filePath)
    util.writeCsv(filePath, data[0: len(answer)])
    
def getByYear(year):
    for month in ['02','03','04','05','06','07','08','09','10', '11','12']: 
        date = year + month + '01'
        print('开始获取', date, '的情绪数据')
        getByMonth(date)
        
    
if __name__ == "__main__":
    # 整年整年获取情绪指数
    # getByYear('2023')
    
    # 如果某几个月请求失败了，则重新请求这几个月，
    # for date in ['20231201']:
    #     getByMonth(date)
    
    #对请求失败的月份，手动记录失败的index，传入startIndex为进度+1    
    # getByMonth('20230301', 89)
    # getByMonth('20230401', 56)
    # getByMonth('20230501', 11)
    # getByMonth('20230601', 26)
    # getByMonth('20230701', 11)
    # getByMonth('20230801', 26)
    # getByMonth('20230901', 16)
    # getByMonth('20231001', 66)
    # getByMonth('20231101', 6)
    # getByMonth('20231201', 11)