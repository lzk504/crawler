import pprint

import requests
import re
import execjs
import os
from pprint import pprint
from prettytable import PrettyTable
from datetime import datetime
import csv

# 请求头
headers = {
    'Cookie': 'NMTID=00OBAwwLHdb4qTdVknxlW5jjAigov4AAAGT2J-TgQ; nts_mail_user=13819870687@163.com:-1:1; _iuqxldmzr_=32; _ntes_nnid=723302c7eb26f0728f9d0e71ffb7ad28,1747037777197; _ntes_nuid=723302c7eb26f0728f9d0e71ffb7ad28; WEVNSM=1.0.0; WNMCID=vtzbpu.1747037778309.01.0; WM_TID=akdMC6jPtpNEEQVBEReSbPRO1hXsuaoy; __snaker__id=1PyiCgpcrOmnHixP; sDeviceId=YD-iuGWjnCTuvFBBwFQQRODKKBLx0S%2BJvwN; ntes_utid=tid._.3ccn6Vh88spERgBFEEKGOaBbxgCrKXz0._.0; ntes_kaola_ad=1; vinfo_n_f_l_n3=29e1bc81405a6c9c.1.0.1760165290724.0.1760165320480; NTES_P_UTID=V3NZ1J5EfvZ1eH4SdoufwpedOR73uPtE|1760323164; __csrf=4c45b4c79bef4945cfa6a94982e8d492; WM_NI=%2BG8Q5Lz6Jc53ZGVrs%2FQyGi9CItm3rRgTvEhdFnO7OGLHv2EK%2Fuzw5uf8kTubMGf3Kd8%2Bz%2FVAY2nYyV2w%2FdSoU8wh8RufM6RMLQrPE6uAamNMdnVe9zk7Uf3J687rQ0hTUHo%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8fef4ababa8a92ed6e8abc8fb7c84b968b9e82db74f5ad0090ee4b83b496d9c22af0fea7c3b92ae999f8b2b848baea8684b8399a999a93f22593a7898abc498baca3d4f15aa58cbaa6eb7086b281d8ce4d9098bad3c841edabb698b87fa6e8a5b5f86a8f99aad4ca70fcf5b6d0d54b9beea2bafc5ef2a9e185d26597e8b989bb5ab7ba83d7d147908fbeb1c83eb79faf8ecd47a8b29a86bc72a9e99b87b242f6e8f993d43cac8c9ba9ee37e2a3; gdxidpyhxdE=CXJkzlqH5oSzga0fiymOui%2Ba%2B%2Fcc1et%2FZzAClBvlk%2FKLSqbf9V2Y3abcCvD4Z4mU4qHZaM12tgjn3vbvxrdAGWmr%5CwR3atBJQ0BM6xsAcq%5C3dK5kAfYIvUk6zftCu%2Ff9rmkBLrMk%5ChyBolaHOfcrU9fgk%5CDHf6ASKB%2Fex9AD%2BZ88O%2FWI%3A1760752430061; MUSIC_U=003EBDA10B5C91FE92393CB8E4C181122BCB115A8AFB69B9755442F03CD3D0DC780105E7CCC3DE1A58C42CE8458B453BA0A1EE171C52C86EAB4A22CDC02D2507F8C65D3175F9BFE5B1E527B69D404208C58661F287185958AEBE0EA29BFEE9C6BAB040A877FBCE017A147A5208A7C7717BBC861C8A8D835A86F2F597917D5AE5CA9487138D5DDED4118F6BD5312654586994BA43791257708E561BFD220324B91142381E1A105B73278EDB646D5230B07858EBA553716982BBD530DD178134CA1029C05F7FB2B9487B532EE72EC99A4AC2AACCA14F77C6418B4D61E6286F3B3DF8421D4452A02E7E49E02406A4B11AC635EE27FA6C54B7FD1EAD1A3A1CF5FA41AB79FAC1DEB53CE61F51E54E4C544B7787EA5B613A674B8676ACD29FCFAA70F852CC01B3FB66E9A56DDBE25266821A0ED5427B1112267F0F33630185B74E6B93A658DFB29052258259E3A8DF5583862C7E06F3905AC7B9B032283AFA45CC141775A8A63A25AC6C033ABD4EFDC0C005054D66CE78CC44746E05E29793DF77ED7279917D3A62106F297B39D1E2EC6562CB6A; __csrf=7a6607683a963ce5797a40eb744c3289; JSESSIONID-WYYY=RMWcrtAZRE8aueda07sSjWqvvjrp04iR0exhWeeyidRkPdb43X%2FaemVhUdWRzn6kjEh%2FzhWZ%2BS%2BKNrDmadVusYdiFMPdS8cqeTcWJxk9%2BG1sWG1%2F7UX6w6gmIhVc%5CczYbTdBZeh1MWO6D2dNuoZPhDOrnvfsE4rNle4AM27OqiksmTaX%3A1760755401871; playerid=45868307',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}


# 编译js代码
def get_js_code():
    js_code = execjs.compile(open('wyy.js', encoding='utf-8').read())
    return js_code


# 获取歌曲信息
def get_music_info():
    url = "https://music.163.com/artist?id=44266"
    html = requests.get(url, headers=headers).text
    music_info = re.findall('<a href="/song\?id=(\d+)">(.*?)</a>', html)
    return music_info


