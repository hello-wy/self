import requests
import json
import os
from datetime import datetime

# 从环境变量中获取 activity_no，如果未设置则使用默认值
ACTIVITY_NO = os.getenv("ACTIVITY_NO", "11111111111736501868255956070000")

# 用户数据
USER_DATA = [
    {
        "userName": "189",
        "x-lf-dxrisk-token": "673717491bK8AXWIlCFV4ozkSwiTp17C17enfG41",
        "x-lf-channel": "C2",
        "token": "eccf53dc3265447d8ffa893458fd0aab",
        "x-lf-usertoken": "eccf53dc3265447d8ffa893458fd0aab",
        "cookie": "acw_tc=b65cfd3d17316652614475806e2dc8b80d3ad4dd411e379521e78e280856d8",
        "x-lf-bu-code": "C20400",
        "x-lf-dxrisk-source": 5,
        # 为抽奖签到和抽奖添加额外的认证字段
        "lottery_cookie": "acw_tc=b65cfd3917402141521538562e6b64e1ff94903137922e70fc80d8afdc76f3",
        "authtoken": "cd97edb319294020a8bf0ae460c0eab5"
    }
]

# 全局变量
notify_msg = []
ck_status = True
do_flag = {"True": "✅", "False": "⛔️"}

# 日志输出
def log(msg):
    print(msg)
    notify_msg.append(msg)

# 发送请求的通用函数
def fetch(url, headers=None, method="GET", data=None):
    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        
        res = response.json()
        if "message" in res and ("登录已过期" in res["message"] or "用户未登录" in res["message"]):
            raise Exception("用户需要去登录")
        return res
    except Exception as e:
        log(f"⛔️ 请求发起失败！{str(e)}")
        return None

# 每日签到
def signin(user, activity_no):
    url = "https://gw2c-hw-open.longfor.com/lmarketing-task-api-mvc-prod/openapi/task/v1/signature/clock"
    headers = {
        "cookie": user["cookie"],
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x18003029) NetType/4G Language/zh_CN miniProgram/wx50282644351869da",
        "token": user["token"],
        "x-lf-dxrisk-token": user["x-lf-dxrisk-token"],
        "x-gaia-api-key": "c06753f1-3e68-437d-b592-b94656ea5517",
        "x-lf-bu-code": user["x-lf-bu-code"],
        "x-lf-channel": user["x-lf-channel"],
        "origin": "https://longzhu.longfor.com",
        "referer": "https://longzhu.longfor.com/",
        "x-lf-dxrisk-source": str(user["x-lf-dxrisk-source"]),
        "x-lf-usertoken": user["x-lf-usertoken"]
    }
    body = {
        "activity_no": activity_no
    }
    
    try:
        res = fetch(url, headers=headers, method="POST", data=body)
        if res:
            reward_num = res.get("data", {}).get("reward_info", [{}])[0].get("reward_num", 0) if res.get("data", {}).get("is_popup") == 1 else 0
            success = res.get("data", {}).get("is_popup") == 1
            log(f"{do_flag[str(success)]} { '每日签到: 成功, 获得' + str(reward_num) + '分' if success else '每日签到: 今日已签到'}")
            return reward_num
    except Exception as e:
        log(f"⛔️ 每日签到失败！{str(e)}")
    return 0

# 抽奖签到
def lottery_signin(user):
    url = "https://gw2c-hw-open.longfor.com/llt-gateway-prod/api/v1/activity/auth/lottery/click"
    headers = {
        "Host": "gw2c-hw-open.longfor.com",
        "Referer": "https://llt.longfor.com/",
        "Cookie": user["lottery_cookie"],
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 &MAIAWebKit_iOS_com.longfor.supera_1.10.2_202501191934_Default_3.2.4.2",
        "bucode": "L00602",
        "x-gaia-api-key": "2f9e3889-91d9-4684-8ff5-24d881438eaf",
        "channel": "L0",
        "Origin": "https://llt.longfor.com",
        "Sec-Fetch-Dest": "empty",
        "authtoken": user["authtoken"],
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Mode": "cors"
    }
    body = {
        "batch_no": "",
        "component_no": "CQ09S56M11J1RAEF",
        "activity_no": "AP258011N6GVNDNT"
    }
    
    try:
        res = fetch(url, headers=headers, method="POST", data=body)
        if res and res.get("code") == 0:  # 假设成功返回 code=0
            ticket_times = res.get("data", {}).get("ticket_times", 0)  # 假设返回抽奖次数在 data.ticket_times
            log(f"{do_flag['True']} 抽奖签到: 成功, 获得 {ticket_times} 次抽奖机会")
            return ticket_times
        else:
            log(f"{do_flag['False']} 抽奖签到: {res.get('message', '失败')}")
            return 0
    except Exception as e:
        log(f"⛔️ 抽奖签到失败！{str(e)}")
    return 0

# 抽奖
def lottery_clock(user):
    url = "https://gw2c-hw-open.longfor.com/llt-gateway-prod/api/v1/activity/auth/lottery/chance?component_no=CQ09S56M11J1RAEF&activity_no=AP258011N6GVNDNT"
    headers = {
        "Host": "gw2c-hw-open.longfor.com",
        "Accept": "application/json, text/plain, */*",
        "channel": "L0",
        "Sec-Fetch-Site": "same-site",
        "authtoken": user["authtoken"],
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "x-gaia-api-key": "2f9e3889-91d9-4684-8ff5-24d881438eaf",
        "Sec-Fetch-Mode": "cors",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": "https://llt.longfor.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 &MAIAWebKit_iOS_com.longfor.supera_1.10.2_202501191934_Default_3.2.4.2",
        "Referer": "https://llt.longfor.com/",
        "bucode": "L00602",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Sec-Fetch-Dest": "empty",
        "Cookie": user["lottery_cookie"]
    }
    
    try:
        res = fetch(url, headers=headers, method="GET")
        if res and res.get("code") == 0:  # 假设成功返回 code=0
            reward_desc = res.get("data", {}).get("desc", "未知奖励")  # 假设奖励描述在 data.desc
            log(f"{do_flag['True']} 抽奖成功, 获得 {reward_desc}")
        else:
            log(f"{do_flag['False']} 抽奖: {res.get('message', '未中奖')}")
    except Exception as e:
        log(f"⛔️ 抽奖失败！{str(e)}")

# 主程序
def main():
    global ck_status, notify_msg
    if not USER_DATA:
        raise Exception("找不到可用的帐户")
    
    log(f"⚙️ 发现 {len(USER_DATA)} 个帐户\n")
    for index, user in enumerate(USER_DATA):
        log("🚀 开始任务")
        notify_msg = []
        ck_status = True
        
        # 每日签到
        signin(user, ACTIVITY_NO)
        lottery_signin(user)
        lottery_clock(user)
        
        # 输出通知消息
        print("\n".join(notify_msg))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"⛔️ 脚本运行错误！{str(e)}")