from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_all_buttons(driver):
    # 等待页面加载完毕
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 查找所有按钮
    buttons = driver.find_elements(By.XPATH, "//button")
    
    # 打印每个按钮的文本和XPath
    for i, button in enumerate(buttons, start=1):
        try:
            text = button.text
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
                "return getElementXPath(arguments[0]);", button)
            print(f"按钮 {i}:")
            print(f"  文本: {text}")
            print(f"  XPath: {xpath}")
        except Exception as e:
            print(f"按钮 {i} 获取信息时发生错误: {e}")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 隐藏浏览器窗口
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://xn--l6qx3lcvp58x.com/#/login?redirect=/plan/8")

    find_all_buttons(driver)
    
    driver.quit()

if __name__ == "__main__":
    main()
