# This is the main program of Patio 1 tasks
# presneted by Team 40 Shiny Pinky in June 2021
#from pyb import Servo
#s3 = Servo(3) # P9

#s3.angle(-50)
import sensor, image, time, math, struct
import ustruct
import car
from pyb import UART
from pyb import LED
from pid import PID
import pyb
# includes encapsulated files of direction control (PID) algorithm to enable direct use of defined fucntions, variables and constants
#from acc_2 import turn_angle

# includes encapsulated files of accelerometer to enable direct use of defined fucntions, variables and constantsfrom ultrasonic import distanceMeasure
# includes encapsulated files of accelerometer to enable direct use of defined fucntions, variables and constants


#LED(1).on()
#LED(2).on()
#LED(3).on()
input_pin1 = pyb.Pin('P6', pyb.Pin.IN, pyb.Pin.PULL_UP)
input_pin2 = pyb.Pin('P9', pyb.Pin.IN, pyb.Pin.PULL_UP)


theta_pid = PID(p=0.45, i=0.2)
ultrasonic_pid = PID(p=0.45, i=0.2)
THRESHOLD =(0, 100, -56, 17, -7, 127)
# THRESHOLD = (20, 100, -80, 70, -21, 90)
# task123版本阈值
# initializes the PI controller and envalues the parameters

#thresh = [(30, 79, -7, 30, 6, 23)]
#THRESHOLD = (6, 68, -25, 22, -56, -11) # Grayscale threshold for dark things...
#THRESHOLD = (9, 68, -30, 32, -57, -16)

#THRESHOLD =(20, 62, -18, 36, -65, -8)
#THRESHOLD =(0, 100, -128, 101, -16, 127)#old_dog
#GRAYSCALE_THRESHOLD = (95, 255)
#5.27 THRESHOLD =(20, 100, -80, 70, -21, 90)
sensor.reset()  # resets and initializes the sensor.
sensor.set_pixformat(sensor.RGB565)  # sets pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # sets frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # waits for settings take effect.
clock = time.clock()  # creates a clock object to track the FPS.
#sensor.set_auto_gain(False)           # 打开自动增益, 默认打开；追踪颜色，则需关闭白平衡。
#sensor.set_auto_whitebal(False)       # 打开（True）或关闭（False）自动白平衡。默认打开；追踪颜色，则需关闭白平衡
#sensor.set_auto_exposure(False, exposure_us=2000)       # 打开（True）或关闭（False）自动曝光。默认打开。
#sensor.set_auto_whitebal(False, rgb_gain_db = (0.0, 0.0, 100))
#sensor.set_auto_gain(False, gain_db = 20)

#sensor.set_contrast(3)      # 设置相机图像对比度。-3至+3。
#sensor.set_brightness(3)   # 设置相机图像亮度。-3至+3。
#sensor.set_saturation(3)   # 设置相机图像饱和度。-3至+3。

#black=(0, 42, -25, 22, -17, 14)
#yellow=(73, 100, -28, 9, 15, 127)
#green=(27, 46, -82, 38, 10, 49)
black=(0, 42, -25, 22, -17, 14)
yellow=(71, 100, -31, 14, 18, 99)
#green=(46, 85, -85, -5, 5, 49)
#5.31早
green=(43, 74, -77, -33, -5, 48)
green=(30, 56, -71, -20, 14, 56)
tree=(80, 15, -103, -21, -15, 64) # 关于小草坪的阈值
#red = (58, 93, 3, 58, 9, 66)
red=(36, 67, 17, 70, 13, 61)
duration = 2
direction = 0
flag_arrow = 0

#PID_flag=0

ROIS = [
    (0, 1, 320, 30, 0.1),
    (0, 31, 320, 30, 0.2),
    (0, 61, 320, 30, 0.3),
    (0, 91, 320, 30, 0.4),
    (0, 121, 320, 30, 0.5),
    (0, 151, 320, 30, 0.5),
    (0, 181, 320, 30, 0.2),
    (0, 211, 320, 30, 0.1)
]
ROIS_MID =(0, 1, 320, 30)
#5.31早9：00测量
timer_triggered = False
timer_yellow_trigger = 0
'''来自task123 line:41-46'''
#ROIS = [
# (10, 50, 300, 30 ,0.15),
# (10, 100, 300, 30, 0.15),
# (10, 150, 300, 30, 0.3),
# (10, 200, 300, 30, 0.4)
# ]
# # defines four regions of interest





