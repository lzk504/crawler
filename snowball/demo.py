import requests
from pprint import pprint
import pandas as pd

# 创建空列表
content_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Cookie': '921735024170902; device_id=aab9a630ab9c30833d50d2a7b0b6dc77; s=ak11r52esn; bid=98497db0c2975c172ebb473d330646f9_m82e4o2p; xq_a_token=b9c7e702181cba3ed732d5019efe2dfe2fb054b0; xqat=b9c7e702181cba3ed732d5019efe2dfe2fb054b0; xq_r_token=c1edaf05e1c6fdf8122671eced8049e8df8a4290; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTc2MTYxNDEwNywiY3RtIjoxNzYwMTUwNTMzMjA0LCJjaWQiOiJkOWQwbjRBWnVwIn0.oTziva9njmVIXIBCtKlpuglincT6-QZEnTzkqlktFChGFy2JLNb1VlInWnN96GD9Kvy-EaF2_Jn99lV9uyR_Vqv7YzvMxyEyGXlyasbFtlW2l1SQ2fhZtiTtftwOIMRYdgbA4zP_beTPj8ifn5jLxCwsVl16RiTGjJ8aLj3ZRe5R0LBsSyJq-5E5Vxg_tZPaQYOZLdnlkMeuyqiFiW2ohxoiismmmk4PT430tgE8YSh-vKbyFJ22j9RQFi1gaJp_GsYss-B86_Lnqa5jR8dUXfFvUKhOv6rJ4DHW_dINgeUPmw_Ef-N2vKMWjQdkxAMi1ODZLOJ46m2Zqx0K87m-nQ; u=921735024170902; Hm_lvt_1db88642e346389874251b5a1eded6e3=1759629719,1760150579; HMACCOUNT=C2AF434F9BE2E2AD; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1760151913; ssxmod_itna=1-Qq0x2iqWqYw8Ki7KitWDOKK0I=GIqDXDUqAQD2DIM47=GF7DCOY97B3nDBI=D7Qzirwv=K4rEHtDlxQeDZDGIdDqx0EiUDpn0K1ZzlGoq14uE70Kpe/0lC8GZWKNt04fyAA=8cCpdzGt2AGPWAw43i0GDfithD0aDmKDU=DqgjrYDeWaDCeDQxirDD4DADibb4D1pDDkD0_AAU3Lm4GWDm_ADWPDYxDr_RoDRPxD0xPmDQF3p9qDBcTnZirI/mLXi3CoovSD/4hAD7H3Dlp4mywAPH/gZDLXzq2632oDXaNDv28o23OR2W3OcfkP4KBxp70imeKiGim5kGD3BhzGKNe_NBG5nq1QGiQG4P6=ix57mb9AmDDAtb567blDH4hZRy/SyV4rqoGbl44O_CCAx97nnxiZ75yhND4qDe5Nmq605nhqjn4EGDD; ssxmod_itna2=1-Qq0x2iqWqYw8Ki7KitWDOKK0I=GIqDXDUqAQD2DIM47=GF7DCOY97B3nDBI=D7Qzirwv=K4rEHYDiP8Gt3=rD7PNQmSm4D/QB2DaPH=maxBxqU9ddqLqS1aH9uQCytdQEizkVjh=AuSFzq0iFzYP5H62FKR0OcOqzjp9WgccF/OD1qmPPbr0H2optHE0FWrp7UOATfoaOT3Ssz=81n1PxIRKCzgYjGEw7z6f5D_vLkKB6PkcCeIjtp9IhU0cAWADPk9Ak0nuOzQDbqABvDEv=G2Pk_ghhMeFFsCY7GXpHFpOEUnocb85qwRPL3=U7qwRxVrGzE40LsTk5Fr5Z7q8h8lh=kRPm2asftZqNs_4iddsRP1etGrwVEmO8pbOsVopqjaWT3WDHdCDibqL2WPitIOdx_F023WwtE2AzATcSpIhrFRPSDGWECe0GfgxXmfj4YvgAVrYXCI3GkZb=/2Pv6pcmaQL5YadK_t3RdY6ik6T3G7K=TUExnmDn3=E1qvZLXLtZZCbhtBR1VOWlfAXCqs8mKp53ud8Ch50WIesp1QXmE34sz8TdWmAo7KkCm/tchs6jts10PLGQFG0uAX3ysLWCzaEfRWh7IP=gGYeY5UOquhWBwg9T3ivt3BQ/iABE5GYb0p3KKGc1hzXCu2=YoehYoUXoqY5lB5=0oS7x3AZSvxgAZ4D'
}

for page in range(1, 168):
    url = f'https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size=30&order=desc&order_by=percent&market=CN&type=sh_sz'

    response = requests.get(url, headers=headers)
    json_data = response.json()
    # print(json_data['data']['list'])

    for index in json_data['data']['list']:
        # pprint(index)
        dit = {
            '代码': index['symbol'],
            '名称': index['name'],
            '现价': index['current'],
            '涨跌额': index['chg'],
            '涨跌幅': index['percent'],
            '年初至今': index['current_year_percent'],
            '成交量': index['volume'],
            '成交额': index['amount'],
            '换手率': index['turnover_rate'],
            '市盈率': index['pe_ttm'],
            '股息率': index['dividend_yield'],
            '市值': index['market_capital'],
        }
        content_list.append(dit)

    pd.DataFrame(content_list).to_excel('stock.xlsx', index=False)
