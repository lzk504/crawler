from DrissionPage import ChromiumPage
import parsel
import csv

# 创建文件对象
f = open('data.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '标题',
    '价格',
    '项目名称',
    '户型',
    '单价',
    '面积',
    '朝向',
    '楼层',
    '年份',
    '区域',
    '商圈',
    '门牌号',
])
csv_writer.writeheader()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
}

dp = ChromiumPage()

dp.headers = headers
for page in range(1, 11):
    dp.get(f"https://nb.anjuke.com/sale/p{page}")
    dp.wait(1)
    # 获取数据源
    html = dp.html
    # 解析数据
    selector = parsel.Selector(html)
    divs = selector.css('.property-content')

    for div in divs:
        title = div.css('.property-content-title-name::text').get()
        # div.css('.property-content-description::attr(title)').get()
        price = div.css('.property-price-total-num::text').get()
        info_name = div.css('.property-content-info-comm-name::text').get()
        # 把列表合并为字符串
        house_type = ''.join(div.css('.property-content-info-attribute span::text').getall())
        average_price = div.css('.property-price-average::text').get()
        info = div.css('.property-content-info-text::text').getall()
        info = [i.strip() for i in info if i != ' ']
        if len(info) == 4:
            fool = info[2]
            data = info[3].replace('年建造', '')
        elif len(info) == 3 and '年建造' in info[-1]:
            fool = '未知'
            data = info[3].replace('年建造', '')
        elif len(info) == 3 and '层' in info[-1]:
            fool = '未知'
            data = '未知'
        else:
            fool = '未知'
            data = '未知'
        address = div.css('.property-content-info-comm-address span ::text').getall()
        dit = {
            '标题': title,
            '价格': price,
            '项目名称': info_name,
            '户型': house_type,
            '单价': average_price.strip().replace('元/㎡', ''),
            '面积': info[0],
            '朝向': info[1],
            '楼层': fool,
            '年份': data,
            '区域': address[0],
            '商圈': address[1],
            '门牌号': address[2],
        }
        print(dit)
        csv_writer.writerow(dit)
