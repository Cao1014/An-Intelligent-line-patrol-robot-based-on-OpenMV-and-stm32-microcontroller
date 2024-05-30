#include "mbed.h"

// Maximum number of element the application buffer can contain
#define MAXIMUM_BUFFER_SIZE 32

BufferedSerial hc_06(D1, D0); // tx, rx
BufferedSerial pc(USBTX, USBRX); // tx, rx

PwmOut gate_servo(A1);


char buf[MAXIMUM_BUFFER_SIZE] = {0};

int main() {
    pc.set_baud(9600); // 设置计算机通信的波特率为9600
    hc_06.set_baud(9600); // 设置HC-06模块通信的波特率为9600

    printf("Serial communication between Mbed and HC-06 Bluetooth module\r\n");
    printf("Enter 'AT' to configure HC-06 module\r\n");

    while(1) {
        // 从计算机读取数据，并发送到 HC-06 模块
        while (pc.readable()) {
            char pc_data;
            pc.read(&pc_data, 1);
            hc_06.write(&pc_data, 1);
        }

        // 从 HC-06 模块读取数据，并发送到计算机
        while (hc_06.readable()) {
            char bt_data;
            hc_06.read(&bt_data, 1);
            pc.write(&bt_data, 1);

            // 如果接收到 "open" 信号，则设置引脚 A1 转至90度，开门
            if (bt_data=='u') {
                printf("open\r\n");
                gate_servo.period_ms(20);// 设置 PWM 频率为 50 Hz (周期为 20ms)
                gate_servo.write(0.08);// 设置占空比为0.03=0度，0.05=45度，0.08=90度
                thread_sleep_for(5000);
            }
            
            // 如果接收到 "close" 信号，则设置引脚 A1 转至0度，关门
            else if (bt_data=='d') {
                printf("close\r\n");
                gate_servo.period_ms(20);// 设置 PWM 频率为 50 Hz (周期为 20ms)
                gate_servo.write(0.03);// 设置占空比为0.03=0度，0.05=45度，0.08=90度
                thread_sleep_for(5000);
            }
        }
    }
}
