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


    

