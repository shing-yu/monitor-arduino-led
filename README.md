# monitor-arduino-led
一个配合 Arduino 和 WS2812B LED 的服务监控脚本  
A service monitor that works with Arduino and WS2812B LEDs.

### 使用方法 How to use
1. 将Arduino连接到电脑，编辑并上传`ino/led.ino`代码到Arduino中。  
   Connect the Arduino to your computer, then edit and upload the `ino/led.ino` code to the Arduino.
2. 复制`config-example.py`为`config.py`，并根据需要修改配置。  
   Copy `config-example.py` to `config.py` and modify the configuration as needed.
3. 安装所需的Python库，运行以下命令：  
   Install the required Python libraries by running the following command:  
   `pip install -r requirements.txt`
4. 运行`monitor.py`脚本。  
   Run the `monitor.py` script.
5. 如果需要，可以修改`monitor.py`中的LED控制逻辑和颜色定义。
   If needed, you can modify the LED control logic and color definitions in `monitor.py`.

### 支持的方式 Supported methods
- **HTTP**: 通过HTTP请求检查服务状态（支持代理）。  
  Check service status via HTTP requests (supports proxy).
- **Ping**: 通过Ping命令检查服务是否可达。  
  Check service reachability via Ping command.
- **[Uptime Kuma](https://github.com/louislam/uptime-kuma)**: 通过 [Uptime Kuma](https://github.com/louislam/uptime-kuma) API 检查服务状态。  
  Check service status via [Uptime Kuma](https://github.com/louislam/uptime-kuma) API.  
  运行`uptime-gettoken.py`脚本以获取API Token。  
  Run the `uptime-gettoken.py` script to get the API Token.

需要更多方式？提交 [Issue](https://github.com/shing-yu/monitor-arduino-led/issues) 或 [PR](https://github.com/shing-yu/monitor-arduino-led/pulls)！  
Want more methods? Submit an [Issue](https://github.com/shing-yu/monitor-arduino-led/issues) or a [PR](https://github.com/shing-yu/monitor-arduino-led/pulls) !

### 许可证 License
本项目采用MIT许可证，详见 LICENSE 文件。  
This project is licensed under the MIT License. See the LICENSE file for details.