#ROIS = [
#    (0, 1, 160, 15, 0.1),
#    (0, 16, 160, 15, 0.2),
#    (0, 31, 160, 15, 0.3),
#    (0, 46, 160, 15, 0.4),
#    (0, 61, 160, 15, 0.5),
#    (0, 76, 160, 15, 0.5),
#    (0, 91, 160, 15, 0.2),
#    (0, 106, 160, 15, 0.1)
#]

# defines 8 regions of interest (test)
weight_sum = 0  # initializes weight values
for r in ROIS: weight_sum += r[4]  # defines calculation for weigted
clock.tick()  # initiates timer
#uart = UART(3, 9600, timeout=10,timeout_char=0,read_buf_len=3)
uart = UART(3, 9600, timeout_char=1000)
rx = "Stay"

while (True):

    s = 1
    if s == 1:

        img = sensor.snapshot()#.binary([THRESHOLD])
        img.rotation_corr(z_rotation=180)  # rectify the image because it is shot upside down



        yellow_blobs = img.find_blobs([yellow],roi=[0, 181, 320, 60],pixels_threshold=1000)
        if yellow_blobs:
        #如果找到了目标颜色
        #            print("Found {} black blob(s).".format(len(black_blobs)))
            for y in yellow_blobs:
         #迭代找到的目标颜色区域
               # Draw a rect around the blob.
               img.draw_rectangle(y[0:4],color=(0,0,0)) # rect
              #用矩形标记出目标颜色区域
               img.draw_cross(y[5], y[6]) # cx, cy
            timer_yellow_trigger = 1
            #print("yellow_trigger is success")
        print(timer_yellow_trigger)

        if (timer_yellow_trigger == 0) :
            if input_pin1.value() == 1 and input_pin2.value() == 0:
                direction = 1
                flag_arrow = 1
                print(direction)
            elif input_pin1.value() == 0 and input_pin2.value() == 1:
                direction = 10
                flag_arrow = 1
                print(direction)
            blobs_tree_mid = img.find_blobs([tree], roi=ROIS_MID, pixels_threshold=400, area_threshold=400, merge=True)
            if blobs_tree_mid:
                # for blob in blobs_tree_mid:
                # Draw a rectangle around each blob
                # img.draw_rectangle(blob.rect(), color=(8128, 128, 0), thickness=100)
                print("tree")
                if direction==1:
                    print("right")
                    start_time = time.time()
                    while (time.time() - start_time < duration):
                        car.run(20, 0)
                    direction = 0
#                    PID_flag = 1

                elif direction == 10:  # see left(actually turn right)
                    print("left")
                    start_time = time.time()
                    while (time.time() - start_time < duration):
                        car.run(0, 20)
                    direction = 0
#                    PID_flag = 1

            while input_pin1.value() == 0 and input_pin2.value() == 0:
                car.run(0, 0)
#                print(input_pin1.value())

            sensor.set_auto_whitebal(False, rgb_gain_db=(1.0,1.0,100.0))
            sensor.set_auto_exposure(False, exposure_us=5000)
            sensor.set_auto_gain(False, gain_db=50.0)

            centroid_sum = 0
            # initializes the weighted distance from centroids to the central line
            for r in ROIS:  # for each centroid of ROI
                # blobs = img.find_blobs([GRAYSCALE_THRESHOLD], roi=r[0:4], merge=True)
                blobs = img.find_blobs([THRESHOLD], roi=r[0:4], merge=True)
                # r[0:4] is roi tuple.
                # finds all white spots and merge as one (connecting each other with lines)
                # searching for lines in ROI

                if blobs:
                    # indentifies the bolb index with the most lines
                    largest_blob = 0
                    most_pixels = 0
                    for i in range(
                            len(blobs)):  # there might be several line clusters in ROI, but identify the larges as the target line

                        if blobs[i].pixels() > most_pixels:
                            most_pixels = blobs[i].pixels()
                            # update the value if there is any larger pixel clusters

                            largest_blob = i

                            img.draw_rectangle(blobs[largest_blob].rect(), color=(128+int(255*r[4]),128+int(255*r[4]),0),thickness=1)
                    # draws a rectangle around the largest pixel cluster

                            img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy(), color = (128+int(255*r[4]),128+int(255*r[4]),0), thickness=1)
                    # marks the largest pixel cluster with a white cross

                    centroid_sum += blobs[largest_blob].cx() * r[4]
                    # accumulates the weighted distances to obtain the final result

            center_pos = (centroid_sum / weight_sum)  # determines the center of line

            # converts the result above to an angle, using unlinear operations

            deflection_angle = 0
            # initializes the angle to turn for the robot
