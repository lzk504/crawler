import requests
import pandas as pd
import re

content_list = []

headers = {
    'referer': 'https://fund.eastmoney.com/data/fundranking.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}
for page in range(1, 371):
    url = f'https://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=1nzf&st=desc&sd=2024-10-11&ed=2025-10-11&qdii=&tabSubtype=,,,,,&pi={page}&pn=50&dx=1&v=0.09705250525400444'
    resp = requests.get(url, headers=headers)
    data = resp.text
    funds = re.findall('datas:(.*?).allRecords', data)[0]
    fund_list = eval(funds)
    for i, entry in enumerate(fund_list):
        fields = entry.split(',')
        dit = {
            "基金代码": fields[0],
            "基金名称": fields[1],
            "简称": fields[2],
            "日期": fields[3],
            "单位净值": fields[4],
            "累计净值": fields[5],
            "日增长率": fields[6],
            "近1周": fields[7],
            "近1月": fields[8],
            "近3月": fields[9],
            "近6月": fields[10],
            "近1年": fields[11],
            "近2年": fields[12],
            "近3年": fields[13],
            "今年来": fields[14],
            "成立以来": fields[15],
            "成立日期": fields[16],
            "手续费": fields[19],
        }
        # print(dit)
        content_list.append(dit)
    pd.DataFrame(content_list).to_excel('fund.xlsx', index=False)
