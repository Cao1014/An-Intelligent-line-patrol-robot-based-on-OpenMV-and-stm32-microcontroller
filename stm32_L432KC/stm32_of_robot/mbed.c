/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

using namespace std::chrono;

DigitalOut trigger_1(D2);
DigitalIn  echo_1(D3);

DigitalOut trigger_2(D4);
DigitalIn  echo_2(D5);

DigitalOut trigger_3(D9);
DigitalIn  echo_3(D10);

BufferedSerial mbed_uart(D1, D0, 9600); // tx, rx

PwmOut servo1(A1);


int measured_distance_1 = 0;
int measured_distance_2 = 0;
int measured_distance_3 = 0;

int correction = 0;

int ultrasonic_output;

//char *c;

Timer sonar;

void send_command(const char* command) {
    mbed_uart.write(command, strlen(command));  // Send the command
    //char delimiter = '\n';
    //mbed_uart.write(&delimiter, sizeof(delimiter));  // Send newline as delimiter
    printf("Command sent: %s\n", command);
}


int main()
{   
    servo1.period_ms(20);
    servo1.write(0.05);//这个角度大概是30°
    // servo1.write(0.035);，如果30°偏大可以尝试这个，大概是25°-20°

    sonar.reset();
// measure actual software polling timer delays
// delay used later in time correction
// start timer
    sonar.start();
// min software polling delay to read echo pin
    while (echo_1==2) {};

// stop timer
    sonar.stop();
// read timer
    correction = duration_cast<microseconds>(sonar.elapsed_time()).count();
    printf("Approximate software overhead timer delay is %d uS\n\r",correction);

//Loop to read Sonar distance values, scale, and print
    while(1) {
// trigger sonar to send a ping
        trigger_1 = 1;

        sonar.reset();
        wait_us(10.0);
        trigger_1 = 0;

//wait for echo high
        while (echo_1==0) {};

//echo high, so start timer
        sonar.start();
//wait for echo low
        while (echo_1==1) {};
//stop timer and read value
        sonar.stop();
//subtract software overhead timer delay and scale to cm
        if ((duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)>= 2353) //40cm*2/100/340*1000*1000=2353 (us)
        {
            measured_distance_1 = 40;
        }
        else if ((duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)<= 118) //2cm*2/100/340*1000*1000=118 (us)
        {
            measured_distance_1 = 2;
        }
        else
        {
        measured_distance_1 = (duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)/58.0;
        }


//////////////////////////////////////////////////////////////////////
        // trigger sonar to send a ping
        trigger_2 = 1;

        sonar.reset();
        wait_us(10.0);
        trigger_2 = 0;

//wait for echo high
        while (echo_2==0) {};

//echo high, so start timer
        sonar.start();
//wait for echo low
        while (echo_2==1) {};
//stop timer and read value
        sonar.stop();
//subtract software overhead timer delay and scale to cm
        if ((duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)>= 2353) //40cm*2/100/340*1000*1000=2353 (us)
        {
            measured_distance_2 = 40;
        }
        else if ((duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)<= 118) //2cm*2/100/340*1000*1000=118 (us)
        {
            measured_distance_2 = 2;
        }
        else
        {
        measured_distance_2 = (duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)/58.0;
        }

        // trigger sonar to send a ping
        trigger_3 = 1;

        sonar.reset();
        wait_us(10.0);
        trigger_3 = 0;

//wait for echo high
        while (echo_3==0) {};

//echo high, so start timer
        sonar.start();
//wait for echo low
        while (echo_3==1) {};
//stop timer and read value
        sonar.stop();
//subtract software overhead timer delay and scale to cm
        if ((duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)>= 2353) //40cm*2/100/340*1000*1000=2353 (us)
        {
            measured_distance_3 = 40;
        }
        else if ((duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)<= 118) //2cm*2/100/340*1000*1000=118 (us)
        {
            measured_distance_3 = 2;
        }
        else
        {
        measured_distance_3 = (duration_cast<microseconds>(sonar.elapsed_time()).count()-correction)/58.0;
        }


        printf(" measured_distance_1 is: %d cm \n\r",measured_distance_1);
//wait so that any echo(s) return before sending another ping
        printf(" measured_distance_2 is: %d cm \n\r",measured_distance_2);
//wait so that any echo(s) return before sending another ping
        printf(" measured_distance_3 is: %d cm \n\r",measured_distance_3);
//        ultrasonic_output = measured_distance_2 - measured_distance_1;


        /*char buffer[32];
        sprintf(buffer, "%d\r\n", ultrasonic_output);  // 将整数转换为字符串并添加换行符
        mbed_uart.write(buffer, sizeof(buffer));       // 发送字符串
        printf("%c \n",buffer);*/
//        mbed_uart.write(&ultrasonic_output, sizeof(ultrasonic_output));
        // 发送分隔符，例如换行符
//        char delimiter = '\n';
//        mbed_uart.write(&delimiter, sizeof(delimiter));

        /*char buffer[4];
        snprintf(buffer, sizeof(buffer), "%d", ultrasonic_output);
        mbed_uart.write(&buffer, sizeof(buffer));*/

        //mbed_uart.read(c, sizeof(c));
        //printf("%c \n", *c);

//        printf(" ultrasonic_output is: %d cm \n\r",ultrasonic_output);


//        printf("\n");


        // Compare distances and decide direction
        if (measured_distance_3 <35) {  // Threshold can be adjusted
            send_command("Righ");
        } else if (measured_distance_1 <35) {
            send_command("Left");
        } else if (measured_distance_2 <35) {
            send_command("Midd");
        } else {
            send_command("Stay");
        }

        if (mbed_uart.readable()) {
            char gate_control_data;
            mbed_uart.read(&gate_control_data, 1);
            //pc.write(&gate_control_data, 1);

            // 如果接收到 "open" 信号，则设置引脚 A1 转至90度，开门
            if (gate_control_data=='u') {
                //printf("open\r\n");

                mbed_uart.write("u", 1);

            }

            // 如果接收到 "close" 信号，则设置引脚 A1 转至0度，关门
            else if (gate_control_data=='d') {
                //printf("open\r\n");

                mbed_uart.write("d", 1);

            }
        }

        thread_sleep_for(100);

    }
}

