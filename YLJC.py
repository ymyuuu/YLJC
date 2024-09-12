from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
import requests
import time

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
            print(f"无法获取流量信息，状态码：{response.status_code}")
            return None, None
    except Exception as e:
        print(f"获取流量信息时发生错误：{e}")
        return None, None

# 函数：点击按钮
def click_button(driver, xpath):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button.click()
        time.sleep(3)
    except (NoSuchElementException, ElementClickInterceptedException, TimeoutException) as e:
        print(f"点击按钮失败：{e}")

# 函数：执行下单和结账
def place_order_and_checkout(driver):
    click_button(driver, "//button[contains(., '下单')]")
    click_button(driver, "//span[contains(text(), '确定') or contains(text(), '确认取消')]")
    click_button(driver, "//button[contains(., '结账')]")

# 主函数：刷取流量
def main():
    original_remaining_data, original_data_info = check_remaining_data()

    if original_remaining_data is not None and original_remaining_data < 50:
        print("剩余流量不足 5G，开始执行刷取...")

        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://xn--l6qx3lcvp58x.com/#/login?redirect=/plan/8")

            # 显式等待邮箱输入框的加载
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='邮箱']")))
            
            # 登录
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
            print(f"执行刷取过程时发生错误：{e}")
        finally:
            driver.quit()

        # 检查刷取后的流量信息
        current_remaining_data, current_data_info = check_remaining_data()

        # 判断刷取是否成功
        if current_remaining_data is not None and current_remaining_data > 50:
            print("刷取成功。")
        else:
            print("刷取未成功。")
    else:
        print("流量充足，无需刷取。")

if __name__ == "__main__":
    main()
