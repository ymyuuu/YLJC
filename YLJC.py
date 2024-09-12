from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def run_script():
    """执行刷取流量的自动化操作"""
    # 设置 Chrome 无头模式以便在服务器上运行，并将浏览器语言设置为中文
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=zh-CN")

    # 启动 Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # 使用显式等待
    wait = WebDriverWait(driver, 10)  # 等待最长10秒

    try:
        print("正在访问登录页面...")
        driver.get(login_url)

        # 输入账号和密码
        print("正在输入账号...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(username)
        print(f"账号 {username} 已输入")

        print("正在输入密码...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(password)
        print("密码已输入")

        # 点击登录按钮
        print("正在点击登录按钮...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]"))).click()
        print("已点击登录按钮，等待页面加载...")

        # 点击“下单”按钮
        print("等待并点击“下单”按钮...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Order')]"))).click()
        print("“下单”按钮已点击")

        # 尝试点击“确定”或“确认取消”按钮
        print("尝试查找并点击“确定”或“确认取消”按钮...")
        try:
            confirm_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Confirm') or contains(text(), 'Confirm Cancel')]")))
            for button in confirm_buttons:
                try:
                    print(f"尝试点击按钮：{button.text}")
                    button.click()
                    time.sleep(3)  # 可以考虑去掉或调整
                    print(f"已成功点击按钮：{button.text}")
                except StaleElementReferenceException:
                    print(f"元素已过期，无法点击：{button.text}")
        except NoSuchElementException:
            print("未找到任何“确定”或“确认取消”按钮，跳过此步骤。")

        # 点击“结账”按钮
        print("等待并点击“结账”按钮...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Chectout')]"))).click()
        print("“结账”按钮已点击")

        # 访问新的 URL 进行第二次刷取
        print("访问新的 URL 进行第二次刷取...")
        driver.get(plan_url)
        print("等待并点击“下单”按钮...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Order')]"))).click()
        print("“下单”按钮已点击")

        # 再次尝试点击“确定”或“确认取消”按钮
        print("再次尝试查找并点击“确定”或“确认取消”按钮...")
        try:
            confirm_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Confirm') or contains(text(), 'Confirm Cancel')]")))
            for button in confirm_buttons:
                try:
                    print(f"尝试点击按钮：{button.text}")
                    button.click()
                    time.sleep(3)  # 可以考虑去掉或调整
                    print(f"已成功点击按钮：{button.text}")
                except StaleElementReferenceException:
                    print(f"元素已过期，无法点击：{button.text}")
        except NoSuchElementException:
            print("未找到任何“确定”或“确认取消”按钮，跳过此步骤。")

        # 点击“结账”按钮
        print("等待并点击“结账”按钮...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Chectout')]"))).click()
        print("“结账”按钮已点击")

        print("流量刷取完成，重新检查流量信息...")
        return True
    except Exception as e:
        print(f"执行刷取操作时出错: {e}")
        send_notification("错误", f"执行刷取操作时出错: {e}")
        return False
    finally:
        driver.quit()
