#include <Adafruit_NeoPixel.h>

// --- 可配置参数 ---
#define LED_PIN    6     // 灯带数据线连接的 Arduino 引脚
#define LED_COUNT  30    // 灯带上灯珠的数量
// -----------------

// 初始化 Adafruit_NeoPixel 对象
// 参数1: 灯珠数量
// 参数2: Arduino 引脚号
// 参数3: 灯珠类型 + 颜色顺序。对于WS2812B，通常是 NEO_GRB + NEO_KHZ800
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // 启动串口通信，波特率为 9600
  Serial.begin(9600);
  strip.begin();           // 初始化 NeoPixel 库
  strip.setBrightness(10); // 设置一个适中的初始亮度 (0-255)
  strip.show();            // 更新灯带，熄灭所有灯珠
}

void loop() {
  // 检查串口是否有数据可读
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // 读取一行指令
    command.trim(); // 去除首尾的空白字符

    // 解析指令
    if (command.startsWith("C")) {        // 设置单个灯珠颜色: C,<index>,<r>,<g>,<b>
      setColor(command);
    } else if (command.startsWith("A")) { // 设置所有灯珠颜色: A,<r>,<g>,<b>
      setAllColor(command);
    } else if (command.startsWith("B")) { // 设置亮度: B,<brightness>
      setBrightnessCmd(command);
    } else if (command == "O") {          // 关闭所有灯珠
      clearAll();
    } else if (command == "S") {          // 更新显示 (Show)
      strip.show();
    }
  }
}

// 解析并设置单个灯珠颜色的函数
// 注意: 此函数不再自动调用 strip.show()
void setColor(String command) {
  // 移除 'C,' 前缀
  command.remove(0, 2);
  
  char* str = (char*)command.c_str();

  char* p = strtok(str, ",");
  if (p == NULL) return;
  int index = atoi(p);

  p = strtok(NULL, ",");
  if (p == NULL) return;
  int r = atoi(p);

  p = strtok(NULL, ",");
  if (p == NULL) return;
  int g = atoi(p);

  p = strtok(NULL, ",");
  if (p == NULL) return;
  int b = atoi(p);

  if (index >= 0 && index < strip.numPixels()) {
    strip.setPixelColor(index, strip.Color(r, g, b));
  }
}

// 解析并设置所有灯珠颜色的函数
// 注意: 此函数不再自动调用 strip.show()
void setAllColor(String command) {
  // 移除 'A,' 前缀
  command.remove(0, 2);
  
  char* str = (char*)command.c_str();

  char* p = strtok(str, ",");
  if (p == NULL) return;
  int r = atoi(p);

  p = strtok(NULL, ",");
  if (p == NULL) return;
  int g = atoi(p);

  p = strtok(NULL, ",");
  if (p == NULL) return;
  int b = atoi(p);
    
  for(int i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, strip.Color(r, g, b));
  }
}

// 解析并设置亮度的函数
// 注意: 此函数不再自动调用 strip.show()
void setBrightnessCmd(String command) {
  // 移除 'B,' 前缀
  command.remove(0, 2);
  int brightness = command.toInt();
  
  // 将亮度限制在 0-255 范围内
  if (brightness < 0) brightness = 0;
  if (brightness > 255) brightness = 255;
  
  strip.setBrightness(brightness);
}

// 关闭所有灯珠的函数
// 注意: 此函数不再自动调用 strip.show()
void clearAll() {
  for(int i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, 0); // 设置为黑色，即关闭
  }
}