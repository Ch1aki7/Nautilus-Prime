from media.display import *       # K230 显示驱动库（控制 LCD/HDMI）
from media.media import *         # K230 媒体管理库（管理显示缓冲区等资源）
from media.sensor import *
import time, os, sys, gc, urandom      # 系统工具库（时间、文件、内存回收）
import lvgl as lv                 # 嵌入式 GUI 库（LVGL，负责 UI 渲染与交互）
from machine import TOUCH         # K230 触摸设备驱动（读取触摸坐标）

DISPLAY_WIDTH = ALIGN_UP(800, 16)  # 800 对齐后仍为 800（800 % 16 = 0）
DISPLAY_HEIGHT = 480               # 固定高度 480

# def display_init():
#     Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
#     MediaManager.init()

# def display_deinit():
#     os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)  # 启用系统休眠出口点
#     time.sleep_ms(50)                        # 延迟 50ms 等待资源释放
#     Display.deinit()                         # 关闭显示驱动
#     MediaManager.deinit()                    # 释放媒体资源（缓冲区等）

def display_test():
    print("display test")

    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.ARGB8888)
    src_img = image.Image("/data/pokedex.bmp")
    # sensor = Sensor()
    # sensor.reset()

    Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
    MediaManager.init()

    try:
        menu_collect = 3 # 当前选中哪个模式
        chosen_color = 0
        input_text = ""
        key_chosen_flag = True
        flag = 2 # 当前在哪个模式里 -1为初始
        key_chosen=20 # 输入界面里的键位选择

        while True:
            img.clear()
            img.draw_string_advanced(95, 25, 80, "NAUTILUS-PRIME", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            img.draw_string_advanced(265, 385, 30, "Press Any Key to Start", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            img.draw_string_advanced(225, 425, 40, "Presented by Zaphkiel", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            #img.draw_image(src_img, 350, 200)
            #暂时无效，原因未知，只能用Display
            if flag == -1:
                Display.show_image(src_img,x=350,y=200,layer = Display.LAYER_OSD1)


            chosen_color=255-chosen_color

            # 选中视觉效果
            if menu_collect == 1:
                img.draw_rectangle(110 , 150, 180, 100, color=(chosen_color, chosen_color, chosen_color), fill=True)
                img.draw_string_advanced(118, 150, 45, "Pokemon", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 180, 53, "Detect", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_rectangle(110, 150, 180, 100,color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                img.draw_rectangle(110, 280, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(119, 280, 45, "Pokemon", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 310, 53, "Browse", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(510, 150, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(519, 150, 50, "Sheikah", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 185, 50, "  Stone", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(510, 280, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(519, 270, 53, "Super", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 320, 53, "  Earth", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            elif menu_collect==2:
                img.draw_rectangle(110, 150, 180, 100,color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(118, 150, 45, "Pokemon", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 180, 53, "Detect", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(110, 280, 180, 100, color=(chosen_color, chosen_color, chosen_color), fill=True)
                img.draw_string_advanced(119, 280, 45, "Pokemon", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 310, 53, "Browse", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_rectangle(110, 280, 180, 100, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                img.draw_rectangle(510, 150, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(519, 150, 50, "Sheikah", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 185, 50, "  Stone", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(510, 280, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(519, 270, 53, "Super", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 320, 53, "  Earth", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            elif menu_collect == 3:
                img.draw_rectangle(110, 150, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(118, 150, 45, "Pokemon", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 180, 53, "Detect", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(110, 280, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(119, 280, 45, "Pokemon", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 310, 53, "Browse", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(510, 150, 180, 100, color=(chosen_color, chosen_color, chosen_color), fill=True)
                img.draw_string_advanced(519, 150, 50, "Sheikah", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 185, 50, "  Stone", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_rectangle(510, 150, 180, 100, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                img.draw_rectangle(510, 280, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(519, 270, 53, "Super", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 320, 53, "  Earth", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            elif menu_collect == 4:
                img.draw_rectangle(110, 150, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(118, 150, 45, "Pokemon", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 180, 53, "Detect", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(110, 280, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(119, 280, 45, "Pokemon", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(119, 310, 53, "Browse", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(510, 150, 180, 100, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(519, 150, 50, "Sheikah", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 185, 50, "  Stone", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(510, 280, 180, 100, color=(chosen_color, chosen_color, chosen_color), fill=True)
                img.draw_string_advanced(519, 270, 53, "Super", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(519, 320, 53, "  Earth", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_rectangle(510, 280, 180, 100, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

            # 进入查找模式
            if flag == 2:
                img.clear()
                # 绘制输入框
                img.draw_rectangle(160, 10, 500, 50, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(40, 10, 45, "Input:", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(170, 10, 40, "text", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                # QWERTY键盘布局
                keys = [
                    "QWERTYUIOP",
                    "ASDFGHJKL",
                    "ZXCVBNM"
                ]

                key_width = 60
                key_height = 60
                margin = 10

                count=0
                for row, key_row in enumerate(keys):
                    for col, the_key in enumerate(key_row):
                        if count!=19:
                            count+=1
                        else:
                            count+=2

                        x = col * (key_width + margin) + 10 + row*10
                        y = row * (key_height + margin) + 270
                        if key_chosen==count:
                            img.draw_rectangle(x, y, key_width, key_height, color=(255, 255, 255),fill=True)
                            img.draw_string(x + 5, y + 5, the_key, color=(0, 0, 0), scale=2)
                        else:
                            img.draw_rectangle(x, y, key_width, key_height, color=(255, 255, 255))
                            img.draw_string(x + 5, y + 5, the_key, color=(255, 255, 255), scale=2)
                del keys
                gc.collect()

                # 制作功能键 一二三行末尾分别是：(710,270)(650，340)(520，410)
                if key_chosen==20:
                    img.draw_rectangle(650, 340, 120, key_height, color=(255, 255, 255),fill=True)
                    #img.draw_string(650, 340, "Random", color=(0, 0, 0), scale=2)
                    img.draw_string_advanced(660, 340, 30,"Random", color=(0, 0, 0), font="/sdcard/res/font/ChillBitmap7x.ttf")
                else:
                    img.draw_rectangle(650, 340, 120, key_height, color=(255, 255, 255))
                    img.draw_string_advanced(660, 340, 30,"Random", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if key_chosen == 28:
                    img.draw_rectangle(520, 410, 190, key_height, color=(255, 255, 255), fill=True)
                    img.draw_string_advanced(530, 410, 30, "<- Backspace", color=(0, 0, 0), font="/sdcard/res/font/ChillBitmap7x.ttf")
                else:
                    img.draw_rectangle(520, 410, 190, key_height, color=(255, 255, 255))
                    img.draw_string_advanced(530, 410, 30, "<- Backspace", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")


            Display.show_image(img)

            time.sleep(0.5)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")

    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()

