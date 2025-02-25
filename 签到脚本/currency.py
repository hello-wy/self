import requests
import json

# 设置API的URL
url = "https://xcr.tratao.com/api/ver2/exchange/xcurrency/historys?base=JPY,USD,GBP,AUD&label=price&quote=CNY&range=1d"

# 设置请求头
headers = {
    "Host": "xcr.tratao.com",
    "appkey": "W6OecX1zIZjmYN3RpW7XJnoDBD7wWzJe",
    "language": "zh-Hans",
    "Accept": "*/*",
    "User-Agent": "XCWidgetExtension/6.0.6 (com.traveltao.ExchangeAssistant.XCWidget; build:1538; iOS 17.5.1) Alamofire/5.6.1",
    "Accept-Language": "zh-Hans-CN;q=1.0, en-CN;q=0.9, ja-CN;q=0.8",
    "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    "Connection": "keep-alive"
}

try:
    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        # 尝试解析JSON响应
        data = response.json()
        for currency in data:
            min = currency["ranges"]["price"]['min']
            max = currency["ranges"]["price"]['max']
            latest = currency["series"][-1]["price"]
            print(latest)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"发生错误: {e}")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    print(f"原始响应: {response.text}")