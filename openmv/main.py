import sensor, image, time, math, struct
import ustruct
import car
from pyb import UART
from pyb import LED
from pid import PID
import pyb

input_pin1 = pyb.Pin('P6', pyb.Pin.IN, pyb.Pin.PULL_UP)
input_pin2 = pyb.Pin('P9', pyb.Pin.IN, pyb.Pin.PULL_UP)
state_pin1 = input_pin1.value()
state_pin2 = input_pin2.value()
#print("Pin P6 state:", state_pin1)
#print("Pin P9 state:", state_pin2)

theta_pid = PID(p=0.45, i=0.2)
ultrasonic_pid = PID(p=0.45, i=0.2)
THRESHOLD = (20, 100, -80, 70, -21, 90)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

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

ROIS_HIGH =(0, 211, 320, 30)


ROIS_MID =(0, 121, 320, 30)


grid = (6, 100, -22, 10, 19, 60)
tree = (9, 91, -77, -23, -128, 127)
duration = 2
direction = 0

weight_sum = 0
for r in ROIS: weight_sum += r[4]
clock.tick()

while (True):
    s = 1
    if s == 1:
        img = sensor.snapshot()
        img.rotation_corr(z_rotation=180)


        if input_pin1.value() == 1 and input_pin2.value() == 0:
            direction = 1
        elif input_pin1.value() == 0 and input_pin2.value() == 1:
            direction = 10


#        for roi in ROIS_HIGH:
#            blobs_tree_high = img.find_blobs([tree], roi = roi, pixels_threshold=100, area_threshold=100, merge=True)
#            while blobs_tree_high:
#                car,run(20,20)


        blobs_tree_mid = img.find_blobs([tree], roi = ROIS_MID, pixels_threshold=100, area_threshold=100, merge=True)
#                for blob in blobs_tree:
#                    img.draw_rectangle(blob.rect())
#                    img.draw_cross(blob.cx(), blob.cy())
        if blobs_tree_mid:
            print(1000)
            if direction == 1: # see right(actually turn left)
                print(3000)
                start_time = time.time()
                while(time.time()-start_time < duration):
                    car.run(20, 0)
                direction = 0

            elif direction == 10: # see left(actually turn right)
                print(2000)
                start_time = time.time()
                while(time.time()-start_time < duration):
                    car.run(0, 20)
                direction = 0

#        for roi in ROIS_GRID:
#            blobs = img.find_blobs([grid], roi=roi, pixels_threshold=100, area_threshold=100, merge=True)
#            if blobs:
#                for blob in blobs:
#                    img.draw_rectangle(blob.rect())
#                    img.draw_cross(blob.cx(), blob.cy())
            while input_pin1.value() == 0 and input_pin2.value() == 0:
                car.run(0, 0)
                print(input_pin1.value())


        sensor.set_auto_whitebal(False, rgb_gain_db=(1.0, 1.0, 100.0))
        sensor.set_auto_exposure(False, exposure_us = 5000)
        sensor.set_auto_gain(False, gain_db = 50.0)


        #img.rotation_corr(z_rotation=180)  # 保留图像旋转设置
        centroid_sum = 0
        for r in ROIS:
            blobs = img.find_blobs([THRESHOLD], roi=r[0:4], merge=True)
            if blobs:
                largest_blob = 0
                most_pixels = 0
                for i in range(len(blobs)):
                    if blobs[i].pixels() > most_pixels:
                        most_pixels = blobs[i].pixels()
                        largest_blob = i
                img.draw_rectangle(blobs[largest_blob].rect(), color=(128+int(255*r[4]), 128+int(255*r[4]), 0), thickness=1)
                img.draw_cross(blobs[largest_blob].cx(), blobs[largest_blob].cy(), color=(128+int(255*r[4]), 128+int(255*r[4]), 0), thickness=1)
                centroid_sum += blobs[largest_blob].cx() * r[4]

        center_pos = (centroid_sum / weight_sum)
        deflection_angle = -math.atan((center_pos - 160) / 10)
        deflection_angle = math.degrees(deflection_angle)
        output = theta_pid.get_pid(deflection_angle, 1)
        car.run(20 + output, 20 - output)

