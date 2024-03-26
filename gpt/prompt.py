# 角色
# 思维链
# 范例
# 避免出错，如果无法判断，则给出-2

prompt = '''你是一名金融领域的专家，你需要根据文本内容判断这段文本所传达出来的情绪是积极、消极还是中立，如果情绪是积极，则结果为1，如果情绪为消极，则结果为-1，如果情绪为中立，则结果为0，如果无法判断，则结果为-2。以下是四个范例：

文本：大家要对股市有信心，相信形式会越来越好的
结果：情绪为积极，因此结果为1

文本：再也不相信股市了，不会再买了
结果：情绪为消极，因此结果为-1

文本：大家觉得今天股市会上涨还是下跌呢？
结果：情绪为中立，因此结果为0

文本：今天心情不好，小房子的微博视频
结果：与金融情绪无关，无法判断，因此结果为-2

接下来给出一个json数组，每个元素的text为文本内容，请判断其情绪，得到情绪结果数字，也就是1、-1、0、-2其中之一，将所有结果以数组形式返回。

接下来是你要根据文本判断情绪：
'''