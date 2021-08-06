import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "jpxgmn"])    # 配置可以在PyCharm实现调试，也可以在cmd中执行 scrapy crawl spider_name 来调试
