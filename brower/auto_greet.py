import os
from playwright.sync_api import sync_playwright, TimeoutError
import time

def auto_send_greetings():
    profile_dir = "/Users/wuyang/Documents/self/brower/profile"  # 存储浏览器配置的目录
    
    with sync_playwright() as p:
        # 使用持久化上下文
        context = p.chromium.launch_persistent_context(
            profile_dir,
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        
        # 导航到招聘网站
        page.goto("https://rd6.zhaopin.com/app/recommend?jobNumber=CCL1485189030J40769238505&tab=recommend#sortType=recommend&age=16,23&ad=1&filterTypes=2,3&saveCondition=true")
        
        # 等待页面加载完成
        page.wait_for_load_state("networkidle", timeout=30000)
        
        # 检查是否需要登录
        try:
            page.wait_for_selector("text=筛选", timeout=5000)  # 替换为登录后可见的元素
            print("已登录，直接继续操作")
        except TimeoutError:
            print("未检测到登录状态，执行登录流程")
            # 替换为实际的登录页面选择器和凭据
            page.fill("input[name='username']", "your_username")
            page.fill("input[name='password']", "your_password")
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle", timeout=30000)
            print("登录完成")
        
        for i in range(200):
            try:
                time.sleep(1)
                greet_buttons = page.get_by_role("button", name="打招呼")
                if greet_buttons.count() > 0:
                    greet_buttons.first.click()
                    print(f"已点击第 {i+1} 个打招呼按钮")
                    page.wait_for_selector("text=消息已发送", timeout=10000, state="visible")
                else:
                    print(f"第 {i+1} 次未找到打招呼按钮，可能是页面末尾或需要加载")
                page.evaluate("window.scrollBy(0, 300)")
                page.wait_for_load_state("domcontentloaded", timeout=10000)
            except TimeoutError:
                print(f"第 {i+1} 次操作超时，可能页面加载缓慢或导航发生")
                continue
            except Exception as e:
                print(f"第 {i+1} 次操作遇到错误: {str(e)}")
                page.wait_for_load_state("networkidle", timeout=10000)
                continue
        
        # 关闭上下文（自动保存浏览器状态）
        context.close()
        print("操作完成")

if __name__ == "__main__":
    auto_send_greetings()