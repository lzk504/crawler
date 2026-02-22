import requests
import json
from pprint import pprint
import re
# 进度条模块
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Cookie': '_did=web_743906307532AB90; csrfToken=ymGbiaU0nOXtF56QMA-wIxqw; safety_id=AAIPYYowfrBB64Ru46dashHx; _did=web_743906307532AB90; webp_supported=%7B%22lossy%22%3Atrue%2C%22lossless%22%3Atrue%2C%22alpha%22%3Atrue%2C%22animation%22%3Atrue%7D; Hm_lvt_2af69bc2b378fb58ae04ed2a04257ed1=1760322707; HMACCOUNT=C2AF434F9BE2E2AD; lsv_js_player_v2_main=ca85g8; cur_req_id=31885556139162ED_self_1fc3d9fe49780b8406949811eaceed82; cur_group_id=31885556139162ED_self_1fc3d9fe49780b8406949811eaceed82_0; Hm_lpvt_2af69bc2b378fb58ae04ed2a04257ed1=1760322763',
    'Referer': 'https://www.acfun.cn/rank/list/?cid=-1&pcid=-1&range=DAY'
}

url = 'https://www.acfun.cn/v/ac47871799'

response = requests.get(url, headers=headers)

html = response.text
# print(html)
# 找到所有需要的数据->提取标题
title = re.findall('"title":"(.*?)"', html)[1]
# print(title)
# 视频信息
info = re.findall('window.pageInfo = window.videoInfo =(.*?);', html)[0]
# print(info)

json_data = json.loads(info)
# pprint(json_data)
m3u8_url = json.loads(json_data['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0]['url']
# pprint(m3u8_url)
# 获取 M3U8 播放列表文件内容
# M3U8 文件实际上是一个文本文件，其中包含了视频分成小片段（通常是 .ts 文件）的链接
m3u8 = requests.get(m3u8_url, headers=headers).text
# print(m3u8)
# 获取ts链接
ts_list = re.findall(',\n(.*?)\n#', m3u8)
# print(ts_list)
for ts in tqdm(ts_list):
    # 构建完整的ts链接地址
    ts_url = 'https://ali-safety-video.acfun.cn/mediacloud/acfun/acfun_video/' + ts
    ts_content = requests.get(ts_url, headers=headers).content
    with open('video\\' + title + '.mp4', mode='ab') as f:
        f.write(ts_content)
    print(ts)
