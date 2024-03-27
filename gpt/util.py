import csv
import os


def writeCsv(filePath, data):
    if not os.path.isfile(filePath):
        is_first_write = 1
    else:
        is_first_write = 0
    with open(filePath, 'w' if is_first_write else 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        print('开始写文件', filePath)
        if is_first_write:
            header = ['id', 'text', 'date', 'emotion']
            writer.writerow(header)
        for item in data:
            writer.writerow([item['id'],item['text'],item['date'],item['emotion']])
            

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]