def get_music_url(music_id):
    url = "https://music.163.com/weapi/song/enhance/player/url/v1"
    params = {
        "csrf_token": "4c45b4c79bef4945cfa6a94982e8d492"
    }
    # 获取加密参数
    i1x = {
        "ids": f"[{music_id}]",
        "level": "exhigh",
        "encodeType": "aac",
        "csrf_token": "4c45b4c79bef4945cfa6a94982e8d492"
    }
    data = get_js_code().call('get_data', i1x)
    # 发送请求
    json_data = requests.post(url=url, params=params, data=data, headers=headers).json()
    # 提取歌曲链接地址
    music_url = json_data['data'][0]['url']
    return music_url


# 保存数据
def save(title, music_url):
    if not os.path.exists("singer_list"):
        os.mkdir('singer_list')
    new_title = re.sub(r'[\\/*?"<>|]', '', title)
    with open('singer_list/' + new_title + '.mp3', 'wb') as f:
        f.write(requests.get(url=music_url).content)
        print(f"{title},下载完成")


# 搜索
def search(keyword):
    url = "https://music.163.com/weapi/cloudsearch/get/web"
    params = {
        "csrf_token": "4c45b4c79bef4945cfa6a94982e8d492"
    }
    i1x = {
        "hlpretag": "<span class=\"s-fc7\">",
        "hlposttag": "</span>",
        "id": "44266",
        "s": keyword,
        "type": "1",
        "offset": "0",
        "total": "true",
        "limit": "30",
        "csrf_token": "4c45b4c79bef4945cfa6a94982e8d492"
    }
    data = get_js_code().call('get_data', i1x)
    json_data = requests.post(url=url, params=params, data=data, headers=headers).json()
    tb = PrettyTable()
    tb.field_names = ['序号', '歌名', '歌手', '专辑']
    page = 1
    search_info = []
    for index in json_data['result']['songs']:
        dit = {
            'id': index['id'],
            'title': index['name'],
        }

        # 添加id到空列表中
        search_info.append(dit)
        name = '/'.join([i['name'] for i in index['ar']])

        tb.add_row([page, index['name'], name, index['al']['name']])
        page += 1
    print(tb)
    return search_info


# 获取评论
def get_comment(music_id, page, cursor):
    url = "https://music.163.com/weapi/comment/resource/comments/get"
    params = {
        "csrf_token": "4c45b4c79bef4945cfa6a94982e8d492"
    }
    i3x = {
        "rid": f"R_SO_4_{music_id}",
        "threadId": f"R_SO_4_{music_id}",
        "pageNo": page,
        "pageSize": "50",
        "cursor": cursor,
        "offset": "0",
        "orderType": "1",
        "csrf_token": "4c45b4c79bef4945cfa6a94982e8d492"
    }
    comments = []
    data = get_js_code().call('get_data', i3x)
    json_data = requests.post(url=url, params=params, data=data, headers=headers).json()
    for index in json_data['data']['comments']:
        # 提取评论时间戳
        c_time = index['time']
        # 去掉毫秒
        time = str(datetime.fromtimestamp(int(str(c_time)[:-3])))

        dit = {
            '昵称': index['user']['nickname'],
            '评论': index['content'],
            'ip': index['ipLocation']['location'],
            '创建时间': time
        }
        comments.append(dit)
    # 提取下一页参数
    cursor = json_data['data']['cursor']
    return comments, cursor


def main():
    print("""
            请选择：
            1，泰勒斯威夫特热歌榜单采集
            2，搜索采集
            3,  采集歌曲评论
        """)
    choose = input('请输入1或2或3')
    if choose == '1':
        music_info = get_music_info()
        for music_id, title in music_info:
            music_url = get_music_url(music_id)
            save(title, music_url)
    elif choose == '2':
        keyword = input(" 请输入搜索内容:")
        search_info = search(keyword)
        num = input("请输入歌曲序号:")
        music_id = search_info[int(num) - 1]['id']
        title = search_info[int(num) - 1]['title']
        music_url = get_music_url(music_id)
        save(title, music_url)
    elif choose == '3':
        keyword = input(" 请输入搜索内容:")
        search_info = search(keyword)
        num = input("请输入歌曲序号:")
        music_id = search_info[int(num) - 1]['id']
        title = search_info[int(num) - 1]['title']
        page_num = input("请入想要采集的评论页数")
        cursor = "-1"
        csv_file = open(f'{title}.csv', mode='w', encoding='utf-8-sig', newline='')
        # 定义CSV文件的列名（表头）
        # 创建一个DictWriter对象，它能将字典直接写入CSV行
        csv_writer = csv.DictWriter(csv_file, fieldnames=[
            '昵称',
            '评论',
            'ip',
            '创建时间'
        ])
        # 写入表头
        csv_writer.writeheader()
        for page_num in range(1, int(page_num) + 1):
            print(f"正在采集第{page_num}页数据")
            comments, cursor = get_comment(music_id, page_num, cursor)
            for comment in comments:
                csv_writer.writerow(comment)
    else:
        print("输入有误请重新输入")


if __name__ == '__main__':
    # music_url = get_music_url("1301736461")
    # title = '爱错'
    # save(title, music_url)
    # comments = get_comment("1301736461", 1, "-1")
    main()
