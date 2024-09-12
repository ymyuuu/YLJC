import requests

# 目标网址
url = "https://xn--l6qx3lcvp58x.com/#/login?redirect=/plan/8"

try:
    # 发送 GET 请求
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，则引发 HTTPError

    # 打印响应的 HTML 内容
    print("页面访问成功。")
    print("响应内容的前1000个字符：")
    print(response.text[:1000])  # 打印前1000个字符
except requests.exceptions.RequestException as e:
    print(f"访问网站时发生错误：{e}")
