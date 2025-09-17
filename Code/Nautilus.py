from media.display import *       # K230 显示驱动库（控制 LCD/HDMI）
from media.media import *         # K230 媒体管理库（管理显示缓冲区等资源）
from media.sensor import *
import time, os, sys, gc, urandom, utime      # 系统工具库（时间、文件、内存回收）
import lvgl as lv                 # 嵌入式 GUI 库（LVGL，负责 UI 渲染与交互）
from machine import TOUCH         # K230 触摸设备驱动（读取触摸坐标）
from machine import Pin
from machine import FPIOA
from machine import Timer

# AI识别模块
from libs.YOLO import YOLOv5
from libs.Utils import *
import os,sys,gc
import ulab.numpy as np
import image

DISPLAY_WIDTH = ALIGN_UP(800, 16)  # 800 对齐后仍为 800（800 % 16 = 0）
DISPLAY_HEIGHT = 480               # 固定高度 480

kmodel_path="/data/best.kmodel"
model_input_size=[224,224]
confidence_threshold = 0

can_touch = 1

sensor_id = 2
sensor = None

#def init_uart():
fpioa = FPIOA()

# 上下左右中
fpioa.set_function(32, FPIOA.GPIO32)
fpioa.set_function(42, FPIOA.GPIO42)
fpioa.set_function(35, FPIOA.GPIO35)
fpioa.set_function(34, FPIOA.GPIO34)
fpioa.set_function(33, FPIOA.GPIO33)

# def display_init():
#     Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
#     MediaManager.init()

# def display_deinit():
#     os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)  # 启用系统休眠出口点
#     time.sleep_ms(50)                        # 延迟 50ms 等待资源释放
#     Display.deinit()                         # 关闭显示驱动
#     MediaManager.deinit()                    # 释放媒体资源（缓冲区等）

def timer_callback(t):
    global can_touch
    can_touch = 1

