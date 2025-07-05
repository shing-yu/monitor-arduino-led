import time
import requests
import subprocess
import sys
from uptime_kuma_api import UptimeKumaApi, MonitorStatus
from led import LedController
import os

if os.path.exists('config.py'): from config import *
else:  print("错误：未找到配置文件 'config.py'。请创建该文件并定义必要的配置。"); sys.exit(1)

# ==============================================================================
# 服务监控器类
# ==============================================================================
class ServiceMonitor:
    """
    监控一系列服务并通过 LedController 显示其状态。
    """
    # 状态定义
    STATUS_OK = 'OK'
    STATUS_FAIL = 'FAIL'
    STATUS_PENDING = 'PENDING'
    STATUS_MAINTENANCE = 'MAINTENANCE'
    SPACE = 'SPACE'  # 空格占位符

    # 颜色定义 (R, G, B)
    COLOR_CYAN = (0, 255, 255)  # 正常
    COLOR_YELLOW = (255, 200, 0)  # 首次失败 / Pending
    COLOR_RED = (255, 0, 0)  # 多次失败 / Down
    COLOR_BLUE = (0, 0, 255)  # 维护
    COLOR_OFF = (0, 0, 0)  # 关闭

    def __init__(self, led_controller: LedController, services_config: list,
                 uptime_kuma_token: str = None, uptime_kuma_url: str = None):
        self.led_controller = led_controller
        self.services = services_config
        self.failure_counts = {service['name']: 0 for service in self.services}
        self.uptime_kuma_token = uptime_kuma_token
        self.uptime_kuma_url = uptime_kuma_url
        self.kuma_apis = {}  # 用于缓存Uptime Kuma的API实例

    def _check_ping(self, host: str) -> str:
        """使用ping命令检查主机可达性。"""
        try:
            # 根据操作系统选择不同参数
            param = '-n' if sys.platform == 'win32' else '-c'
            command = ['ping', param, '2', '-w', '2', host]
            # 隐藏命令行窗口和输出
            process = subprocess.run(command, capture_output=True, check=False)
            return self.STATUS_OK if process.returncode == 0 else self.STATUS_FAIL
        except Exception as e:
            print(f"  [Ping Error] {host}: {e}")
            return self.STATUS_FAIL

    def _check_request(self, url: str, proxy: dict = None) -> str:
        """检查URL是否可访问。"""
        try:
            proxies = {'http': proxy, 'https': proxy} if proxy else None
            response = requests.get(url, timeout=10, proxies=proxies)
            # 认为234状态码都是成功的
            return self.STATUS_OK if response.status_code < 500 else self.STATUS_FAIL
        except requests.exceptions.RequestException:
            # print(f"  [Request Error] {url}: {e}") # 错误信息可能过长
            return self.STATUS_FAIL

    def _check_uptime_kuma(self, service_id: int) -> str:
        """通过Uptime Kuma API获取监控状态。"""
        api_url = self.uptime_kuma_url
        token = self.uptime_kuma_token

        if not all([api_url, token]):
            print(f"  [UptimeKuma Error] {service_id}: API配置不完整。")
            return self.STATUS_FAIL

        try:
            # 缓存API实例，避免重复登录
            if api_url not in self.kuma_apis:
                api = UptimeKumaApi(api_url)
                api.login_by_token(token)
                self.kuma_apis[api_url] = api
            else:
                api = self.kuma_apis[api_url]

            status = api.get_monitor_status(service_id)
            if status == MonitorStatus.UP:
                return self.STATUS_OK
            elif status == MonitorStatus.PENDING:
                return self.STATUS_PENDING
            elif status == MonitorStatus.MAINTENANCE:
                return self.STATUS_MAINTENANCE
            else:  # DOWN or other
                return self.STATUS_FAIL

            # print(f"  [UptimeKuma Warning] 在Uptime Kuma中未找到名为'{service_id}'的监控项。")
            # return self.STATUS_FAIL

        except Exception as e:
            print(f"  [UptimeKuma Error] {service_id}: {e}")
            # 如果API连接失败，清除缓存的实例以便下次重试
            if api_url in self.kuma_apis:
                del self.kuma_apis[api_url]
            return self.STATUS_FAIL

    def run_check(self):
        """执行一轮所有服务的检查，并更新LED状态。"""
        if not self.led_controller or not self.led_controller.ser:
            print("监控暂停，因为LED控制器未连接。")
            return

        print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - 开始新一轮监控...")
        start_time = time.time()

        for i, service in enumerate(self.services):
            name = service['name']
            method = service['method']
            argu = service['argu']
            status = self.STATUS_FAIL  # 默认为失败

            print(f"  - 正在检查 {name} (方法: {method})...", end='')

            if method == 'ping':
                status = self._check_ping(argu)
            elif method == 'request':
                status = self._check_request(argu)
            elif method == 'request-proxy':
                # 'argu'应为 {'url': '...', 'proxy': '...'}
                status = self._check_request(argu.get('url'), argu.get('proxy'))
            elif method == 'uptime-kuma':
                # 'name' 用于匹配监控项，'argu' 包含API连接信息
                status = self._check_uptime_kuma(argu)
            elif method == 'space':
                # 空格占位符，什么都不做
                status = self.SPACE

            print(f" 结果: {status}")

            # 根据状态和历史失败次数决定颜色
            # noinspection PyUnusedLocal
            color = self.COLOR_OFF
            if method == 'uptime-kuma':
                if status == self.STATUS_OK:
                    color = self.COLOR_CYAN
                elif status == self.STATUS_PENDING:
                    color = self.COLOR_YELLOW
                elif status == self.STATUS_MAINTENANCE:
                    color = self.COLOR_BLUE
                else:  # FAIL
                    color = self.COLOR_RED
            else:  # ping, request, request-proxy
                if status == self.STATUS_OK:
                    self.failure_counts[name] = 0
                    color = self.COLOR_CYAN
                elif status == self.SPACE:
                    color = self.COLOR_OFF  # 空格占位符，不显示颜色
                else:  # FAIL
                    self.failure_counts[name] += 1
                    if self.failure_counts[name] == 1:
                        color = self.COLOR_YELLOW  # 首次失败
                    else:
                        color = self.COLOR_RED  # 多次失败

            # 设置单个LED颜色，但不立即显示
            self.led_controller.set_single_color(i, *color, auto_show=False)

        # 所有LED颜色设置完毕后，一次性更新灯带
        self.led_controller.show()
        print("所有服务状态已更新到LED灯带。")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"本轮检查耗时: {elapsed_time:.2f}秒")

    # noinspection PyUnreachableCode
    def start_monitoring_loop(self, interval_minutes: int = 5):
        """启动无限监控循环。"""
        try:
            while True:
                self.run_check()
                sleep_seconds = interval_minutes * 60
                print(f"下一轮检查将在 {interval_minutes} 分钟后开始...")
                time.sleep(sleep_seconds)
        except KeyboardInterrupt:
            print("\n监控程序被用户中断。")
        finally:
            if self.led_controller:
                print("程序退出前关闭所有LED...")
                self.led_controller.turn_off()
                self.led_controller.close()
            # 关闭所有Uptime Kuma API会话
            for api in self.kuma_apis.values():
                api.disconnect()


# ==============================================================================
# 主程序入口
# ==============================================================================
if __name__ == '__main__':
    LED_COUNT = len(SERVICES_TO_MONITOR)

    # --- 4. 初始化并运行 ---
    print("正在初始化LED控制器...")
    led = LedController(port=SERIAL_PORT, baudrate=BAUDRATE, led_count=LED_COUNT)

    # 检查串口是否成功连接
    if led.ser:
        # 启动动画，确认LED工作正常
        led.set_brightness(18)
        led.rainbow_scroll(duration_s=3)
        led.turn_off()
        time.sleep(1)

        # 创建并启动监控器
        monitor_ = ServiceMonitor(led, SERVICES_TO_MONITOR, uptime_kuma_token=UPTIME_KUMA_TOKEN, uptime_kuma_url=UPTIME_KUMA_URL)
        monitor_.start_monitoring_loop(interval_minutes=3)
    else:
        print("无法启动监控，因为LED控制器初始化失败。请检查串口设置。")