#-*-coding:utf-8
import os
import pandas as pd

# 有的数据因为带了敏感信息，导致无法获取的，需要进行手动加工，例如'qingang外长被免'

path1 = '../结果文件/中国股市/'
path2 = '../结果文件/A股/'


def getDataByTime(time):
    fileName1 = path1 + time + '/中国股市.csv'
    df1 = pd.DataFrame([])
    if os.path.exists(fileName1):
        df1 = pd.DataFrame(pd.read_csv(fileName1, encoding='utf-8'))
        
    fileName2 = path2 + time + '/A股.csv'
    df2 = pd.DataFrame([])
    if os.path.exists(fileName2):
        df2 = pd.DataFrame(pd.read_csv(fileName2, encoding='utf-8'))
    # 合并并去掉重复
    merged = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    
    data = merged[['id','微博正文', '发布时间']].values
    
    array = []
    for i in range(0,len(data)): 
        item = data[i]
        time = item[2]
        date=time.split(' ')[0]
            
        array.append({
            "id": item[0],
            "text": item[1],
            "date": date
        })
    
    return array
    