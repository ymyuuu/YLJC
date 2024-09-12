from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import requests
import time

# 函数：发送Bark通知
def send_bark_notification(title, content):
    # 直接将 Bark API 地址写在代码中
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
    
    # API地址，直接写在代码中
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

# 函数：点击按钮
def click_button(driver, xpath):
    try:
        button = driver.find_element(By.XPATH, xpath)
        button.click()
        time.sleep(3)
    except (NoSuchElementException, ElementClickInterceptedException) as e:
        if isinstance(e, ElementClickInterceptedException):
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)
        else:
            print(f"未找到按钮：{xpath}，跳过此步骤。")

# 函数：执行下单和结账
def place_order_and_checkout(driver):
    click_button(driver, "//button[contains(., '下单')]")
    click_button(driver, "//span[contains(text(), '确定') or contains(text(), '确认取消')]")
    click_button(driver, "//button[contains(., '结账')]")

# 主函数：刷取流量
def main():
    original_remaining_data, original_data_info = check_remaining_data()

    if original_remaining_data is not None and original_remaining_data < 5:
        print("剩余流量不足 5G，开始执行刷取...")

        try:
            # 启动无头模式浏览器
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # 无头模式
            options.add_argument('--disable-gpu')  # 禁用 GPU 加速
            options.add_argument('--no-sandbox')  # 取消沙箱模式

            driver = webdriver.Chrome(options=options)
            driver.get("https://xn--l6qx3lcvp58x.com/#/login?redirect=/plan/8")

            # 登录（在代码中直接提供用户名和密码）
            driver.find_element(By.XPATH, "//input[@placeholder='邮箱']").send_keys("ymyuuu@qq.com")
            driver.find_element(By.XPATH, "//input[@placeholder='密码']").send_keys("ymyuuu@qq.com")
            driver.find_element(By.XPATH, "//button[contains(., '登入')]").click()
            time.sleep(5)

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
