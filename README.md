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

### 许可证 License
本项目采用MIT许可证，详见 LICENSE 文件。
This project is licensed under the MIT License. See the LICENSE file for details.
