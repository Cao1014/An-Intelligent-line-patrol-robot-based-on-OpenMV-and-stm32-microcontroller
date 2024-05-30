# Untitled - By: zrn - Sun Mar 3 2024

import sensor, image, time,math

def color_detection(color):

    threshold_index = 0 #0 for red, 1 for green, 2 for blue 设置颜色的阈值 阈值可通过图片/camera的图像自动产生，
    #在工具-机器视觉-阈值编辑器之中,拖动下方多个滑块，使得右侧图像中需要识别的部分呈现为白色即可
    #后续实践之中阈值应该通过实时摄像头返回的图像进行识别
    red = (100, 20, 42, 76, -67, 127) #红色阈值
    yellow = (9, 100, 6, 71, 17, 111)#黄色阈值
    green = (38, 91, -78, -28, -128, 127)#绿色阈值

    clock = time.clock()

    #while(True):
    clock.tick()
    img = sensor.snapshot() #截取一张图像

    #函数解释：blob意思是“色块”，即在截图中提取符合要求的色块并返回blob列表 （find_blobs:提取、识别多个色块）
    # threshold为颜色的阈值，通过之前defined index来索引
    # roi 是对图像的感兴趣区域进行识别，不设置则默认为对整个图像进行识别
    # x_stride： 默认为2 即查找色块的x方向上最小宽度的像素
    # y_stride: 默认为1，其余理同
    # invert:阈值反转，即阈值以外的颜色会被查找
    # area_threshold:方框面积阈值，若色块面积小于该阈值则会被过滤掉
    # merge：合并，即所有被识别到的颜色将被合并进入一个方框之中
    blobs = []

    # Detect blobs for each color range and append them to the blobs list
    for color in [red, yellow, green]:
        new_blob = img.find_blobs([color], pixels_threshold=200, area_threshold=100)
        blobs.append(new_blob)

    max_brightness = 0
    brightest_blob = None
    brightest_blob_index = 0

    # Iterate over the lists of blobs for each color
    for i, color_blobs in enumerate(blobs):
     # Check if blobs were found for this color range
        if color_blobs:
            # Iterate over the blobs for this color range
            for blob in color_blobs:
                # Get statistics for the current blob
                stats = img.get_statistics(roi=blob.rect())

                # Update the maximum brightness and corresponding blob
                if stats.l_max() > max_brightness:
                    max_brightness = stats.l_max()
                    brightest_blob = blob
                    brightest_blob_index = i

    if (brightest_blob):
        img.draw_rectangle(brightest_blob.rect()) #blob.rect:返回色块的外框——一元矩阵，image画出来
        img.draw_cross(brightest_blob.cx(),brightest_blob.cy()) #blob.x:返回外框的x坐标 和blob[0]一样 blob.cx():返回色块的中心的x坐标
        color = brightest_blob_index #0: red 1: yellow 2: green

    return color


