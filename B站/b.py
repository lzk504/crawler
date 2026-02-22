from DrissionPage import ChromiumPage
from pprint import pprint
from datetime import datetime
import csv

f = open('data.csv', mode='w', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '标题',
    '分区',
    'bv',
    'up',
    '地区',
    '投币',
    '弹幕',
    '收藏',
    '点赞',
    '评论',
    '转发',
    '简介',
    '时间',
])
csv_writer.writeheader()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'cookie': "buvid3=3BEDCC68-7A85-94FC-E680-EB73E6EE74F158961infoc; b_nut=1734091558; _uuid=395657A2-3799-FD910-E4DF-9FCF34426AED60858infoc; rpdid=|(um|mm|)Yuu0J'u~JR|mulY|; enable_web_push=DISABLE; buvid_fp_plain=undefined; LIVE_BUVID=AUTO7617347906069655; hit-dyn-v2=1; is-2022-channel=1; enable_feed_channel=ENABLE; DedeUserID=17547056; DedeUserID__ckMd5=86230b801481f565; fingerprint=edb97f816287b76f07699a0240b4afc0; buvid_fp=edb97f816287b76f07699a0240b4afc0; header_theme_version=OPEN; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; theme-switch-show=SHOWED; CURRENT_QUALITY=80; home_feed_column=5; buvid4=A4DA3A11-3A8D-3394-81DB-0C928E2879A359935-024121312-n+KVs7JdRFw0e9vfJhvo1Q%3D%3D; browser_resolution=1536-730; timeMachine=0; PVID=1; ogv_device_support_hdr=0; bp_t_offset_17547056=1128972625230430208; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjE5NjI5NTYsImlhdCI6MTc2MTcwMzY5NiwicGx0IjotMX0.go_QoSt5KMuHe0hirH3fbmfL6sdbIjo6nzhqAvTn89w; bili_ticket_expires=1761962896; SESSDATA=14e06cbb%2C1777276762%2Cb12aa%2Aa2CjD-ohzklZxX8SXARrfAzuPWpypwyPEy1ZzNheh02DP0zZjfj7LdCfBoXFkmWKS67usSVjB5bWs5aWczQzdYeVNSNUhjbXppTVNZb0ZpbUhNLVZvTmhJclJWT1BwUlNyZklxVGo0YlpVRkNYN0ZTQjBWUVowSm11T0FoSWQ0U2NGcExhclNMU1BBIIEC; bili_jct=3ee96553e579238c6bc8b8c8ef66ea50; sid=8p5u6h2c; b_lsid=4EF1010F59_19A32CB4F9A; CURRENT_FNVAL=2000"
}

params = {
    'ps': '20',
    'pn': '1',
    'web_location': '333.934',
    'w_rid': '8071c2185850fbc961973e1bbb1b6857',
    'wts': '1761790224',
}

dp = ChromiumPage()

dp.listen.start('x/web-interface/popular')
dp.get('https://www.bilibili.com/v/popular/all?spm_id_from=333.1007.0.0')

r = dp.listen.wait()

json_data = r.response.body
video_info_list = json_data['data']['list']

for index in video_info_list:
    data = str(datetime.fromtimestamp(index['ctime']))
    dit = {
        '标题': index['title'],
        '分区': index['tname'],
        'bv': index['bvid'],
        'up': index['owner']['name'],
        '地区': index['pub_location'],
        '投币': index['stat']['coin'],
        '弹幕': index['stat']['danmaku'],
        '收藏': index['stat']['favorite'],
        '点赞': index['stat']['like'],
        '评论': index['stat']['reply'],
        '转发': index['stat']['share'],
        '简介': index['desc'],
        '时间': data,
    }
    csv_writer.writerow(dit)