#            if PID_flag == 0:
#                deflection_angle = -math.atan((center_pos - 160) / 20)
#            else:
#                deflection_angle = -math.atan((center_pos - 160) / 30)


            deflection_angle = -math.atan((center_pos - 160) / 20)
            # obtains the result (in radian)

            deflection_angle = math.degrees(deflection_angle)
            # converts result to degrees

            output = theta_pid.get_pid(deflection_angle, 1)
            '''公共部分：图像采集，output输出'''
            car.run(30 + output, 30 - output)


        elif(timer_yellow_trigger != 0):
#            sensor.set_auto_whitebal(False, rgb_gain_db=(1.0,1.0,1.0))
#            sensor.set_auto_exposure(False, exposure_us=5000)
#            sensor.set_auto_gain(False, gain_db=50.0)
            centroid_sum = 0
            # initializes the weighted distance from centroids to the central line
            for r in ROIS:  # for each centroid of ROI
                # blobs = img.find_blobs([GRAYSCALE_THRESHOLD], roi=r[0:4], merge=True)
                blobs = img.find_blobs([THRESHOLD], roi=r[0:4], merge=True)
                # r[0:4] is roi tuple.
                # finds all white spots and merge as one (connecting each other with lines)
                # searching for lines in ROI

                if blobs:
                    # indentifies the bolb index with the most lines
                    largest_blob = 0
                    most_pixels = 0
                    for i in range(
                            len(blobs)):  # there might be several line clusters in ROI, but identify the larges as the target line

                        if blobs[i].pixels() > most_pixels:
                            most_pixels = blobs[i].pixels()
                            # update the value if there is any larger pixel clusters

                            largest_blob = i

                    #                img.draw_rectangle(blobs[largest_blob].rect(), color=(128+int(255*r[4]),128+int(255*r[4]),0),thickness=1)
                    # draws a rectangle around the largest pixel cluster

                    #                img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy(), color = (128+int(255*r[4]),128+int(255*r[4]),0), thickness=1)
                    # marks the largest pixel cluster with a white cross

                    centroid_sum += blobs[largest_blob].cx() * r[4]
                    # accumulates the weighted distances to obtain the final result

            center_pos = (centroid_sum / weight_sum)  # determines the center of line

            # converts the result above to an angle, using unlinear operations

            deflection_angle = 0
            # initializes the angle to turn for the robot

            deflection_angle = -math.atan((center_pos - 160) / 20)
            # obtains the result (in radian)

            deflection_angle = math.degrees(deflection_angle)
            # converts result to degrees

            output = theta_pid.get_pid(deflection_angle, 1)
            '''公共部分：图像采集，output输出'''

