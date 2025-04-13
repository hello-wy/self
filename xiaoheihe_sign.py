import requests
import time
import json

def xiaoheihe_sign():
    # 请求URL和参数
    base_url = "https://api.xiaoheihe.cn/task/sign_v3/sign"
    
    # 请求参数
    params = {
        "os_type": "iOS",
        "hkey": "53b8db52",
        "dw": "393",
        "device_id": "40F1EC9E-D257-4318-BD45-E6E983B1E154",
        "x_client_type": "mobile",
        "device_info": "iPhone15Pro",
        "heybox_id": "36969681",
        "os_version": "18.4",
        "nonce": "p7t54Mlaxdc9YgKJ21so6AmcH1AFpKAr",  # 这个可能需要动态生成
        "version": "1.3.341",
        "x_os_type": "iOS",
        "lang": "zh-cn",
        "x_app": "heybox",
        "_time": str(int(time.time())),  # 使用当前时间替代原请求中的时间戳
        "time_zone": "Asia/Shanghai"
    }
    
    # 请求头
    headers = {
        "Host": "api.xiaoheihe.cn",
        "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "baggage": "sentry-environment=production,sentry-public_key=cd2481795348588c5ea1fe1284a27c0b,sentry-release=com.max.xiaoheihe@1.3.341+1309,sentry-trace_id=2dd9d60b45554879928deafa3afdde76",
        "Cookie": "hkey=37f51948b40da18f8d9a4435d57bc444;x_xhh_tokenid=BSwZMHba4axl+DzjNl6SgHaUAI/h+DFFDzftWcpnunT7UdncDJoL2jJeTRodNUZwMiv9QqJ98okxoP/6x8lbwmQ==;pkey=MTczMjM3Njk3Ni44NV8zNjk2OTY4MWh2dnd6aWFxbHJxd2dlcmI__",
        "User-Agent": "xiaoheihe/1.3.341 (com.max.xiaoheihe; build:1309; iOS 18.4.0) Alamofire/5.9.0",
        "Accept-Language": "zh-Hans-CN;q=1.0, en-CN;q=0.9, ja-CN;q=0.8",
        "Referer": "http://api.maxjia.com/",
        "sentry-trace": "2dd9d60b45554879928deafa3afdde76-800daa762e364271-0"
    }
    
    try:
        # 发送GET请求
        response = requests.get(base_url, params=params, headers=headers)
        
        # 打印响应状态码和内容
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 解析JSON响应
        result = response.json()
        
        # 判断签到是否成功
        if result.get("status") == "ok":
            print("签到成功!")
        else:
            print(f"签到失败: {result.get('msg', '未知错误')}")
            
        return result
        
    except Exception as e:
        print(f"请求出错: {str(e)}")
        return None

# 执行签到
if __name__ == "__main__":
    print("开始执行小黑盒签到...")
    result = xiaoheihe_sign()
    print("签到完成")