import csv
import os


def writeCsv(time, data):
    filePath = './结果文件/' + time + '.csv'
    if not os.path.isfile(filePath):
        is_first_write = 1
    else:
        is_first_write = 0
    with open(filePath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_first_write:
            header = ['id', 'text', 'date', 'emotion']
            writer.writerow(header)
        for item in data:
            writer.writerow([item['id'],item['text'],item['date'],item['emotion']])
            

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]