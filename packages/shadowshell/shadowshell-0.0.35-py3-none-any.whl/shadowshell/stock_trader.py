# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import akshare as ak
# import pandas as pd

# # 获取美股中概股实时行情
# df_us = ak.stock_us_spot_em()

# target_names = ["哔哩哔哩", "爱奇艺", "京东", "阿里巴巴", "蔚来", "小鹏汽车", "理想汽车"] 
# stocks = df_us[df_us["名称"].isin(target_names)]

# print(stocks[["代码", "名称","最新价","涨跌幅","涨跌额","开盘价","最高价","最低价","昨收价","总市值","市盈率","成交量","成交额","振幅","换手率"]])

# # df_us.to_csv("/Users/shadowwalker/Desktop/selected_stocks.csv", index=False, encoding="utf_8_sig")

