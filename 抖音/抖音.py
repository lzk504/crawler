from DrissionPage import ChromiumPage
import requests
import os
import re

headers = {
    'referer': 'https://www.douyin.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0'
}

# 打开浏览器
dp = ChromiumPage()

# 监听数据包特征
dp.listen.start('aweme/post')
# dp.get('https://www-hj.douyin.com/aweme/v1/web/aweme/post/')
dp.get(
    'https://www.douyin.com/user/MS4wLjABAAAADwJ7qUuqvFr5hSJ4mzvqt4tSvu8uVvPq5q_OGaPfzixvnyX7JQYhhXcNXQpqrEJa?from_tab_name=main')
# 等待数据包加载
r = dp.listen.wait()

# 获取响应数据
json_data = r.response.body

# 提取信息所在的列表
info_list = json_data['aweme_list']

os.mkdir('video')

for index in info_list:
    title = index['desc']
    video_id = index['aweme_id']
    video_url = index['video']['play_addr']['url_list'][0]
    video_name = re.sub(r'[\\/:*?"<>|\n\r%]', '_', title)
    print(video_name, video_id, video_url)
    video_content = requests.get(url=video_url, headers=headers).content
    with open(f'video\\{video_name}.mp4', 'wb') as f:
        f.write(video_content)
