
# --- 1. 配置您的硬件 ---
# 在Windows上可能是 'COM3', 'COM4' 等
# 在Linux上可能是 '/dev/ttyUSB0', '/dev/ttyACM0' 等
SERIAL_PORT = 'COM3'  # 串口设备
BAUDRATE = 9600  # 波特率，必须与Arduino代码中的设置一致
BRIGHTNESS = 18  # LED灯的初始亮度，范围0-255

# --- 2. 配置您要监控的服务 ---
# LED灯珠会按照列表中的顺序依次对应
# 例如: 第一个服务对应第0个灯，第二个服务对应第1个灯...

SERVICES_TO_MONITOR = [
    {
        'name': '路由器',
        'method': 'ping',  # 使用 ping 方法检查
        'argu': '192.168.1.1'  # 路由器的IP地址
    },
    {
        'name': '百度',
        'method': 'request',  # 使用 HTTP 请求检查
        'argu': 'https://www.baidu.com'  # 百度的URL
    },
    {
        'name': 'Google',
        'method': 'request-proxy',  # 使用代理请求检查
        'argu': {'url': 'https://www.google.com', 'proxy': 'http://127.0.0.1:7890'}  # Google的URL和代理地址
    },
    {
        'name': '个人博客',
        'method': 'uptime-kuma',  # 使用 Uptime Kuma API 检查
        'argu': 1  # Uptime Kuma中监控项的ID
    },
    {
        'name': '空格',
        'method': 'space',  # 空格占位符
        'argu': ''  # 空格占位符不需要参数
    },
]

# --- 3. 配置Uptime Kuma API ---
# 如果您使用Uptime Kuma来监控服务，请确保以下配置正确。
# UPTIME_KUMA_TOKEN 获取方式:
# 使用 pip 安装 uptime-kuma-api
# 运行 uptime-gettoken.py 脚本，输入您的Uptime Kuma URL、用户名、密码和二次验证代码（如果有）。
UPTIME_KUMA_TOKEN = ""  # 在这里填入您的Uptime Kuma API Token
UPTIME_KUMA_URL = ""  # 在这里填入您的Uptime Kuma URL
