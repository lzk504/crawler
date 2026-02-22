import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Content-Type': 'text/plain',
    "Referer": "http://192.168.100.231:8080/StormWeb/report.do?action=showReportListDo&userId=df7fb716-c7f4-4947-9c87-52a2a83b8461&isNewPage=true&unitTypeId=1"
}


def get_table_info():
    url = "http://192.168.100.231:8080/StormWeb/dwr/call/plaincall/reportAjax.getReportDeviceReListInfo.dwr"
    data = {
        "callCount": "1",
        "windowName": "c0 - param0",
        "c0-scriptName": "reportAjax",
        "c0-methodName": "getReportDeviceReListInfo",
        "c0-id": "0",
        "c0-e1": "string:df7fb716-c7f4-4947-9c87-52a2a83b8461",
        "c0-e2": "string:-1",
        "c0-e3": "string:1",
        "c0-e4": "string:0",
        "c0-e5": "string:0",
        "c0-e6": "string:0",
        "c0-e7": "string:-1",
        "c0-e8": "string:-1",
        "c0-e9": "string:-1",
        "c0-e10": "string",
        "c0-e11": "number:0",
        "c0-e12": "number:20",
        "c0-param0": "Object_Object:{userId:reference:c0-e1, unitId:reference:c0-e2, unitTypeId:reference:c0-e3, reportType:reference:c0-e4, reportOwner:reference:c0-e5, reportCycle:reference:c0-e6, timeType:reference:c0-e7, startTime:reference:c0-e8, endTime:reference:c0-e9, keyword:reference:c0-e10, start:reference:c0-e11, limit:reference:c0-e12}",
        "batchId": "1",
        "instanceId": "0",
        "page": "%2FStormWeb%2Freport.do%3Faction%3DshowReportListDo%26userId%3Ddf7fb716-c7f4-4947-9c87-52a2a83b8461%26isNewPage%3Dtrue%26unitTypeId%3D1",
        "scriptSessionId": "ItpsuDLpYF7kEOTvg0h$6r0$*Dp/exFo$Dp-HEkMaJMUi",
    }
    response = requests.post(url=url, headers=headers).content
    print(response)


def get_table(key):
    url = "http://192.168.100.231:8080/StormWeb/report.do"
    params = {
        "action": "exportReport",
        "userId": "df7fb716-c7f4-4947-9c87-52a2a83b8461",
        "reportId": key,
        "exportType": 2
    }
    if not os.path.exists("网强list"):
        os.mkdir("网强list")
    with open("网强list/", '123', '.xlsx', "wb") as f:
        f.write(requests.get(url=url, headers=headers, params=params).content)
        print("下载完成")


if __name__ == '__main__':
    get_table("4028e467938f2fed0199fda74cef1cbf")
