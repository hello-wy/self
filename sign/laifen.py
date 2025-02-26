import requests
import json

# 请求 URL
url = "https://h5.youzan.com/wscump/checkin/checkinV2.json?checkinId=1883040&app_id=wx42413e034aafdda0&kdt_id=99207827&access_token=34a43346de678e3ea729b2c6367db4"

# 请求头
headers = {
    "Host": "h5.youzan.com",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Extra-Data": json.dumps({
        "is_weapp": 1,
        "sid": "YZ1342611332125720576YZ4PDikEAT",
        "version": "2.196.6.102",
        "client": "weapp",
        "bizEnv": "wsc",
        "uuid": "Wu8Ozo4POdROUgv1740145025937",
        "ftime": 1740145025934
    }),
    "Accept-Encoding": "gzip,compress,br,deflate",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003137) NetType/4G Language/zh_CN",
    "Referer": "https://servicewechat.com/wx42413e034aafdda0/51/page-frame.html"
}

# 发送 GET 请求
try:
    response = requests.get(url, headers=headers)
    
    # 检查响应状态码
    if response.status_code == 200:
        # 尝试解析 JSON 响应
        try:
            result = response.json()
            print("请求成功，返回结果：")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except json.JSONDecodeError:
            print("请求成功，但返回内容不是有效的 JSON：")
            print(response.text)
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"请求发生错误：{e}")
