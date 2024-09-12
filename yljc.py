import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent  # 用于生成随机的 User-Agent
import time

# 从环境变量中读取 API 和其他配置
bark_api_url = os.getenv("BARK_API_URL")
traffic_api_url = os.getenv("TRAFFIC_API_URL")
login_url = os.getenv("LOGIN_URL")
plan_8_url = os.getenv("PLAN_8_URL")
plan_9_url = os.getenv("PLAN_9_URL")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def send_notification(title, content):
    """发送通知到 Bark 应用"""
    url = f"{bark_api_url}{title}/{content}"
    try:
        requests.get(url)
        print("通知已发送")
    except requests.RequestException as e:
        print(f"发送通知时出错: {e}")

def check_traffic():
    """检查剩余流量信息"""
    print("正在检查流量信息...")
    try:
        # 使用 curl 方式请求流量信息
        response = requests.get(traffic_api_url, headers={"User-Agent": user_agent})
        data = response.text
        print("当前剩余流量信息：", data)
        
        # 从返回的文本中提取剩余流量信息
        if "剩余流量" in data:
            start = data.find("剩余流量：") + 5
            end = data.find("GB", start)
            remaining_traffic = float(data[start:end].strip())
            return remaining_traffic
        else:
            print("无法解析流量信息")
            send_notification("错误", "无法解析流量信息")
            return None
    except Exception as e:
        print(f"检查流量信息时出错: {e}")
        send_notification("错误", f"检查流量信息时出错: {e}")
        return None

def run_script():
    """执行刷取流量的自动化操作"""

    # 使用 fake_useragent 随机生成 macOS 的 User-Agent
    ua = UserAgent()
    user_agent = ua.random
    while "Macintosh" not in user_agent:
        user_agent = ua.random

    # 设置 Chrome 无头模式以便在服务器上运行
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agent}")

    # 启动 Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # 访问登录页面
        driver.get(login_url)

        # 输入账号和密码
        driver.find_element(By.XPATH, "//input[@placeholder='邮箱']").send_keys(email)
        driver.find_element(By.XPATH, "//input[@placeholder='密码']").send_keys(password)

        # 点击登录按钮
        driver.find_element(By.XPATH, "//button[contains(., '登入')]").click()

        # 等待页面加载完成
        time.sleep(5)

        # 点击“下单”按钮
        driver.find_element(By.XPATH, "//button[contains(., '下单')]").click()
        time.sleep(5)

        # 尝试点击“确定”或“确认取消”按钮
        try:
            confirm_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), '确定') or contains(text(), '确认取消')]")
            for button in confirm_buttons:
                button.click()
                time.sleep(3)
                print("已点击按钮：", button.text)
        except NoSuchElementException:
            print("未找到任何按钮，跳过此步骤。")

        # 点击“结账”按钮
        driver.find_element(By.XPATH, "//button[contains(., '结账')]").click()
        time.sleep(5)

        # 访问新的 URL 进行第二次刷取
        driver.get(plan_9_url)
        time.sleep(5)

        # 重复刷取步骤
        driver.find_element(By.XPATH, "//button[contains(., '下单')]").click()
        time.sleep(5)

        # 再次尝试点击“确定”或“确认取消”按钮
        try:
            confirm_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), '确定') or contains(text(), '确认取消')]")
            for button in confirm_buttons:
                button.click()
                time.sleep(3)
                print("已点击按钮：", button.text)
        except NoSuchElementException:
            print("未找到任何按钮，跳过此步骤。")

        # 点击“结账”按钮
        driver.find_element(By.XPATH, "//button[contains(., '结账')]").click()
        time.sleep(5)

        print("流量刷取完成，重新检查流量信息...")
        return True
    except Exception as e:
        print(f"执行刷取操作时出错: {e}")
        send_notification("错误", f"执行刷取操作时出错: {e}")
        return False
    finally:
        driver.quit()

# 主流程
remaining_traffic = check_traffic()

if remaining_traffic is not None and remaining_traffic < 5:
    print("剩余流量不足 5G，开始执行刷取...")
    if run_script():
        new_remaining_traffic = check_traffic()
        if new_remaining_traffic > 5:
            print(f"刷取成功！原流量: {remaining_traffic} GB, 现在流量: {new_remaining_traffic} GB")
            send_notification("刷取成功", f"原流量: {remaining_traffic} GB, 现在流量: {new_remaining_traffic} GB")
        else:
            print("刷取失败，流量未达到预期值。")
            send_notification("刷取失败", f"原流量: {remaining_traffic} GB, 现在流量: {new_remaining_traffic} GB")
else:
    print(f"剩余流量充足: {remaining_traffic} GB，无需刷取。")