#            while input_pin1.value() == 0 and input_pin2.value() == 0:
#                car.run(0, 0)
##                print(input_pin1.value())

            if uart.any():
                rx = uart.readline().decode().strip()
                # rx=uart.readline().decode()#.strip()
            #            ultrasonic_output, = struct.unpack('<i', rx)  # 假设发送端是小端字节序
            print(rx)

            '''yellow_trigger的符号'''

            black_blobs = img.find_blobs([black],pixels_threshold=300)

            if black_blobs and len(black_blobs) > 3:
            #如果找到了目标颜色
                print("{} blob(s).".format(len(black_blobs)))
                for b in black_blobs:
                #迭代找到的目标颜色区域
                    # Draw a rect around the blob.
                    img.draw_rectangle(b[0:4]) # rect
                    #用矩形标记出目标颜色区域
                    img.draw_cross(b[5], b[6]) # cx, cy
                    #在目标颜色区域的中心画十字形标记

                if len(black_blobs) > 3 and not timer_triggered:
                    origin_time = time.time()  # 记录当前时间
                    while time.time() - origin_time < 3:  # 持续检查时间是否已过1秒
                        car.run(0,0)
                    timer_triggered = True  # 标记计时已经执行，防止再次执行
                    print (" time trigger is success(done)")


                if (timer_triggered==True):
                    if (rx=="Stay"):
            #            car.run(30 + output , 30 - output)
                        car.run(15,11)
                    elif (rx=="Left"):
                        car.run(0,0)
                        time.sleep(3.0)
                    elif (rx=="Righ"):
                        car.run(0,0)
                        time.sleep(3.0)
                    elif (rx=="Midd"):
                        car.run(0,0)
                        time.sleep(3.0)
                    else:
                        car.run(0,0)


            elif (rx=="Stay"):
    #            car.run(30 + output , 30 - output)
                car.run(20+output,20-output)
            elif (rx=="Left"):

    #            uart = UART(3, 9600, timeout_char=1000)
     #            uart.readline()
     #            rx=uart.readline().decode().strip()
     #            print(rx)
                 car.run(0,0)
                 time.sleep(0.3)
                 while uart.any():
                     uart.readline()
                 car.run(0,-30)
                 time.sleep(2.0)
                 car.run(40,40)
                 '''左转出弯，往前开五秒，5（3）'''
                 time.sleep(3.0)
                 # time.sleep(3.0)

                 car.run(-30,0)
                 time.sleep(1.7) #回正方向，左右转方向不一样

                 '''直行段落，假设20s（2s）'''
                 car.run(40,40)
                 time.sleep(4.0)
                 # time.sleep(2.0)

                 car.run(-30,0)
                 time.sleep(1.7)

                 '''右转出弯，往前开五秒，5（3）'''
                 car.run(40,40)
                 time.sleep(2.5)
                 # time.sleep(3.0)
                 car.run(0,-30)
                 time.sleep(1.5)
                 #            car.run(20,20)
                 #            time.sleep(1.0)

                 rx=="Stay"

            elif (rx=="Righ"):

                car.run(0,0)
                time.sleep(0.3)
                while uart.any():
                    uart.readline()
                car.run(0,-30)
                time.sleep(2.0)
                car.run(40,40)
                '''左转出弯，往前开五秒，5（3）'''
                time.sleep(3.0)
                # time.sleep(3.0)

                car.run(-30,0)
                time.sleep(1.7) #回正方向，左右转方向不一样

                '''直行段落，假设20s（2s）'''
                car.run(40,40)
                time.sleep(4.0)
                # time.sleep(2.0)

                car.run(-30,0)
                time.sleep(1.7)

                '''右转出弯，往前开五秒，5（3）'''
                car.run(40,40)
                time.sleep(2.5)
                # time.sleep(3.0)
                car.run(0,-30)
                time.sleep(1.5)
                #            car.run(20,20)
                #            time.sleep(1.0)

                rx=="Stay"

            elif (rx=="Midd"):


                car.run(0,0)
                time.sleep(0.3)
                while uart.any():
                    uart.readline()
                car.run(0,-30)
                time.sleep(2.0)
                car.run(40,40)
                '''左转出弯，往前开五秒，5（3）'''
                time.sleep(3.0)
                # time.sleep(3.0)

                car.run(-30,0)
                time.sleep(1.7) #回正方向，左右转方向不一样

                '''直行段落，假设20s（2s）'''
                car.run(40,40)
                time.sleep(4.0)
                # time.sleep(2.0)

                car.run(-30,0)
                time.sleep(1.7)

                '''右转出弯，往前开五秒，5（3）'''
                car.run(40,40)
                time.sleep(2.5)
                # time.sleep(3.0)
                car.run(0,-30)
                time.sleep(1.5)
                #            car.run(20,20)
                #            time.sleep(1.0)

                rx=="Stay"

            else:
    #            car.run(30+output , 30+output)
                car.run(20+output,20-output)

            '''我这里UART程序发送"u/n"'''
            green_blobs = img.find_blobs([green],roi=[0, 60, 320, 120],pixels_threshold=8000)
            red_blobs = img.find_blobs([red],roi=[0,61,320,180], pixels_threshold=1000)
            print(timer_yellow_trigger)
            if green_blobs and timer_yellow_trigger==1:
               car.run(20,20) # 进入绿色区域
               time.sleep(3)
               car.run(0,0)
               time.sleep(3)
               timer_yellow_trigger=2

            if timer_yellow_trigger==2:
                if not red_blobs:
                    car.run(20+output,20-output)
                    uart.write("u\n")
                else:
                    car.run(0,0)
                    uart.write("d\n")
                    time.sleep(3)
            #如果找到了目标颜色
            #            print("Found {} black blob(s).".format(len(black_blobs)))
            #在目标颜色区域的中心画十字形标记
    #            car.run(0,0)
               # for g in  green_blobs:
             #迭代找到的目标颜色区域
                   # Draw a rect around the blob.
                   #img.draw_rectangle(g[0:4],color=(0, 255, 0)) # rect
                  #用矩形标记出目标颜色区域
                   #img.draw_cross(g[5], g[6]) # cx, cy