def display_test():
    print("display test")
    print(gc.mem_free())
    #init_uart()
    # 2查询功能的变量数组
    labels=['abra', 'aerodactyl', 'alakazam', 'arbok', 'arcanine', 'articuno', 'beedrill', 'bellsprout', 'blastoise', 'bulbasaur', 'butterfree', 'caterpie', 'chansey', 'charizard', 'charmander', 'charmeleon', 'clefable', 'clefairy', 'cloyster', 'cubone', 'dewgong', 'diglett', 'ditto', 'dodrio', 'doduo', 'dragonair', 'dragonite', 'dratini', 'drowzee', 'dugtrio', 'eevee', 'ekans', 'electabuzz', 'electrode', 'exeggcute', 'exeggutor', 'farfetchd', 'fearow', 'flareon', 'gastly', 'gengar', 'geodude', 'gloom', 'golbat', 'goldeen', 'golduck', 'golem', 'graveler', 'grimer', 'growlithe', 'gyarados', 'haunter', 'hitmonchan', 'hitmonlee', 'horsea', 'hypno', 'ivysaur', 'jigglypuff', 'jolteon', 'jynx', 'kabuto', 'kabutops', 'kadabra', 'kakuna', 'kangaskhan', 'kingler', 'koffing', 'krabby', 'lapras', 'lickitung', 'machamp', 'machoke', 'machop', 'magikarp', 'magmar', 'magnemite', 'magneton', 'mankey', 'marowak', 'meowth', 'metapod', 'mew', 'mewtwo', 'moltres', 'mr-mime', 'muk', 'nidoking', 'nidoqueen', 'nidoran-f', 'nidoran-m', 'nidorina', 'nidorino', 'ninetales', 'oddish', 'omanyte', 'omastar', 'onix', 'paras', 'parasect', 'persian', 'pidgeot', 'pidgeotto', 'pidgey', 'pikachu', 'pinsir', 'poliwag', 'poliwhirl', 'poliwrath', 'ponyta', 'porygon', 'primeape', 'psyduck', 'raichu', 'rapidash', 'raticate', 'rattata', 'rhydon', 'rhyhorn', 'sandshrew', 'sandslash', 'scyther', 'seadra', 'seaking', 'seel', 'shellder', 'slowbro', 'slowpoke', 'snorlax', 'spearow', 'squirtle', 'starmie', 'staryu', 'tangela', 'tauros', 'tentacool', 'tentacruel', 'vaporeon', 'venomoth', 'venonat', 'venusaur', 'victreebel', 'vileplume', 'voltorb', 'vulpix', 'wartortle', 'weedle', 'weepinbell', 'weezing', 'wigglytuff', 'zapdos', 'zubat']
    pokemon_lables = [f"{i:04d}" for i in range(1, 387)]
    pokemon_linkname=['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill', 'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate', 'spearow', 'fearow', 'ekans', 'arbok', 'pikachu', 'raichu', 'sandshrew', 'sandslash', 'nidoran-f', 'nidorina', 'nidoqueen', 'nidoran-m', 'nidorino', 'nidoking', 'clefairy', 'clefable', 'vulpix', 'ninetales', 'jigglypuff', 'wigglytuff', 'zubat', 'golbat', 'oddish', 'gloom', 'vileplume', 'paras', 'parasect', 'venonat', 'venomoth', 'diglett', 'dugtrio', 'meowth', 'persian', 'psyduck', 'golduck', 'mankey', 'primeape', 'growlithe', 'arcanine', 'poliwag', 'poliwhirl', 'poliwrath', 'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell', 'victreebel', 'tentacool', 'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta', 'rapidash', 'slowpoke', 'slowbro', 'magnemite', 'magneton', 'farfetchd', 'doduo', 'dodrio', 'seel', 'dewgong', 'grimer', 'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix', 'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb', 'electrode', 'exeggcute', 'exeggutor', 'cubone', 'marowak', 'hitmonlee', 'hitmonchan', 'lickitung', 'koffing', 'weezing', 'rhyhorn', 'rhydon', 'chansey', 'tangela', 'kangaskhan', 'horsea', 'seadra', 'goldeen', 'seaking', 'staryu', 'starmie', 'mr-mime', 'scyther', 'jynx', 'electabuzz', 'magmar', 'pinsir', 'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto', 'eevee', 'vaporeon', 'jolteon', 'flareon', 'porygon', 'omanyte', 'omastar', 'kabuto', 'kabutops', 'aerodactyl', 'snorlax', 'articuno', 'zapdos', 'moltres', 'dratini', 'dragonair', 'dragonite', 'mewtwo', 'mew', 'chikorita', 'bayleef', 'meganium', 'cyndaquil', 'quilava', 'typhlosion', 'totodile', 'croconaw', 'feraligatr', 'sentret', 'furret', 'hoothoot', 'noctowl', 'ledyba', 'ledian', 'spinarak', 'ariados', 'crobat', 'chinchou', 'lanturn', 'pichu', 'cleffa', 'igglybuff', 'togepi', 'togetic', 'natu', 'xatu', 'mareep', 'flaaffy', 'ampharos', 'bellossom', 'marill', 'azumarill', 'sudowoodo', 'politoed', 'hoppip', 'skiploom', 'jumpluff', 'aipom', 'sunkern', 'sunflora', 'yanma', 'wooper', 'quagsire', 'espeon', 'umbreon', 'murkrow', 'slowking', 'misdreavus', 'unown', 'wobbuffet', 'girafarig', 'pineco', 'forretress', 'dunsparce', 'gligar', 'steelix', 'snubbull', 'granbull', 'qwilfish', 'scizor', 'shuckle', 'heracross', 'sneasel', 'teddiursa', 'ursaring', 'slugma', 'magcargo', 'swinub', 'piloswine', 'corsola', 'remoraid', 'octillery', 'delibird', 'mantine', 'skarmory', 'houndour', 'houndoom', 'kingdra', 'phanpy', 'donphan', 'porygon2', 'stantler', 'smeargle', 'tyrogue', 'hitmontop', 'smoochum', 'elekid', 'magby', 'miltank', 'blissey', 'raikou', 'entei', 'suicune', 'larvitar', 'pupitar', 'tyranitar', 'lugia', 'ho-oh', 'celebi', 'treecko', 'grovyle', 'sceptile', 'torchic', 'combusken', 'blaziken', 'mudkip', 'marshtomp', 'swampert', 'poochyena', 'mightyena', 'zigzagoon', 'linoone', 'wurmple', 'silcoon', 'beautifly', 'cascoon', 'dustox', 'lotad', 'lombre', 'ludicolo', 'seedot', 'nuzleaf', 'shiftry', 'taillow', 'swellow', 'wingull', 'pelipper', 'ralts', 'kirlia', 'gardevoir', 'surskit', 'masquerain', 'shroomish', 'breloom', 'slakoth', 'vigoroth', 'slaking', 'nincada', 'ninjask', 'shedinja', 'whismur', 'loudred', 'exploud', 'makuhita', 'hariyama', 'azurill', 'nosepass', 'skitty', 'delcatty', 'sableye', 'mawile', 'aron', 'lairon', 'aggron', 'meditite', 'medicham', 'electrike', 'manectric', 'plusle', 'minun', 'volbeat', 'illumise', 'roselia', 'gulpin', 'swalot', 'carvanha', 'sharpedo', 'wailmer', 'wailord', 'numel', 'camerupt', 'torkoal', 'spoink', 'grumpig', 'spinda', 'trapinch', 'vibrava', 'flygon', 'cacnea', 'cacturne', 'swablu', 'altaria', 'zangoose', 'seviper', 'lunatone', 'solrock', 'barboach', 'whiscash', 'corphish', 'crawdaunt', 'baltoy', 'claydol', 'lileep', 'cradily', 'anorith', 'armaldo', 'feebas', 'milotic', 'castform', 'kecleon', 'shuppet', 'banette', 'duskull', 'dusclops', 'tropius', 'chimecho', 'absol', 'wynaut', 'snorunt', 'glalie', 'spheal', 'sealeo', 'walrein', 'clamperl', 'huntail', 'gorebyss', 'relicanth', 'luvdisc', 'bagon', 'shelgon', 'salamence', 'beldum', 'metang', 'metagross', 'regirock', 'regice', 'registeel', 'latias', 'latios', 'kyogre', 'groudon', 'rayquaza', 'jirachi', 'deoxys']
    colors=[('红色',243,82,82),('蓝色',148,219,238),('绿色',170,209,94),('黄色',255,255,153),('紫色',197,150,189),('粉红色',255,221,255),('褐色',204,153,102),('黑色',187,187,187),('灰色',238,238,238),('白色',255,255,255)]
    values=[('一般',187,187,170),('格斗',187,85,68),('飞行',129,185,199),('毒',170,85,153),('地面',221,187,85),('岩石',187,170,102),('虫',170,187,34),('幽灵',142,142,187),('钢',170,170,187),('火',255,68,34),('水',51,153,255),('草',119,204,85),('电',255,204,51),('超能力',255,85,153),('冰',119,221,245),('龙',179,102,238),('恶',119,85,68),('妖精',255,170,255)]


    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.RGB565)
    pokedex_img = image.Image("/data/pokedex.bmp")

    # sensor加载
    sensor = Sensor()
    sensor.reset()
    sensor.set_framesize(width=1920, height=1080, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
    MediaManager.init()



    try:
        # 按键实例化
        key1 = Pin(32, Pin.IN, pull=Pin.PULL_UP, drive=7) # 上
        key2 = Pin(42, Pin.IN, pull=Pin.PULL_UP, drive=7) # 下
        key3 = Pin(35, Pin.IN, pull=Pin.PULL_UP, drive=7) # 左
        key4 = Pin(34, Pin.IN, pull=Pin.PULL_UP, drive=7) # 右
        key5 = Pin(33, Pin.IN, pull=Pin.PULL_UP, drive=7) # 中
        button = Pin(53, Pin.IN, Pin.PULL_DOWN)  # 使用下拉电阻

        last_key_state1=1
        last_key_state2=1
        last_key_state3=1
        last_key_state4=1
        last_key_state5=1

        menu_collect = 1 # 当前选中哪个模式
        chosen_color = 0
        input_text = ""
        key_chosen_flag = True
        flag = 1 # 当前在哪个模式里 -1为初始

        sheikah_stone = 0 # 希卡之石模式 实际为flag = 10
        super_earth = 0 # 战备呼叫模式 实际为flag = 20

        key_chosen=20 # 输入界面里的键位选择
        random_flag = 0 # 随机选择标志位
        pinyin_res_count=0
        choose_flag=0 # 查询界面选择标记
        choose_pokemon=0
        yolo_flag = 0 # 推理标记 

        read_init_flag = 0 # 详情界面标记
        linkname = "" # 存储res[0]
        form_flag = 0 #区分宝可梦形态
        form_num = 0


        # 触摸控制
        tp = TOUCH(0)
        global can_touch
        tim = Timer(-1)
        tim.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)


        # 使用IDE的帧缓冲区作为显示输出
        Display.init(Display.VIRT, width=1920, height=1080, to_ide=True)

        while True:
            # 实时获取按键
            current_key_state1 = key1.value()
            current_key_state2 = key2.value()
            current_key_state3 = key3.value()
            current_key_state4 = key4.value()
            current_key_state5 = key5.value()

            #主界面
            if flag == -1:
                img.clear()
                img.draw_string_advanced(95, 25, 80, "NAUTILUS-PRIME", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(265, 385, 30, "Press Any Key to Start", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(225, 425, 40, "Presented by Zaphkiel", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_image(pokedex_img, 310, 170, 1.5, 1.5,alpha=256)
                #暂时无效，原因未知，只能用Display
                #改变了img通道后完全解决
                #if flag == -1:
                    #Display.show_image(pokedex_img,x=350,y=200,layer = Display.LAYER_OSD1)

                # 触摸控制
                p = tp.read()
                if p != () and can_touch == 1:
                    can_touch = 0
                    if p[0].x > 110 and p[0].x < 290 and p[0].y > 150 and p[0].y < 250:
                        if menu_collect != 1:
                            menu_collect = 1
                        else:
                            flag = 1
                    if p[0].x > 110 and p[0].x < 290 and p[0].y > 280 and p[0].y < 380:
                        if menu_collect != 2:
                            menu_collect = 2
                        else:
                            flag = 2
                    if p[0].x > 510 and p[0].x < 690 and p[0].y > 150 and p[0].y < 250:
                        if menu_collect != 3:
                            menu_collect = 3
                        else:
                            flag = 3
                    if p[0].x > 510 and p[0].x < 690 and p[0].y > 280 and p[0].y < 380:
                        if menu_collect != 4:
                            menu_collect = 4
                        else:
                            flag = 4

                chosen_color=255

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
                else:
                    menu_collect = 1


            # 进入查找模式
            if flag == 2 and key_chosen_flag:
                key_chosen_flag=False
                img.clear()
                # 绘制输入框
                img.draw_rectangle(160, 10, 500, 50, color=(255, 255, 255), thickness=2)
                img.draw_string_advanced(40, 10, 45, "Input:", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(170, 10, 40, input_text, color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

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
                            img.draw_string_advanced(x + 15, y + 5, 30, the_key, color=(0, 0, 0), font="/sdcard/res/font/ChillBitmap7x.ttf")
                        else:
                            img.draw_rectangle(x, y, key_width, key_height, color=(255, 255, 255))
                            img.draw_string_advanced(x + 15, y + 5, 30, the_key, color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                del keys
                gc.collect()

                # 制作功能键 一二三行末尾分别是：(710,270)(650，340)(520，410)
                if key_chosen==20:
                    img.draw_rectangle(650, 340, 120, key_height, color=(255, 255, 255),fill=True)
                    #img.draw_string_advanced(650, 340, "Random", color=(0, 0, 0), font="/sdcard/res/font/ChillBitmap7x.ttf")
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

                # 首字母搜索 待数据集训练
                # 读取拼音数据库并解析
                with open("/data/pinyin.txt", "r",encoding='utf-8') as f:
                    pinyin_list = eval(f.read())

                pinyin_results=[]
                for i,pinyin in enumerate(pinyin_list):
                    if pinyin.startswith(input_text):
                        pinyin_results.append(i)

                result_num=len(pinyin_results)

                # 补充模糊匹配
                if result_num<10:
                    for i,pinyin in enumerate(pinyin_list):
                        if not pinyin.startswith(input_text) and input_text in pinyin:
                            pinyin_results.append(i)

                del pinyin_list
                gc.collect()

                #只取前 10 个
                pinyin_res_count=len(pinyin_results[:10])

                count=0
                for i,res in enumerate(pinyin_results[:10]):
                    pinyin_pokename=pokemon_linkname[res]
                    kkk=res+1
                    xxxxx=str(kkk)
                    xxxxx='0'*(4-len(xxxxx))+xxxxx

                    if kkk<=151:
                        gen=1
                    elif kkk<=251:
                        gen=2
                    elif kkk<=386:
                        gen=3
                    elif kkk<=493:
                        gen=4
                    elif kkk<=649:
                        gen=5
                    elif kkk<=721:
                        gen=6
                    elif kkk<=809:
                        gen=7
                    elif kkk<=905:
                        gen=8
                    else:
                        gen=9

                    #读取单个宝可梦信息
                    file_path="/data/gen"+str(gen)+"/"+xxxxx+pinyin_pokename+"/inform.txt"

                    with open(file_path, "r",encoding='utf-8') as f:
                        data = f.readlines()
                        pokename=eval(data[0])
                        attributes=eval(data[1])

                    del data
                    gc.collect()

                    count-=1
                    if key_chosen==count:
                        choose_pokemon=res
                        num_color=(0,0,0)
                        if i+1<=result_num:
                            rec_color=(255,255,255)
                        else:
                            rec_color=(200,200,200)
                        if i<=4:
                            img.draw_rectangle(35, 65+i*37, 240, 35, color=rec_color,fill=True)
                        else:
                            img.draw_rectangle(425, 65+(i-5)*37, 240, 35, color=rec_color,fill=True)
                    else:
                        if i+1<=result_num:
                            num_color=(255,255,255)
                        else:
                            num_color=(200,200,200)

                    if i<=4:
                        #img.draw_rectangle(20, 185, 45, 20, color=(255, 255, 255),fill=True)
                        img.draw_string_advanced(35, 60+i*37, 32, pokename[0], color=num_color, font="/sdcard/res/font/ChillBitmap7x.ttf")
                        img.draw_string_advanced(145, 60+i*37, 32, pokename[1], color=num_color, font="/sdcard/res/font/SourceHanSansSC-Normal-Min.ttf")
                        # pokemon_img = image.Image("/data/gen"+str(gen)+"/"+xxxxx+pinyin_pokename+"/sprite.jpg")
                        # img.draw_image(pokemon_img, 135,31+i*27,alpha=256)
                        # del pokemon_img
                        gc.collect()
                    else:
                        img.draw_string_advanced(425, 60+(i-5)*37, 32, pokename[0], color=num_color, font="/sdcard/res/font/ChillBitmap7x.ttf")
                        img.draw_string_advanced(535, 60+(i-5)*37, 32, pokename[1], color=num_color, font="/sdcard/res/font/SourceHanSansSC-Normal-Min.ttf")
                        # pokemon_img = image.Image("/data/gen"+str(gen)+"/"+xxxxx+pinyin_pokename+"/sprite.jpg")
                        # img.draw_image(pokemon_img, 295,31+(i-5)*27, alpha=256)
                        # del pokemon_img
                        gc.collect()

                    del pokename
                    del attributes
                del pinyin_results
                gc.collect()
            # 拍摄模式
            if flag == 1:
                sensor.run()
                img.clear()
                # 单独提取拍摄图像
                captured_img = sensor.snapshot(chn=CAM_CHN_ID_0)
                img.draw_image(captured_img,0,0,0.4167,0.4167 )

            # 识图模式
            if flag == 0 and yolo_flag == 1 and read_init_flag == 0:
                yolo_flag = 0
                print(gc.mem_free())
                img.clear()

                
                test_img , test_img_ori= read_image("/data/test/0001.jpg")
                rgb888p_size=[test_img.shape[2],test_img.shape[1]]
                yolo=YOLOv5(task_type="classify",mode="image",kmodel_path=kmodel_path,labels=pokemon_lables,rgb888p_size=rgb888p_size,model_input_size=model_input_size,conf_thresh=confidence_threshold,debug_mode=0)
                yolo.config_preprocess()

                img.draw_image(test_img_ori, 100, 5, 0.5, 0.5, alpha=256)
                # 可知返回结果res为一个元组，分别代表序号和可信度(int)
                res=yolo.run(test_img)
                yolo.draw_result(res,test_img_ori)
              
                img.draw_image(captured_img, 5, 5, 0.5, 0.5, alpha=256)
                img.draw_string_advanced(5,5,60 ,"识别结果:"+pokemon_linkname[res[0]]+'\n'+"可信度："+str(res[1]), color=(250, 250, 250), font = "/sdcard/res/font/ChillBitmap7x.ttf")
                
                # 这里可向串口发送数据，用于喇叭、LED等功能

                # 由于不含0，k为实际编号
                k=res[0]+1
                x=str(k)
                x='0'*(4-len(x))+x
                linkname=pokemon_linkname[k-1]


                yolo.deinit()
                gc.collect()

            

            if read_init_flag == 1:
                img.clear()
                img.draw_image(captured_img, 5, 5, 0.2, 0.2, alpha=256) # 缩放到左上角

                if k<=151:
                    gen=1
                elif k<=251:
                    gen=2
                elif k<=386:
                    gen=3
                elif k<=493:
                    gen=4
                elif k<=649:
                    gen=5
                elif k<=721:
                    gen=6
                elif k<=809:
                    gen=7
                elif k<=905:
                    gen=8
                else:
                    gen=9

                file_path="/data/gen"+str(gen)+"/"+x+linkname+"/inform.txt"

                with open(file_path, "r",encoding='utf-8') as f:
                    data = f.readlines()
                    pokename=eval(data[0])
                    attributes=eval(data[1])
                    categories=eval(data[2])
                    special=eval(data[3])
                    height=data[4].strip()
                    weight=data[5].strip()
                    pokecolor=data[6].strip()
                    data1=eval(data[7])
                    gif_count=int(data[8])

                del data
                gc.collect()

                # 共有UI
                img.draw_string_advanced(450,0,40,"%s %s"%(pokename[0],pokename[3]),color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                # 页脚
                now_name=int(pokename[0].split('#')[-1])
                img.draw_string_advanced(350,440,40,"0"*(4-len(str(now_name)))+"%s/386"%(str(now_name)),color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                if now_name==1:
                    pre_name=386
                    next_name=now_name+1
                elif now_name==386:
                    pre_name=now_name-1
                    next_name=1
                else:
                    pre_name=now_name-1
                    next_name=now_name+1

                backname=pokemon_linkname[pre_name-1]
                img.draw_line(5, 460, 5, 480, color=(255,255,255), thickness=3)
                img.draw_line(5, 470, 25, 480, color=(255,255,255), thickness=3)
                img.draw_line(5, 470, 25, 460, color=(255,255,255), thickness=3)
                img.draw_line(25, 460, 25, 480, color=(255,255,255), thickness=3)
                img.draw_string_advanced(30,450,25,b"%s %s"%('#'+'0'*(4-len(str(pre_name)))+str(pre_name),backname),color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                forname=pokemon_linkname[next_name-1]
                img.draw_line(795, 460, 795, 480, color=(255,255,255), thickness=3)
                img.draw_line(795, 470, 775, 460, color=(255,255,255), thickness=3)
                img.draw_line(795, 470, 775, 480, color=(255,255,255), thickness=3)
                img.draw_line(775, 460, 775, 480, color=(255,255,255), thickness=3)
                img.draw_string_advanced(770-21*len(forname.strip()),450,25,b"%s %s"%(forname,'#'+'0'*(4-len(str(next_name)))+str(next_name)),color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                # 对应颜色
                for col in colors:
                    if col[0]==pokecolor:
                        img.draw_string_advanced(450,40,40,b"%s"%(pokename[1]),color=(col[1],col[2], col[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")
                # 空间问题 日语名暂且注释
                # img.draw_string_advanced(790-45*len(pokename[2].strip()),40,40,b"%s"%(pokename[2]),color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                # 元素属性
                attr_count=0
                for attr in attributes:
                    for value in values:
                        if value[0]==attr:
                            attr_count+=1
                            if attr_count==1:
                                img.draw_rectangle(450,90,120,60,(value[1],value[2],value[3]), thickness=3)
                                if len(attr)==1:
                                    img.draw_string_advanced(485,90,50,b"%s"%(attributes[0]) ,color=(value[1],value[2],value[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")
                                elif len(attr)==2:
                                    img.draw_string_advanced(465,90,50,b"%s"%(attributes[0]) ,color=(value[1],value[2],value[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")
                                else:
                                    img.draw_string_advanced(455,90,40,b"%s"%(attributes[0]) ,color=(value[1],value[2],value[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")
                            elif attr_count==2:
                                img.draw_rectangle(585,90,120,60,(value[1],value[2],value[3]), thickness=3)
                                if len(attr)==1:
                                    img.draw_string_advanced(620,90,50,b"%s"%(attributes[1]) ,color=(value[1],value[2],value[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")
                                elif len(attr)==2:
                                    img.draw_string_advanced(595,90,50,b"%s"%(attributes[1]) ,color=(value[1],value[2],value[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")
                                else:
                                    img.draw_string_advanced(590,90,40,b"%s"%(attributes[1]) ,color=(value[1],value[2],value[3]), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if isinstance(categories,list):
                    img.draw_string_advanced(450,145,45,b"%s"%(categories[0]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                elif isinstance(categories,str):
                    img.draw_string_advanced(450,145,45,b"%s"%(categories), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_string_advanced(450,190,40,b"特性", color=(200, 200, 200), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_string_advanced(300,230,30,b"种族值:", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(300,270,25,b"ＨＰ", color=(138,198,84), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(300,300,25,b"攻击", color=(248,203,60), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(300,330,25,b"防御", color=(217,136,55), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(300,360,25,b"特攻", color=(89,195,208), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(300,390,25,b"特防", color=(88,144,205), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(300,420,25,b"速度", color=(164,86,208), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if data1[0]!='?':
                    strength1=int(str(data1[0]).split("：")[-1])
                    strength2=int(str(data1[1]).split("：")[-1])
                    strength3=int(str(data1[2]).split("：")[-1])
                    strength4=int(str(data1[3]).split("：")[-1])
                    strength5=int(str(data1[4]).split("：")[-1])
                    strength6=int(str(data1[5]).split("：")[-1])
                    data1_sum=strength1+strength2+strength3+strength4+strength5+strength6
                else:
                    strength1='?'
                    strength2='?'
                    strength3='?'
                    strength4='?'
                    strength5='?'
                    strength6='?'
                    data1_sum='???'

                img.draw_string_advanced(420,230,30,b"%s"%(str(data1_sum)), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(560,190,30,b"%s"%(height), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(640,190,30,b"%s"%(weight), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_rectangle(295,270,480,180,(255,255,255), thickness=2)
                img.draw_string_advanced(360,270,25,"%s"%(data1[0].split("：")[-1]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(360,300,25,"%s"%(data1[1].split("：")[-1]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(360,330,25,"%s"%(data1[2].split("：")[-1]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(360,360,25,"%s"%(data1[3].split("：")[-1]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(360,390,25,"%s"%(data1[4].split("：")[-1]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(360,420,25,"%s"%(data1[5].split("：")[-1]), color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                img.draw_line(400, 270, 400, 450, color=(255,255,255), thickness=2)
                if data1[0]!='?':
                    img.draw_line(400, 270+15, 400+int(strength1*2.0), 270+15, color=(138,198,84), thickness=8)
                    img.draw_line(400, 300+15, 400+int(strength2*2.0), 300+15, color=(248,203,60), thickness=8)
                    img.draw_line(400, 330+15, 400+int(strength3*2.0), 330+15, color=(217,136,55), thickness=8)
                    img.draw_line(400, 360+15, 400+int(strength4*2.0), 360+15, color=(89,195,208), thickness=8)
                    img.draw_line(400, 390+15, 400+int(strength5*2.0), 390+15, color=(88,144,205), thickness=8)
                    img.draw_line(400, 420+15, 400+int(strength6*2.0), 420+15, color=(164,86,208), thickness=8)
                else:
                    img.draw_string_advanced(400+3,270+15,30,"???", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_string_advanced(400+3,300+15,30,"???", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_string_advanced(400+3,330+15,30,"???", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_string_advanced(400+3,360+15,30,"???", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_string_advanced(400+3,390+15,30,"???", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_string_advanced(400+3,420+15,30,"???", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

            if flag == 10:
                img.clear()
                img.draw_string_advanced(200, 15, 60, "SHEIKAH-STONE", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(265, 385, 30, "Press Any Key to Start", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_string_advanced(180, 425, 40, "Please Choose A Function", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
                img.draw_image(pokedex_img, 310, 170, 1.5, 1.5,alpha=256)

                # 触摸控制
                p = tp.read()
                if p != () and can_touch == 1:
                    can_touch = 0
                    # 区域1: Clock (180,100,120,80) → x:180-300, y:100-180
                    if p[0].x > 180 and p[0].x < 180+120 and p[0].y > 100 and p[0].y < 100+80:
                        if menu_collect != 1:
                            menu_collect = 1
                        else:
                            flag = 11
                    # 区域2: Cam (120,200,120,80) → x:120-240, y:200-280
                    if p[0].x > 120 and p[0].x < 120+120 and p[0].y > 200 and p[0].y < 200+80:
                        if menu_collect != 2:
                            menu_collect = 2
                        else:
                            flag = 12
                    # 区域3: Temp (180,300,120,80) → x:180-300, y:300-380
                    if p[0].x > 180 and p[0].x < 180+120 and p[0].y > 300 and p[0].y < 300+80:
                        if menu_collect != 3:
                            menu_collect = 3
                        else:
                            flag = 13
                    # 区域4: Mag (510,100,120,80) → x:510-630, y:100-180
                    if p[0].x > 510 and p[0].x < 510+120 and p[0].y > 100 and p[0].y < 100+80:
                        if menu_collect != 4:
                            menu_collect = 4
                        else:
                            flag = 14
                    # 区域5: Music (570,200,120,80) → x:570-690, y:200-280
                    if p[0].x > 570 and p[0].x < 570+120 and p[0].y > 200 and p[0].y < 200+80:
                        if menu_collect != 5:
                            menu_collect = 5
                        else:
                            flag = 15
                    # 区域6: Bomb (510,300,120,80) → x:510-630, y:300-380
                    if p[0].x > 510 and p[0].x < 510+120 and p[0].y > 300 and p[0].y < 300+80:
                        if menu_collect != 6:
                            menu_collect = 6
                        else:
                            flag = 16


                chosen_color=255

                # 选中视觉效果
                if menu_collect == 1:
                    img.draw_rectangle(180, 100, 120, 80, color=(chosen_color, chosen_color, chosen_color), fill=True)
                    img.draw_string_advanced(190, 100, 45, "Clock", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_rectangle(180, 100, 120, 80,color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                    img.draw_rectangle(120, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(130, 200, 45, "Cam", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(180, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 300, 45, "Temp", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 100, 50, "Mag", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(570, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(580, 200, 45, "Music", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 300, 45, "Bomb", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if menu_collect == 2:
                    img.draw_rectangle(180, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 100, 45, "Clock", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(120, 200, 120, 80, color=(chosen_color, chosen_color, chosen_color), fill=True)
                    img.draw_string_advanced(130, 200, 45, "Cam", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_rectangle(120, 200, 120, 80, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                    img.draw_rectangle(180, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 300, 45, "Temp", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 100, 50, "Mag", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(570, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(580, 200, 45, "Music", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 300, 45, "Bomb", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if menu_collect == 3:
                    img.draw_rectangle(180, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 100, 45, "Clock", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(120, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(130, 200, 45, "Cam", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(180, 300, 120, 80, color=(chosen_color, chosen_color, chosen_color), fill=True)
                    img.draw_string_advanced(190, 300, 45, "Temp", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_rectangle(180, 300, 120, 80, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                    img.draw_rectangle(510, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 100, 50, "Mag", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(570, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(580, 200, 45, "Music", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 300, 45, "Bomb", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if menu_collect == 4:
                    img.draw_rectangle(180, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 100, 45, "Clock", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(120, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(130, 200, 45, "Cam", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(180, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 300, 45, "Temp", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 100, 120, 80, color=(chosen_color, chosen_color, chosen_color), fill=True)
                    img.draw_string_advanced(519, 100, 50, "Mag", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_rectangle(510, 100, 120, 80, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                    img.draw_rectangle(570, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(580, 200, 45, "Music", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 300, 45, "Bomb", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if menu_collect == 5:
                    img.draw_rectangle(180, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 100, 45, "Clock", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(120, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(130, 200, 45, "Cam", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(180, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 300, 45, "Temp", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 100, 50, "Mag", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(570, 200, 120, 80, color=(chosen_color, chosen_color, chosen_color), fill=True)
                    img.draw_string_advanced(580, 200, 45, "Music", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_rectangle(570, 200, 120, 80, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)

                    img.draw_rectangle(510, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 300, 45, "Bomb", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                if menu_collect == 6:
                    img.draw_rectangle(180, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 100, 45, "Clock", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(120, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(130, 200, 45, "Cam", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(180, 300, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(190, 300, 45, "Temp", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 100, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(519, 100, 50, "Mag", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(570, 200, 120, 80, color=(255, 255, 255), thickness=2)
                    img.draw_string_advanced(580, 200, 45, "Music", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")

                    img.draw_rectangle(510, 300, 120, 80, color=(chosen_color, chosen_color, chosen_color), fill=True)
                    img.draw_string_advanced(519, 300, 45, "Bomb", color=(255-chosen_color, 255-chosen_color, 255-chosen_color), font="/sdcard/res/font/ChillBitmap7x.ttf")
                    img.draw_rectangle(510, 300, 120, 80, color=(255-chosen_color, 255-chosen_color, 255-chosen_color), thickness=2)



            # 确认键
            if current_key_state5 == 0 and last_key_state5 == 1:
                #初始界面
                if flag==-1:
                    if menu_collect==1:
                        flag=1
                    elif menu_collect==2:
                        flag=2
                    elif menu_collect==3:
                        flag=10
                    elif menu_collect==4:
                        flag=4

                # 输入界面
                elif flag==2:
                    # 消抖
                    utime.sleep_ms(50)
                    key_chosen_flag=True
                    if key_chosen==20:
                        flag=1
                        random_flag=1
                    elif key_chosen==28:
                        input_text=input_text[:-1]
                    elif key_chosen>=1:
                        if len(input_text)<=4:
                            if key_chosen<=19:
                                input_text += "QWERTYUIOPASDFGHJKLZXCVBNM"[key_chosen-1]
                            else:
                                input_text += "QWERTYUIOPASDFGHJKLZXCVBNM"[key_chosen-2]
                    elif key_chosen<0:
                        flag=0
                        choose_flag=1
                elif flag==1:
                    # 拍摄进入展示界面
                    flag = 0
                    captured_img.save("/data/test/0001.jpg") # 调试
                    yolo_flag = 1
                    # form_num=0




                # 识图进入详情界面
                elif flag==0:
                    read_init_flag=1



                # 之后可配置切换信息
                # elif choose_flag == 1:
                #     choose_flag=0
                #     key_chosen=20
                #     input_text = ""
                #     k=choose_pokemon+1

                #     x=str(k)
                #     x='0'*(4-len(x))+x
                #     linkname=pokemon_linkname[k-1]
                # # 注意模型未导入时k未定义，按键进入状态会报错
                # if k<=151:
                #     gen=1
                # elif k<=251:
                #     gen=2
                # elif k<=386:
                #     gen=3
                # elif k<=493:
                #     gen=4
                # elif k<=649:
                #     gen=5
                # elif k<=721:
                #     gen=6
                # elif k<=809:
                #     gen=7
                # elif k<=905:
                #     gen=8
                # else:
                #     gen=9

                # file_path="/data/gen"+str(gen)+"/"+x+linkname+"/inform.txt"

                # with open(file_path, "r",encoding='utf-8') as f:
                #     data = f.readlines()
                #     pokename=eval(data[0])
                #     attributes=eval(data[1])
                #     categories=eval(data[2])
                #     special=eval(data[3])
                #     height=data[4].strip()
                #     weight=data[5].strip()
                #     pokecolor=data[6].strip()
                #     data1=eval(data[7])
                #     gif_count=int(data[8])

                # del data
                # gc.collect()

                # # 形态切换
                # if form_flag==1:
                #     form_flag=0
                #     form_num+=1
                #     form_path="/data/gen"+str(gen)+"/"+x+linkname+"/form/form_info/"+str(form_num)+".txt"
                #     try:
                #         with open(form_path, "r",encoding='utf-8') as f:
                #             data = f.readlines()
                #             formname=eval(data[0])[1]
                #             attributes=eval(data[1])
                #             categories=data[2].strip()
                #             special=eval(data[3])
                #             height=data[4].strip()
                #             weight=data[5].strip()
                #             pokecolor=data[6].strip()
                #             data1=eval(data[7])
                #         form_show_flag=1
                #     except:
                #         try:
                #             form_num=0
                #             form_path="/data/gen"+str(gen)+"/"+x+linkname+"/form/form_info/0.txt"
                #             with open(form_path, "r",encoding='utf-8') as f:
                #                 data = f.readlines()
                #                 formname=eval(data[0])[1]
                #                 attributes=eval(data[1])
                #                 categories=data[2].strip()
                #                 special=eval(data[3])
                #                 height=data[4].strip()
                #                 weight=data[5].strip()
                #                 pokecolor=data[6].strip()
                #                 data1=eval(data[7])
                #             form_show_flag=1
                #         except:
                #             form_num=0

                # # 神秘标志位
                # if not read_init_flag0==1:
                #     if form_num==0:
                #         evo_txt="/sd/gen"+str(gen)+"/"+x+linkname+"/evolution.txt"
                #         evo_img="/sd/gen"+str(gen)+"/"+x+linkname+"/evolution/"
                #         with open(evo_txt,'r') as f:
                #             evolutions=eval(f.read().strip())

                #     elif int(x)==555 and (form_num==2 or form_num==3):
                #         evo_txt="/sd/gen"+str(gen)+"/"+x+linkname+"/form/form_evo/evolution_form.txt"
                #         evo_img="/sd/gen"+str(gen)+"/"+x+linkname+"/form/form_evo/"
                #         with open(evo_txt,'r') as f:
                #             evolutions=eval(f.read().strip())

                #     elif form_num==1:
                #         try:
                #             evo_txt="/sd/gen"+str(gen)+"/"+x+linkname+"/form/form_evo/evolution_form.txt"
                #             evo_img="/sd/gen"+str(gen)+"/"+x+linkname+"/form/form_evo/"
                #             with open(evo_txt,'r') as f:
                #                 evolutions=eval(f.read().strip())
                #         except:
                #             evo_txt="/sd/gen"+str(gen)+"/"+x+linkname+"/evolution.txt"
                #             evo_img="/sd/gen"+str(gen)+"/"+x+linkname+"/evolution/"
                #             with open(evo_txt,'r') as f:
                #                 evolutions=eval(f.read().strip())



            # 上
            if current_key_state1 == 0 and last_key_state1 == 1:
                if flag==-1:
                    if menu_collect==1:
                        menu_collect=1
                    elif menu_collect==2:
                        menu_collect=1
                    elif menu_collect==3:
                        menu_collect=3
                    elif menu_collect==4:
                        menu_collect=3
                elif flag==2:
                    key_chosen_flag=True
                    if pinyin_res_count==0:
                        if key_chosen<=1:
                            key_chosen=key_chosen+20
                        elif key_chosen<=8:
                            key_chosen=key_chosen+19
                        elif key_chosen<=10:
                            key_chosen=28
                        elif key_chosen<=20:
                            key_chosen=key_chosen-10
                        elif key_chosen<=28:
                            key_chosen=key_chosen-10
                    else:
                        if key_chosen==-1:
                            key_chosen=max([-(pinyin_res_count),-5])
                        elif key_chosen==-6:
                            key_chosen=max([-(pinyin_res_count),-10])
                        elif key_chosen<0:
                            key_chosen=key_chosen+1
                        elif key_chosen<=10:
                            key_chosen=-1
                        elif key_chosen<=20:
                            key_chosen=key_chosen-10
                        elif key_chosen<=28:
                            key_chosen=key_chosen-10
                elif flag==10:
                    if menu_collect == 1:
                        menu_collect = 1
                    elif menu_collect == 2:
                        menu_collect = 1
                    elif menu_collect == 3:
                        menu_collect = 2
                    elif menu_collect == 4:
                        menu_collect = 4
                    elif menu_collect == 5:
                        menu_collect = 4
                    elif menu_collect == 6:
                        menu_collect = 5


            # 下
            if current_key_state2 == 0 and last_key_state2 == 1:
                if flag==-1:
                    if menu_collect==1:
                        menu_collect=2
                    elif menu_collect==2:
                        menu_collect=2
                    elif menu_collect==3:
                        menu_collect=4
                    elif menu_collect==4:
                        menu_collect=4
                elif flag==2:
                    key_chosen_flag=True
                    if pinyin_res_count==0:
                        if key_chosen<=10:
                            key_chosen=key_chosen+10
                        elif key_chosen<=17:
                            key_chosen=key_chosen+10
                        elif key_chosen<=20:
                            key_chosen=28
                        elif key_chosen<=21:
                            key_chosen=1
                        elif key_chosen<=28:
                            key_chosen=key_chosen-20
                    else:
                        if key_chosen==max([-(pinyin_res_count),-5]):
                            key_chosen=1
                        elif key_chosen==max([-(pinyin_res_count),-10]):
                            key_chosen=1
                        elif key_chosen<0:
                            key_chosen=key_chosen-1
                        elif key_chosen<=10:
                            key_chosen=key_chosen+10
                        elif key_chosen<=17:
                            key_chosen=key_chosen+10
                        elif key_chosen<=20:
                            key_chosen=28
                        elif key_chosen<=28:
                            key_chosen=-1
                elif flag==10:
                    if menu_collect == 1:
                        menu_collect = 2
                    elif menu_collect == 2:
                        menu_collect = 3
                    elif menu_collect == 3:
                        menu_collect = 3
                    elif menu_collect == 4:
                        menu_collect = 5
                    elif menu_collect == 5:
                        menu_collect = 6
                    elif menu_collect == 6:
                        menu_collect = 6

            # 左
            if current_key_state3 == 0 and last_key_state3 == 1:
                if flag==-1:
                    if menu_collect==1:
                        menu_collect=1
                    elif menu_collect==2:
                        menu_collect=2
                    elif menu_collect==3:
                        menu_collect=1
                    elif menu_collect==4:
                        menu_collect=2
                elif flag==2:
                    key_chosen_flag=True
                    if pinyin_res_count==0:
                        if key_chosen==1:
                            key_chosen=10
                        elif key_chosen==11:
                            key_chosen=20
                        elif key_chosen==21:
                            key_chosen=28
                        else:
                            key_chosen=key_chosen-1
                    else:
                        if key_chosen<=-6:
                            key_chosen+=5
                        elif key_chosen==1:
                            key_chosen=10
                        elif key_chosen==11:
                            key_chosen=20
                        elif key_chosen==21:
                            key_chosen=28
                        else:
                            key_chosen=key_chosen-1
                elif flag==10:
                    if menu_collect == 1:
                        menu_collect = 1
                    elif menu_collect == 2:
                        menu_collect = 2
                    elif menu_collect == 3:
                        menu_collect = 3
                    elif menu_collect == 4:
                        menu_collect = 1
                    elif menu_collect == 5:
                        menu_collect = 2
                    elif menu_collect == 6:
                        menu_collect = 3

            # 右
            if current_key_state4 == 0 and last_key_state4 == 1:
                if flag==-1:
                    if menu_collect==1:
                        menu_collect=3
                    elif menu_collect==2:
                        menu_collect=4
                    elif menu_collect==3:
                        menu_collect=3
                    elif menu_collect==4:
                        menu_collect=4
                elif flag==2:
                    key_chosen_flag=True
                    if pinyin_res_count==0:
                        if key_chosen==10:
                            key_chosen=1
                        elif key_chosen==20:
                            key_chosen=11
                        elif key_chosen==28:
                            key_chosen=21
                        else:
                            key_chosen=key_chosen+1
                    else:
                        if key_chosen<0 and key_chosen>=-5:
                            key_chosen=max([-pinyin_res_count,key_chosen-5])
                        elif key_chosen==10:
                            key_chosen=1
                        elif key_chosen==20:
                            key_chosen=11
                        elif key_chosen==28:
                            key_chosen=21
                        else:
                            key_chosen=key_chosen+1
                elif flag==10:
                    if menu_collect == 1:
                        menu_collect = 4
                    elif menu_collect == 2:
                        menu_collect = 5
                    elif menu_collect == 3:
                        menu_collect = 6
                    elif menu_collect == 4:
                        menu_collect = 4
                    elif menu_collect == 5:
                        menu_collect = 5
                    elif menu_collect == 6:
                        menu_collect = 6

            # 返回
            if button.value() == 1:
                if flag == 0 or flag == 1 or flag == 2 or flag == 10:
                    flag = -1
                    read_init_flag = 0
                elif flag == 11 or flag == 12 or flag == 13 or flag == 14 or flag == 15 or flag == 16:
                    flag = 10


            last_key_state1 = current_key_state1
            last_key_state2 = current_key_state2
            last_key_state3 = current_key_state3
            last_key_state4 = current_key_state4
            last_key_state5 = current_key_state5

            Display.show_image(img)

#            time.sleep(0.5)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        print(f"Exception {e}")

    sensor.stop()
    # deinit display
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # release media buffer
    MediaManager.deinit()

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    display_test()

