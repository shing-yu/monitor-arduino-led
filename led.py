import serial
import time

class LedController:
    """
    通过串口控制连接到Arduino的WS2812B灯带的Python类。
    """

    def __init__(self, port: str, baudrate: int = 9600, led_count: int = 10):
        """
        初始化串口连接。

        :param port: Arduino连接的串口设备文件路径。
                     Windows: 'COM3', 'COM4'等
                     Linux: '/dev/ttyUSB0', '/dev/ttyACM0'等
        :param baudrate: 波特率，必须与Arduino代码中的设置一致。
        :param led_count: 灯带上的LED数量，用于动画效果。
        """
        self.led_count = led_count
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            # 等待Arduino重启完成
            time.sleep(2)
            print(f"成功连接到 {port}")
            self.set_brightness(10)  # 设置初始亮度为10
        except serial.SerialException as e:
            print(f"错误：无法打开串口 {port}。")
            print(f"请检查设备是否连接/繁忙，或者是否有权限访问。")
            print(f"在Linux上,可尝试使用 'sudo chmod 666 {port}' 来授予权限。")
            print(f"详细错误: {e}")
            self.ser = None

    def _send_command(self, command: str):
        """向Arduino发送指令。"""
        if not self.ser:
            # print("错误：串口未连接。") # 在循环中打印会很烦人，暂时注释
            return

        full_command = command + '\n'
        self.ser.write(full_command.encode('utf-8'))

    def show(self):
        """
        发送更新指令 (S)，将之前所有设置应用到灯带上。
        对于动画或批量更新，这非常高效。
        """
        self._send_command("S")

    def set_single_color(self, index: int, r: int, g: int, b: int, auto_show: bool = True):
        """
        设置单个灯珠的颜色。

        :param index: 灯珠的索引 (从0开始)。
        :param r: 红色分量 (0-255)。
        :param g: 绿色分量 (0-255)。
        :param b: 蓝色分量 (0-255)。
        :param auto_show: 如果为 True，则立即更新灯带显示。
        """
        r, g, b = [max(0, min(255, c)) for c in (r, g, b)]
        command = f"C,{index},{r},{g},{b}"
        self._send_command(command)
        if auto_show:
            self.show()

    def set_all_color(self, r: int, g: int, b: int, auto_show: bool = True):
        """
        设置所有灯珠为同一种颜色。
        """
        r, g, b = [max(0, min(255, c)) for c in (r, g, b)]
        command = f"A,{r},{g},{b}"
        self._send_command(command)
        if auto_show:
            self.show()

    def set_brightness(self, brightness: int, auto_show: bool = True):
        """
        设置灯带的整体亮度。
        """
        brightness = max(0, min(255, brightness))
        command = f"B,{brightness}"
        self._send_command(command)
        if auto_show:
            self.show()

    def turn_off(self, auto_show: bool = True):
        """
        关闭所有灯珠。
        """
        self._send_command("O")
        if auto_show:
            self.show()

    @staticmethod
    def _color_wheel(pos: int) -> tuple[int, int, int]:
        """
        输入一个0-255之间的值，返回一个(r, g, b)颜色元组。
        """
        pos = pos & 255
        if pos < 85:
            return pos * 3, 255 - pos * 3, 0
        elif pos < 170:
            pos -= 85
            return 255 - pos * 3, 0, pos * 3
        else:
            pos -= 170
            return 0, pos * 3, 255 - pos * 3

    def rainbow_scroll(self, duration_s: int = 5):
        """
        执行彩虹滚动效果。
        """
        if not self.ser:
            print("错误：无法执行动画，串口未连接。")
            return
        print(f"\n执行彩虹滚动效果 ({duration_s}秒)...")
        start_time = time.time()
        j = 0
        while time.time() < start_time + duration_s:
            for i in range(self.led_count):
                pixel_hue = (i * 256 // self.led_count + j)
                r, g, b = self._color_wheel(pixel_hue)
                self.set_single_color(i, r, g, b, auto_show=False)

            self.show()
            time.sleep(0.01)
            j = (j + 1) % 256

    def close(self):
        """关闭串口连接。"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("\n串口连接已关闭。")