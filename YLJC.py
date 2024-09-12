import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

# 从环境变量中获取 API URL 和其他敏感信息
bark_api_key = os.getenv("BARK_API_KEY")
traffic_api_url = os.getenv("TRAFFIC_API_URL")
login_url = os.getenv("LOGIN_URL")
plan_url = os.getenv("PLAN_URL")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Bark 推送 API 地址
bark_api_url = f"https://api.day.app/{bark_api_key}/"

def send_notification(title, content):
    """发送通知到 Bark 应用"""
    url = f"{bark_api_url}{title}/{content}"
    try:
        requests.get(url)
    except requests.RequestException as e:
        print(f"发送通知时出错: {e}")

def check_traffic():
    """检查剩余流量信息"""
    try:
        # 使用请求方式获取流量信息
        response = requests.get(traffic_api_url, headers={"User-Agent": "Loon"})
        data = response.text
        
        # 从返回的文本中提取剩余流量信息
        if "剩余流量" in data:
            start = data.find("剩余流量：") + 5
            end = data.find("GB", start)
            remaining_traffic = float(data[start:end].strip())
            print(f"剩余流量: {remaining_traffic} GB")
            return remaining_traffic
        else:
            send_notification("错误", "无法解析流量信息")
            return None
    except Exception as e:
        print(f"检查流量信息时出错: {e}")
        send_notification("错误", f"检查流量信息时出错: {e}")
        return None

def run_script():
    """执行刷取流量的自动化操作"""
    # 设置 Chrome 无头模式以便在服务器上运行
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)

    try:
        # 访问登录页面
        driver.get(login_url)

        # 输入账号和密码
        driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(password)

        # 点击登录按钮
        driver.find_element(By.XPATH, "//button[contains(., 'Login')]").click()

        # 等待页面加载完成
        time.sleep(5)

        # 访问计划页面并点击“下单”按钮
        driver.get(plan_url)
        driver.find_element(By.XPATH, "//button[contains(., 'Order')]").click()
        time.sleep(5)

        # 尝试点击“确认”或“确认取消”按钮
        try:
            confirm_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), 'Confirm') or contains(text(), 'Confirm Cancel')]")
            for button in confirm_buttons:
                button.click()
                time.sleep(3)
        except NoSuchElementException:
            pass

        # 点击“结账”按钮
        driver.find_element(By.XPATH, "//button[contains(., 'Checkout')]").click()
        time.sleep(5)

        return True
    except Exception as e:
        print(f"执行刷取操作时出错: {e}")
        send_notification("错误", f"执行刷取操作时出错: {e}")
        return False
    finally:
        driver.quit()

# 主流程
remaining_traffic = check_traffic()

if remaining_traffic is not None and remaining_traffic < 50:
    print(f"剩余流量不足 5GB，开始执行刷取...")
    if run_script():
        new_remaining_traffic = check_traffic()
        if new_remaining_traffic > 5:
            print(f"刷取成功！现在流量: {new_remaining_traffic} GB")
            send_notification("刷取成功", f"现在流量: {new_remaining_traffic} GB")
        else:
            print("刷取失败，流量未达到预期值。")
            send_notification("刷取失败", f"现在流量: {new_remaining_traffic} GB")
else:
    print(f"剩余流量充足: {remaining_traffic} GB，无需刷取。")
