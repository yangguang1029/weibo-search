#http://baostock.com/baostock/index.php/%E5%85%AC%E5%BC%8F%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E8%AF%B4%E6%98%8E

# sz.399317	国证Ａ指
# sz.399106	深证综指
# sz.399107	深证A指
# sh.000001	上证指数	上证综合指数
# sh.000002	Ａ股指数	上证A股指数

# 股票的涨跌幅=( 现价-上一个交易日的收盘价)/上一个交易日的收盘价×100%。


import baostock as bs
import pandas as pd
from datetime import date,timedelta

YEAR = 2023


def getData(code, start_date, end_date):
    print('start getdata')
    rs = bs.query_history_k_data_plus(code ,"date,code,pctChg", start_date, end_date, frequency="d")
    # print('query_history_k_data_plus respond error_code:'+rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
    data_list = []
    while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    return data_list

def getDataByMonth():
    for month in range(1, 13):
        start_date = date(YEAR, month, 1).strftime('%Y-%m-%d')
        next_month = date(YEAR, month, 28) + timedelta(days=4)
        end_date = (next_month - timedelta(days=next_month.day)).strftime('%Y-%m-%d')
        # 国证A指
        data1 = getData('sz.399317', start_date, end_date)
        print('国证A指', data1)
        # 深证综指
        data2 = getData('sz.399106', start_date, end_date)
        print('深证综指', data2)
        # 深证A指
        data3 = getData('sz.399107', start_date, end_date)
        print('深证A指', data3)
        # 上证指数
        data4 = getData('sh.000001', start_date, end_date)
        print('上证指数', data4)
        # 上证A指
        data5 = getData('sh.000002', start_date, end_date)
        print('上证A指', data5)
        length = len(data1)
        if(len(data2) != length or len(data3) != length or len(data4) != length or len(data5) != length):
            print('数据长度不一致，请检查数据')
            return
        totalData = [['date', 'guoa', 'shenzong', 'shena', 'shangzheng', 'shanga']]
        for index in range(length):
            d1 = data1[index]
            totalData.append([d1[0], d1[2], data2[index][2], data3[index][2], data4[index][2], data5[index][2]])
        result = pd.DataFrame(totalData)
        result.to_csv('./data/'+start_date+ '.csv', index=False)
    

def main():
    lg = bs.login()
    getDataByMonth()
    # 登出系统
    # bs.logout()
   
    
    
    
    

    
if __name__ == '__main__':
    main()





# result = pd.DataFrame(data_list, columns=rs.fields)
# # 结果集输出到csv文件
# result.to_csv("./history_Index_k_data.csv", index=False)
# print(result)

