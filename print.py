import threading
import requests


def run():
    try:
        url = "https://print.lexiangsport.com/m/currency?src=addAdvertCurrency&time=1668585218297&appid=wxa520f15ccb7b2709&version=2.1.3&shopId=ck_-2b0kAphVIdaY-3d&schoolId=ck_-2b0kAphVIdaY-3d"
        payload = {}
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d38) NetType/4G Language/zh_CN',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Cookie': 'JSESSIONID=5E6DEE81218CA2E55E42841C359FBD1C',
            'Host': 'print.lexiangsport.com',
            'Referer': 'https://servicewechat.com/wxa520f15ccb7b2709/45/page-frame.html'
        }
        response = requests.get(url, headers=headers, data=payload)

        data = response.json()
        if data['code'] == 'ok':
            # 在修改共享变量之前获取锁
            lock.acquire()
            try:
                global total
                total += 1
                print("积分 +1")
            finally:
                lock.release()  # 释放锁

    except Exception as e:
        print("发生异常:", str(e))


def loop():
    for i in range(0, 1000):  # 增加循环次数
        run()


if __name__ == '__main__':
    total = 0
    lock = threading.Lock()  # 创建锁对象
    threads = []
    for _ in range(3):
        t = threading.Thread(target=loop)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()  # 等待所有线程完成

    print("总共获得积分:", total)