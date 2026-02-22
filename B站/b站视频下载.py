from email.mime import audio
import re
import requests
import subprocess
import os
from pprint import pprint
import time

"""
首先获取视频id参数：https://api.bilibili.com/x/web-interface/wbi/view/detail
在获取视频链接和音频链接 数据包：https://api.bilibili.com/x/player/wbi/playurl
目标获取视频信息包含视频和音频

"""

# 完整的请求头配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Referer': 'https://www.bilibili.com/',
    'Origin': 'https://www.bilibili.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    # ⬇️ 在这里填写你的 Cookie ⬇️
    'Cookie': "buvid3=5A559D33-BB42-6DEA-BAF3-1FE8D4359DD837533infoc; b_nut=1770528537; _uuid=A816AEDA-4F65-C33F-310B8-936378C59310939084infoc; CURRENT_QUALITY=0; buvid4=A4DA3A11-3A8D-3394-81DB-0C928E2879A359935-024121312-n+KVs7JdRFw0e9vfJhvo1Q%3D%3D; buvid_fp=c7de73fa3429290550a3bac5bdd90e8b; rpdid=|(u|umu||uJ|0J'u~~|lk)lJ); home_feed_column=5; SESSDATA=c0c02ac2%2C1786173165%2C5b8d5%2A21CjCQIwX5VnX2YYySIzKB5RYfFi6wCdQ-U5oHa2R0YNgyEeDdWfisDXPlQCc-JZtY2A4SVjVUVVJRazlpbTktQm1LcWxLQlp4VXpERkN5M3l4ZTVDaS02QW51LUF3OGE4ZDdlaEpWQTdQdXZQRmNrUG85X3JCQmpRd2s5Qm1LeFlWdnAwVV9qVnR3IIEC; bili_jct=10b27b10a1776db1bc500901bfa4fead; DedeUserID=17547056; DedeUserID__ckMd5=86230b801481f565; sid=74t27bk6; theme-tip-show=SHOWED; hit-dyn-v2=1; LIVE_BUVID=AUTO3217707022111354; theme-avatar-tip-show=SHOWED; PVID=2; browser_resolution=1920-945; bp_t_offset_17547056=1172123294069948416; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzIwMDM4NDAsImlhdCI6MTc3MTc0NDU4MCwicGx0IjotMX0.OcUNUtwq9UqbMzgKuGEobdxb14LI208YzUIKCQP8Cbc; bili_ticket_expires=1772003780; CURRENT_FNVAL=4048; b_lsid=33D07140_19C84361506" 
}

# 使用 session 保持连接和 cookie
session = requests.Session()
session.headers.update(headers)
# 禁用 SSL 验证（B站有时候SSL证书验证可能有问题）
session.verify = False
# 添加重试机制
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

# 请求链接
url = input("请输入https://api.bilibili.com/x/web-interface/wbi/view/detail的链接url：")
print("正在请求数据，请稍候...")

try:
    # 添加超时和重试
    response = session.get(url=url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
    print("\n解决方案：")
    print("1. 更新 Cookie - 在浏览器中复制最新的 Cookie")
    print("2. 检查网络连接")
    print("3. 稍后重试（B站可能有频率限制）")
    exit()


json_data = response.json()

# 检查API是否返回成功
if json_data.get('code') != 0:
    print(f"API 错误: {json_data.get('message', '未知错误')}")
    print("建议：")
    print("1. Cookie 可能已过期，需要更新")
    print("2. 请在浏览器中登录 https://www.bilibili.com")
    print("3. 打开开发者工具 (F12) -> Network，刷新后找到 view/detail 请求")
    print("4. 复制完整的 Cookie 并替换代码中的 Cookie")
    exit()

# 解析数据-->通过字典取值获取内容
try:
    pages = json_data['data']['View']['pages']
except KeyError as e:
    print(f"数据解析错误: 找不到 {e}")
    print("响应数据:", json_data)
    exit()

print(f"成功获取 {len(pages)} 个视频分P")
pprint(pages)

# 创建 video 目录（如果不存在）
if not os.path.exists('video'):
    os.makedirs('video')
    print("已创建 video 目录")

for page in pages:
    cid = page['cid']
    title = page['part']
    # 第二次请求
    link = input('请输入https://api.bilibili.com/x/player/wbi/playurl的链接：')
    link_data = requests.get(url=link, headers=headers).json()
    video_url = link_data['data']['dash']['video'][0]['baseUrl']
    audio_url = link_data['data']['dash']['audio'][0]['baseUrl']
    
    print(f"正在下载视频：{title}")
    video_content = requests.get(video_url, headers=headers).content
    audio_content = requests.get(audio_url, headers=headers).content

    # 清理文件名中的非法字符
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
    
    # 使用 os.path.join 构建路径（跨平台兼容）
    mp4_path = os.path.join('video', f'{safe_title}.mp4')
    mp3_path = os.path.join('video', f'{safe_title}.mp3')
    output_path = os.path.join('video', f'{safe_title}_final.mp4')
    
    # 保存视频和音频文件
    print(f"保存视频到: {mp4_path}")
    with open(mp4_path, mode='wb') as f:
        f.write(video_content)
    print(f"保存音频到: {mp3_path}")
    with open(mp3_path, mode='wb') as f:
        f.write(audio_content)
    
    # 验证文件是否存在
    if not os.path.exists(mp4_path):
        print(f"错误：视频文件保存失败 {mp4_path}")
        continue
    if not os.path.exists(mp3_path):
        print(f"错误：音频文件保存失败 {mp3_path}")
        continue
    
    print(f"文件大小 - 视频: {os.path.getsize(mp4_path)} 字节, 音频: {os.path.getsize(mp3_path)} 字节")
    
    # 使用正确的 FFmpeg 命令
    cmd = f'ffmpeg -i "{mp4_path}" -i "{mp3_path}" -c:v copy -c:a aac -strict experimental "{output_path}"'
    print(f"执行命令: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg 错误: {result.stderr}")
        else:
            print(f"合并成功: {output_path}")
            # 删除临时文件
            os.remove(mp4_path)
            os.remove(mp3_path)
            print(f"已删除临时文件")
    except Exception as e:
        print(f"执行 FFmpeg 失败: {e}")
    
    break
