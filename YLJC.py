from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        # 访问登录页面
        driver.get(login_url)

        # 输入账号和密码
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))).send_keys(password)

        # 点击登录按钮
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]"))).click()

        # 等待页面加载完成
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Order')]"))).click()

        # 尝试点击“确定”或“确认取消”按钮
        try:
            confirm_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Confirm') or contains(text(), 'Confirm Cancel')]")))
            for button in confirm_buttons:
                button.click()
                time.sleep(3)  # 可以考虑去掉或调整
                print("已点击按钮：", button.text)
        except NoSuchElementException:
            print("未找到任何按钮，跳过此步骤。")

        # 点击“结账”按钮
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Chectout')]"))).click()

        # 访问新的 URL 进行第二次刷取
        driver.get(plan_url)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Order')]"))).click()

        # 再次尝试点击“确定”或“确认取消”按钮
        try:
            confirm_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(text(), 'Confirm') or contains(text(), 'Confirm Cancel')]")))
            for button in confirm_buttons:
                button.click()
                time.sleep(3)  # 可以考虑去掉或调整
                print("已点击按钮：", button.text)
        except NoSuchElementException:
            print("未找到任何按钮，跳过此步骤。")

        # 点击“结账”按钮
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Chectout')]"))).click()

        print("流量刷取完成，重新检查流量信息...")
        return True
    except Exception as e:
        print(f"执行刷取操作时出错: {e}")
        send_notification("错误", f"执行刷取操作时出错: {e}")
        return False
    finally:
        driver.quit()
