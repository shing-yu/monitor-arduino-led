from uptime_kuma_api import UptimeKumaApi

url = input("请输入 Uptime Kuma URL: ")
api = UptimeKumaApi(url)

account = input("请输入 Uptime Kuma 用户名: ")
password = input("请输入 Uptime Kuma 密码: ")
twofa = input("请输入 Uptime Kuma 二次验证代码（如果有）: ")

res = api.login(account, password, twofa) if twofa else api.login(account, password)
if res:
    print("已获取Token: ")
    print(f"Token: {res['token']}")
