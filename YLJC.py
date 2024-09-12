from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# 函数：发送Bark通知
def send_bark_notification(title, content):
    api_url = f"https://api.day.app/Y6wZN8swvDrno2URYa5CDZ/{title}/{content}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print("通知已发送。")
        else:
            print("发送通知失败。状态码：", response.status_code)
    except Exception as e:
        print("发送通知时发生错误：", e)

# 函数：检查流量信息
def check_remaining_data():
    print("正在检查流量信息...")
    headers = {"User-Agent": "Loon"}
    url = "https://315d0fe0-47cc-4afb-8d61-e714ee509609.xn--l6qx3lcvp58x.com/api/v1/client/subscribe?token=f03265a6ac38302d8dc247a5af93fb92"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.text
            remaining_data = float(data.split("剩余流量：")[1].split(" GB")[0])
            print(f"当前剩余流量：{remaining_data} GB")
            return remaining_data, data
        else:
            error_message = f"无法获取流量信息，状态码：{response.status_code}"
            print(error_message)
            send_bark_notification("流量检查失败", error_message)
            return None, None
    except Exception as e:
        error_message = f"获取流量信息时发生错误：{e}"
        print(error_message)
        send_bark_notification("流量检查失败", error_message)
        return None, None

# 函数：等待元素
def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return element
    except Exception as e:
        print(f"等待元素 {value} 时发生错误: {e}")
        return None

# 函数：查找并打印所有输入框
def find_all_inputs(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    inputs = driver.find_elements(By.XPATH, "//input")
    for i, input_element in enumerate(inputs, start=1):
        try:
            placeholder = input_element.get_attribute("placeholder")
            xpath = driver.execute_script(
                "function getElementXPath(element) {"
                "   var paths = [];"
                "   while (element.nodeType === Node.ELEMENT_NODE) {"
                "       var index = 0;"
                "       for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {"
                "           if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === element.tagName) {"
                "               index++;"
                "           }"
                "       }"
                "       var tagName = element.tagName.toLowerCase();"
                "       var path = tagName + (index ? '[' + (index + 1) + ']' : '');"
                "       paths.unshift(path);"
                "       element = element.parentNode;"
                "   }"
                "   return paths.length ? '/' + paths.join('/') : null;"
                "}"
                "return getElementXPath(arguments[0]);", input_element)
            print(f"输入框 {i}:")
            print(f"  Placeholder: {placeholder}")
            print(f"  XPath: {xpath}")
        except Exception as e:
            print(f"输入框 {i} 获取信息时发生错误: {e}")

# 函数：点击按钮
def click_button(driver, xpath):
    try:
        button = wait_for_element(driver, By.XPATH, xpath)
        if button:
            button.click()
            time.sleep(3)
        else:
            print(f"未找到按钮：{xpath}，跳过此步骤。")
    except Exception as e:
        print(f"点击按钮时发生错误：{e}")

# 函数：执行下单和结账
def place_order_and_checkout(driver):
    click_button(driver, "//button[contains(., '下单')]")
    click_button(driver, "//span[contains(text(), '确定') or contains(text(), '确认取消')]")
    click_button(driver, "//button[contains(., '结账')]")

# 主函数：刷取流量
def main():
    original_remaining_data, original_data_info = check_remaining_data()

    if original_remaining_data is not None and original_remaining_data < 55:
        print("剩余流量不足 5G，开始执行刷取...")

        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 隐藏浏览器窗口
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://xn--l6qx3lcvp58x.com/#/login?redirect=/plan/8")

            # 查找并打印所有输入框
            find_all_inputs(driver)

            # 登录
            email_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='邮箱']")
            password_input = wait_for_element(driver, By.XPATH, "//input[@placeholder='密码']")
            login_button = wait_for_element(driver, By.XPATH, "//button[contains(., '登入')]")
            
            if email_input and password_input and login_button:
                email_input.send_keys("ymyuuu@qq.com")
                password_input.send_keys("ymyuuu@qq.com")
                login_button.click()
                time.sleep(5)
            else:
                print("登录元素未找到。")

            # 第一次下单和结账
            place_order_and_checkout(driver)

            # 第二次下单和结账
            driver.get("https://xn--l6qx3lcvp58x.com/#/plan/9")
            time.sleep(5)
            place_order_and_checkout(driver)

        except Exception as e:
            error_message = f"执行刷取过程时发生错误：{e}"
            print(error_message)
            send_bark_notification("刷取过程失败", error_message)
        finally:
            if 'driver' in locals():
                driver.quit()

        # 检查刷取后的流量信息
        current_remaining_data, current_data_info = check_remaining_data()

        # 判断刷取是否成功
        if current_remaining_data is not None and current_remaining_data > 50:
            print("刷取成功。")
            send_bark_notification("刷取成功", f"原始流量：{original_remaining_data} GB，现在流量：{current_remaining_data} GB")
        else:
            print("刷取未成功。")
            send_bark_notification("刷取失败", f"原始流量：{original_remaining_data} GB，现在流量：{current_remaining_data if current_remaining_data else '未获取'}")
    else:
        print("流量充足，无需刷取。")

if __name__ == "__main__":
    main()
