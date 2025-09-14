from media.display import *       # K230 显示驱动库（控制 LCD/HDMI）
from media.media import *         # K230 媒体管理库（管理显示缓冲区等资源）
from media.sensor import *
import time, os, sys, gc, urandom      # 系统工具库（时间、文件、内存回收）
import lvgl as lv                 # 嵌入式 GUI 库（LVGL，负责 UI 渲染与交互）
from machine import TOUCH         # K230 触摸设备驱动（读取触摸坐标）
from machine import Pin
from machine import FPIOA
from machine import Timer

DISPLAY_WIDTH = ALIGN_UP(800, 16)  # 800 对齐后仍为 800（800 % 16 = 0）
DISPLAY_HEIGHT = 480               # 固定高度 480

can_touch = 1;

def init_uart():
    fpioa = FPIOA()

    fpioa.set_function()

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

    # 2查询功能的变量数组
    labels=['abra', 'aerodactyl', 'alakazam', 'arbok', 'arcanine', 'articuno', 'beedrill', 'bellsprout', 'blastoise', 'bulbasaur', 'butterfree', 'caterpie', 'chansey', 'charizard', 'charmander', 'charmeleon', 'clefable', 'clefairy', 'cloyster', 'cubone', 'dewgong', 'diglett', 'ditto', 'dodrio', 'doduo', 'dragonair', 'dragonite', 'dratini', 'drowzee', 'dugtrio', 'eevee', 'ekans', 'electabuzz', 'electrode', 'exeggcute', 'exeggutor', 'farfetchd', 'fearow', 'flareon', 'gastly', 'gengar', 'geodude', 'gloom', 'golbat', 'goldeen', 'golduck', 'golem', 'graveler', 'grimer', 'growlithe', 'gyarados', 'haunter', 'hitmonchan', 'hitmonlee', 'horsea', 'hypno', 'ivysaur', 'jigglypuff', 'jolteon', 'jynx', 'kabuto', 'kabutops', 'kadabra', 'kakuna', 'kangaskhan', 'kingler', 'koffing', 'krabby', 'lapras', 'lickitung', 'machamp', 'machoke', 'machop', 'magikarp', 'magmar', 'magnemite', 'magneton', 'mankey', 'marowak', 'meowth', 'metapod', 'mew', 'mewtwo', 'moltres', 'mr-mime', 'muk', 'nidoking', 'nidoqueen', 'nidoran-f', 'nidoran-m', 'nidorina', 'nidorino', 'ninetales', 'oddish', 'omanyte', 'omastar', 'onix', 'paras', 'parasect', 'persian', 'pidgeot', 'pidgeotto', 'pidgey', 'pikachu', 'pinsir', 'poliwag', 'poliwhirl', 'poliwrath', 'ponyta', 'porygon', 'primeape', 'psyduck', 'raichu', 'rapidash', 'raticate', 'rattata', 'rhydon', 'rhyhorn', 'sandshrew', 'sandslash', 'scyther', 'seadra', 'seaking', 'seel', 'shellder', 'slowbro', 'slowpoke', 'snorlax', 'spearow', 'squirtle', 'starmie', 'staryu', 'tangela', 'tauros', 'tentacool', 'tentacruel', 'vaporeon', 'venomoth', 'venonat', 'venusaur', 'victreebel', 'vileplume', 'voltorb', 'vulpix', 'wartortle', 'weedle', 'weepinbell', 'weezing', 'wigglytuff', 'zapdos', 'zubat']
    pokemon_linkname=['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle', 'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill', 'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate', 'spearow', 'fearow', 'ekans', 'arbok', 'pikachu', 'raichu', 'sandshrew', 'sandslash', 'nidoran-f', 'nidorina', 'nidoqueen', 'nidoran-m', 'nidorino', 'nidoking', 'clefairy', 'clefable', 'vulpix', 'ninetales', 'jigglypuff', 'wigglytuff', 'zubat', 'golbat', 'oddish', 'gloom', 'vileplume', 'paras', 'parasect', 'venonat', 'venomoth', 'diglett', 'dugtrio', 'meowth', 'persian', 'psyduck', 'golduck', 'mankey', 'primeape', 'growlithe', 'arcanine', 'poliwag', 'poliwhirl', 'poliwrath', 'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell', 'victreebel', 'tentacool', 'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta', 'rapidash', 'slowpoke', 'slowbro', 'magnemite', 'magneton', 'farfetchd', 'doduo', 'dodrio', 'seel', 'dewgong', 'grimer', 'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix', 'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb', 'electrode', 'exeggcute', 'exeggutor', 'cubone', 'marowak', 'hitmonlee', 'hitmonchan', 'lickitung', 'koffing', 'weezing', 'rhyhorn', 'rhydon', 'chansey', 'tangela', 'kangaskhan', 'horsea', 'seadra', 'goldeen', 'seaking', 'staryu', 'starmie', 'mr-mime', 'scyther', 'jynx', 'electabuzz', 'magmar', 'pinsir', 'tauros', 'magikarp', 'gyarados', 'lapras', 'ditto', 'eevee', 'vaporeon', 'jolteon', 'flareon', 'porygon', 'omanyte', 'omastar', 'kabuto', 'kabutops', 'aerodactyl', 'snorlax', 'articuno', 'zapdos', 'moltres', 'dratini', 'dragonair', 'dragonite', 'mewtwo', 'mew', 'chikorita', 'bayleef', 'meganium', 'cyndaquil', 'quilava', 'typhlosion', 'totodile', 'croconaw', 'feraligatr', 'sentret', 'furret', 'hoothoot', 'noctowl', 'ledyba', 'ledian', 'spinarak', 'ariados', 'crobat', 'chinchou', 'lanturn', 'pichu', 'cleffa', 'igglybuff', 'togepi', 'togetic', 'natu', 'xatu', 'mareep', 'flaaffy', 'ampharos', 'bellossom', 'marill', 'azumarill', 'sudowoodo', 'politoed', 'hoppip', 'skiploom', 'jumpluff', 'aipom', 'sunkern', 'sunflora', 'yanma', 'wooper', 'quagsire', 'espeon', 'umbreon', 'murkrow', 'slowking', 'misdreavus', 'unown', 'wobbuffet', 'girafarig', 'pineco', 'forretress', 'dunsparce', 'gligar', 'steelix', 'snubbull', 'granbull', 'qwilfish', 'scizor', 'shuckle', 'heracross', 'sneasel', 'teddiursa', 'ursaring', 'slugma', 'magcargo', 'swinub', 'piloswine', 'corsola', 'remoraid', 'octillery', 'delibird', 'mantine', 'skarmory', 'houndour', 'houndoom', 'kingdra', 'phanpy', 'donphan', 'porygon2', 'stantler', 'smeargle', 'tyrogue', 'hitmontop', 'smoochum', 'elekid', 'magby', 'miltank', 'blissey', 'raikou', 'entei', 'suicune', 'larvitar', 'pupitar', 'tyranitar', 'lugia', 'ho-oh', 'celebi', 'treecko', 'grovyle', 'sceptile', 'torchic', 'combusken', 'blaziken', 'mudkip', 'marshtomp', 'swampert', 'poochyena', 'mightyena', 'zigzagoon', 'linoone', 'wurmple', 'silcoon', 'beautifly', 'cascoon', 'dustox', 'lotad', 'lombre', 'ludicolo', 'seedot', 'nuzleaf', 'shiftry', 'taillow', 'swellow', 'wingull', 'pelipper', 'ralts', 'kirlia', 'gardevoir', 'surskit', 'masquerain', 'shroomish', 'breloom', 'slakoth', 'vigoroth', 'slaking', 'nincada', 'ninjask', 'shedinja', 'whismur', 'loudred', 'exploud', 'makuhita', 'hariyama', 'azurill', 'nosepass', 'skitty', 'delcatty', 'sableye', 'mawile', 'aron', 'lairon', 'aggron', 'meditite', 'medicham', 'electrike', 'manectric', 'plusle', 'minun', 'volbeat', 'illumise', 'roselia', 'gulpin', 'swalot', 'carvanha', 'sharpedo', 'wailmer', 'wailord', 'numel', 'camerupt', 'torkoal', 'spoink', 'grumpig', 'spinda', 'trapinch', 'vibrava', 'flygon', 'cacnea', 'cacturne', 'swablu', 'altaria', 'zangoose', 'seviper', 'lunatone', 'solrock', 'barboach', 'whiscash', 'corphish', 'crawdaunt', 'baltoy', 'claydol', 'lileep', 'cradily', 'anorith', 'armaldo', 'feebas', 'milotic', 'castform', 'kecleon', 'shuppet', 'banette', 'duskull', 'dusclops', 'tropius', 'chimecho', 'absol', 'wynaut', 'snorunt', 'glalie', 'spheal', 'sealeo', 'walrein', 'clamperl', 'huntail', 'gorebyss', 'relicanth', 'luvdisc', 'bagon', 'shelgon', 'salamence', 'beldum', 'metang', 'metagross', 'regirock', 'regice', 'registeel', 'latias', 'latios', 'kyogre', 'groudon', 'rayquaza', 'jirachi', 'deoxys', 'turtwig', 'grotle', 'torterra', 'chimchar', 'monferno', 'infernape', 'piplup', 'prinplup', 'empoleon', 'starly', 'staravia', 'staraptor', 'bidoof', 'bibarel', 'kricketot', 'kricketune', 'shinx', 'luxio', 'luxray', 'budew', 'roserade', 'cranidos', 'rampardos', 'shieldon', 'bastiodon', 'burmy', 'wormadam', 'mothim', 'combee', 'vespiquen', 'pachirisu', 'buizel', 'floatzel', 'cherubi', 'cherrim', 'shellos', 'gastrodon', 'ambipom', 'drifloon', 'drifblim', 'buneary', 'lopunny', 'mismagius', 'honchkrow', 'glameow', 'purugly', 'chingling', 'stunky', 'skuntank', 'bronzor', 'bronzong', 'bonsly', 'mime-jr', 'happiny', 'chatot', 'spiritomb', 'gible', 'gabite', 'garchomp', 'munchlax', 'riolu', 'lucario', 'hippopotas', 'hippowdon', 'skorupi', 'drapion', 'croagunk', 'toxicroak', 'carnivine', 'finneon', 'lumineon', 'mantyke', 'snover', 'abomasnow', 'weavile', 'magnezone', 'lickilicky', 'rhyperior', 'tangrowth', 'electivire', 'magmortar', 'togekiss', 'yanmega', 'leafeon', 'glaceon', 'gliscor', 'mamoswine', 'porygon-z', 'gallade', 'probopass', 'dusknoir', 'froslass', 'rotom', 'uxie', 'mesprit', 'azelf', 'dialga', 'palkia', 'heatran', 'regigigas', 'giratina', 'cresselia', 'phione', 'manaphy', 'darkrai', 'shaymin', 'arceus', 'victini', 'snivy', 'servine', 'serperior', 'tepig', 'pignite', 'emboar', 'oshawott', 'dewott', 'samurott', 'patrat', 'watchog', 'lillipup', 'herdier', 'stoutland', 'purrloin', 'liepard', 'pansage', 'simisage', 'pansear', 'simisear', 'panpour', 'simipour', 'munna', 'musharna', 'pidove', 'tranquill', 'unfezant', 'blitzle', 'zebstrika', 'roggenrola', 'boldore', 'gigalith', 'woobat', 'swoobat', 'drilbur', 'excadrill', 'audino', 'timburr', 'gurdurr', 'conkeldurr', 'tympole', 'palpitoad', 'seismitoad', 'throh', 'sawk', 'sewaddle', 'swadloon', 'leavanny', 'venipede', 'whirlipede', 'scolipede', 'cottonee', 'whimsicott', 'petilil', 'lilligant', 'basculin', 'sandile', 'krokorok', 'krookodile', 'darumaka', 'darmanitan', 'maractus', 'dwebble', 'crustle', 'scraggy', 'scrafty', 'sigilyph', 'yamask', 'cofagrigus', 'tirtouga', 'carracosta', 'archen', 'archeops', 'trubbish', 'garbodor', 'zorua', 'zoroark', 'minccino', 'cinccino', 'gothita', 'gothorita', 'gothitelle', 'solosis', 'duosion', 'reuniclus', 'ducklett', 'swanna', 'vanillite', 'vanillish', 'vanilluxe', 'deerling', 'sawsbuck', 'emolga', 'karrablast', 'escavalier', 'foongus', 'amoonguss', 'frillish', 'jellicent', 'alomomola', 'joltik', 'galvantula', 'ferroseed', 'ferrothorn', 'klink', 'klang', 'klinklang', 'tynamo', 'eelektrik', 'eelektross', 'elgyem', 'beheeyem', 'litwick', 'lampent', 'chandelure', 'axew', 'fraxure', 'haxorus', 'cubchoo', 'beartic', 'cryogonal', 'shelmet', 'accelgor', 'stunfisk', 'mienfoo', 'mienshao', 'druddigon', 'golett', 'golurk', 'pawniard', 'bisharp', 'bouffalant', 'rufflet', 'braviary', 'vullaby', 'mandibuzz', 'heatmor', 'durant', 'deino', 'zweilous', 'hydreigon', 'larvesta', 'volcarona', 'cobalion', 'terrakion', 'virizion', 'tornadus', 'thundurus', 'reshiram', 'zekrom', 'landorus', 'kyurem', 'keldeo', 'meloetta', 'genesect', 'chespin', 'quilladin', 'chesnaught', 'fennekin', 'braixen', 'delphox', 'froakie', 'frogadier', 'greninja', 'bunnelby', 'diggersby', 'fletchling', 'fletchinder', 'talonflame', 'scatterbug', 'spewpa', 'vivillon', 'litleo', 'pyroar', 'flabebe', 'floette', 'florges', 'skiddo', 'gogoat', 'pancham', 'pangoro', 'furfrou', 'espurr', 'meowstic', 'honedge', 'doublade', 'aegislash', 'spritzee', 'aromatisse', 'swirlix', 'slurpuff', 'inkay', 'malamar', 'binacle', 'barbaracle', 'skrelp', 'dragalge', 'clauncher', 'clawitzer', 'helioptile', 'heliolisk', 'tyrunt', 'tyrantrum', 'amaura', 'aurorus', 'sylveon', 'hawlucha', 'dedenne', 'carbink', 'goomy', 'sliggoo', 'goodra', 'klefki', 'phantump', 'trevenant', 'pumpkaboo', 'gourgeist', 'bergmite', 'avalugg', 'noibat', 'noivern', 'xerneas', 'yveltal', 'zygarde', 'diancie', 'hoopa', 'volcanion', 'rowlet', 'dartrix', 'decidueye', 'litten', 'torracat', 'incineroar', 'popplio', 'brionne', 'primarina', 'pikipek', 'trumbeak', 'toucannon', 'yungoos', 'gumshoos', 'grubbin', 'charjabug', 'vikavolt', 'crabrawler', 'crabominable', 'oricorio', 'cutiefly', 'ribombee', 'rockruff', 'lycanroc', 'wishiwashi', 'mareanie', 'toxapex', 'mudbray', 'mudsdale', 'dewpider', 'araquanid', 'fomantis', 'lurantis', 'morelull', 'shiinotic', 'salandit', 'salazzle', 'stufful', 'bewear', 'bounsweet', 'steenee', 'tsareena', 'comfey', 'oranguru', 'passimian', 'wimpod', 'golisopod', 'sandygast', 'palossand', 'pyukumuku', 'type-null', 'silvally', 'minior', 'komala', 'turtonator', 'togedemaru', 'mimikyu', 'bruxish', 'drampa', 'dhelmise', 'jangmo-o', 'hakamo-o', 'kommo-o', 'tapu-koko', 'tapu-lele', 'tapu-bulu', 'tapu-fini', 'cosmog', 'cosmoem', 'solgaleo', 'lunala', 'nihilego', 'buzzwole', 'pheromosa', 'xurkitree', 'celesteela', 'kartana', 'guzzlord', 'necrozma', 'magearna', 'marshadow', 'poipole', 'naganadel', 'stakataka', 'blacephalon', 'zeraora', 'meltan', 'melmetal', 'grookey', 'thwackey', 'rillaboom', 'scorbunny', 'raboot', 'cinderace', 'sobble', 'drizzile', 'inteleon', 'skwovet', 'greedent', 'rookidee', 'corvisquire', 'corviknight', 'blipbug', 'dottler', 'orbeetle', 'nickit', 'thievul', 'gossifleur', 'eldegoss', 'wooloo', 'dubwool', 'chewtle', 'drednaw', 'yamper', 'boltund', 'rolycoly', 'carkol', 'coalossal', 'applin', 'flapple', 'appletun', 'silicobra', 'sandaconda', 'cramorant', 'arrokuda', 'barraskewda', 'toxel', 'toxtricity', 'sizzlipede', 'centiskorch', 'clobbopus', 'grapploct', 'sinistea', 'polteageist', 'hatenna', 'hattrem', 'hatterene', 'impidimp', 'morgrem', 'grimmsnarl', 'obstagoon', 'perrserker', 'cursola', 'sirfetchd', 'mr-rime', 'runerigus', 'milcery', 'alcremie', 'falinks', 'pincurchin', 'snom', 'frosmoth', 'stonjourner', 'eiscue', 'indeedee', 'morpeko', 'cufant', 'copperajah', 'dracozolt', 'arctozolt', 'dracovish', 'arctovish', 'duraludon', 'dreepy', 'drakloak', 'dragapult', 'zacian', 'zamazenta', 'eternatus', 'kubfu', 'urshifu', 'zarude', 'regieleki', 'regidrago', 'glastrier', 'spectrier', 'calyrex', 'wyrdeer', 'kleavor', 'ursaluna', 'basculegion', 'sneasler', 'overqwil', 'enamorus', 'sprigatito', 'floragato', 'meowscarada', 'fuecoco', 'crocalor', 'skeledirge', 'quaxly', 'quaxwell', 'quaquaval', 'lechonk', 'oinkologne', 'tarountula', 'spidops', 'nymble', 'lokix', 'pawmi', 'pawmo', 'pawmot', 'tandemaus', 'maushold', 'fidough', 'dachsbun', 'smoliv', 'dolliv', 'arboliva', 'squawkabilly', 'nacli', 'naclstack', 'garganacl', 'charcadet', 'armarouge', 'ceruledge', 'tadbulb', 'bellibolt', 'wattrel', 'kilowattrel', 'maschiff', 'mabosstiff', 'shroodle', 'grafaiai', 'bramblin', 'brambleghast', 'toedscool', 'toedscruel', 'klawf', 'capsakid', 'scovillain', 'rellor', 'rabsca', 'flittle', 'espathra', 'tinkatink', 'tinkatuff', 'tinkaton', 'wiglett', 'wugtrio', 'bombirdier', 'finizen', 'palafin', 'varoom', 'revavroom', 'cyclizar', 'orthworm', 'glimmet', 'glimmora', 'greavard', 'houndstone', 'flamigo', 'cetoddle', 'cetitan', 'veluza', 'dondozo', 'tatsugiri', 'annihilape', 'clodsire', 'farigiraf', 'dudunsparce', 'kingambit', 'great-tusk', 'scream-tail', 'brute-bonnet', 'flutter-mane', 'slither-wing', 'sandy-shocks', 'iron-treads', 'iron-bundle', 'iron-hands', 'iron-jugulis', 'iron-moth', 'iron-thorns', 'frigibax', 'arctibax', 'baxcalibur', 'gimmighoul', 'gholdengo', 'wo-chien', 'chien-pao', 'ting-lu', 'chi-yu', 'roaring-moon', 'iron-valiant', 'koraidon', 'miraidon', 'walking-wake', 'iron-leaves', 'dipplin', 'poltchageist', 'sinistcha', 'okidogi', 'munkidori', 'fezandipiti', 'ogerpon', 'archaludon', 'hydrapple', 'gouging-fire', 'raging-bolt', 'iron-boulder', 'iron-crown', 'terapagos', 'pecharunt']
    colors=[('红色',243,82,82),('蓝色',148,219,238),('绿色',170,209,94),('黄色',255,255,153),('紫色',197,150,189),('粉红色',255,221,255),('褐色',204,153,102),('黑色',187,187,187),('灰色',238,238,238),('白色',255,255,255)]
    values=[('一般',187,187,170),('格斗',187,85,68),('飞行',129,185,199),('毒',170,85,153),('地面',221,187,85),('岩石',187,170,102),('虫',170,187,34),('幽灵',142,142,187),('钢',170,170,187),('火',255,68,34),('水',51,153,255),('草',119,204,85),('电',255,204,51),('超能力',255,85,153),('冰',119,221,245),('龙',179,102,238),('恶',119,85,68),('妖精',255,170,255)]


    img = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.RGB565)
    src_img = image.Image("/data/pokedex.bmp")
    # sensor = Sensor()
    # sensor.reset()
    Display.init(Display.ST7701, width = DISPLAY_WIDTH, height = DISPLAY_HEIGHT, to_ide = True)
    MediaManager.init()


    try:

        key = Pin(62, Pin.OUT, pull=Pin.PULL_NONE, drive=7)


        menu_collect = 3 # 当前选中哪个模式
        chosen_color = 0
        input_text = ""
        key_chosen_flag = True
        flag = -1 # 当前在哪个模式里 -1为初始
        key_chosen=20 # 输入界面里的键位选择
        pinyin_res_count=0
        choose_flag=0
        choose_pokemon=0

        # 触摸控制
        tp = TOUCH(0)
        global can_touch
        tim = Timer(-1)
        tim.init(period=1000, mode=Timer.PERIODIC, callback=timer_callback)

        while True:
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

            img.clear()
            img.draw_string_advanced(95, 25, 80, "NAUTILUS-PRIME", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            img.draw_string_advanced(265, 385, 30, "Press Any Key to Start", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            img.draw_string_advanced(225, 425, 40, "Presented by Zaphkiel", color=(255, 255, 255), font="/sdcard/res/font/ChillBitmap7x.ttf")
            img.draw_image(src_img, 310, 170, 1.5, 1.5,alpha=256)
            #暂时无效，原因未知，只能用Display
            #改变了img通道后完全解决
            #if flag == -1:
                #Display.show_image(src_img,x=350,y=200,layer = Display.LAYER_OSD1)


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
                            img.draw_rectangle(30, 36+i*27, 140, 20, color=rec_color,fill=True)
                        else:
                            img.draw_rectangle(170, 36+(i-5)*27, 140, 20, color=rec_color,fill=True)
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

