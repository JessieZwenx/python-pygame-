# 引入需要的库
import pygame
import random
# 引用以对程序进行控制
import sys

# 初始化程序
pygame.init()

# 定义部分

# 屏幕
screen_width = 1280
screen_height = 768
# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
GREEN = (0, 200, 100)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
PURPLE = (180, 100, 240)
DARK_BLUE = (0, 60, 120)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (60, 60, 60)
BUTTON_GREEN = (0, 180, 80)
PANEL_BLUE = (0, 255, 255)
BUTTON_HOVER = BLUE
# 时钟
clock = pygame.time.Clock()
FPS = 60
# 字体
title_font = pygame.font.SysFont("microsoftyahei",48,bold=True)
header_font = pygame.font.SysFont("microsoftyahei",32,bold=True)
normal_font = pygame.font.SysFont("microsoftyahei",24)
small_font = pygame.font.SysFont("microsoftyahei",20)
button_font = pygame.font.SysFont('microsoftyahei', 32, bold=True)
# 资源
resources ={
    "能源": 50,
    "食物": 30, 
    "水源": 10,
    "氧气": 30,
    "材料": 0
}

# 模块
modules= {
     "太阳能板": {"等级": 1, "效率": 5},
    "水循环系统": {"等级": 1, "效率": 3},
    "氧气生成器": {"等级": 1, "效率": 4},
    "温室": {"等级": 1, "效率": 2},
    "采矿机": {"等级": 1, "效率": 2}
}

# 人员
crew ={
     "工程师": 1,
    "科学家": 1,
    "医生": 1,
    "飞行员": 1
}

# 天数从1开始
day = 1

# 游戏状态（通过状态进行界面的跳转）
game_started = False
game_over = False

# 常量
message = "欢迎来到深空哨站"
snd1=pygame.mixer.Sound('python-game-spacecontrol - 副本/sources/music/音效 (2).mp3')
snd2=pygame.mixer.Sound('python-game-spacecontrol - 副本/sources/music/音效 (1).mp3')
snd3_切换=pygame.mixer.Sound('python-game-spacecontrol - 副本/sources/music/音效 (5)_切换.mp3')
snd3_结束=pygame.mixer.Sound('python-game-spacecontrol - 副本/sources/music/音效 (4)_结束.mp3')
snd3_损失=pygame.mixer.Sound('python-game-spacecontrol - 副本/sources/music/音效 (6)_损失.mp3')

pygame.mixer.music.set_volume(0.8)
# snd1.set_volume(0.6)

# 创建游戏窗口
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("深空哨站- 太空站资源管理游戏")

# 函数部分

# ---定义---

# 按钮

def draw_button(rect,text,color,hover_color,font=button_font):
    # 获取鼠标点击的位置
    mouse_pos = pygame.mouse.get_pos()
    # 判断点是不是在碰撞箱范围
    is_hover = rect.collidepoint(mouse_pos)

    # 悬停按钮变化
    if is_hover:
        button_color = hover_color
       
    else:
        button_color = color

    # 绘制按钮
    # 按钮底色
    pygame.draw.rect(screen,button_color,rect,border_radius = 8)
    # 按钮边框
    pygame.draw.rect(screen,WHITE,rect,2,border_radius = 8)

    # 按钮文字
    text_surface = font.render(text,True,(0,40,80))
    # 按钮文字的位置
    text_rect = text_surface.get_rect(center = rect.center)
    # 绘制文字到屏幕上
    screen.blit(text_surface,text_rect)

    # 只返回用户的交互信息比如悬停状态，视觉信息内部处理就行
    return is_hover


# 进度条

def draw_resource_bar(resource,value,x,y,width = 200):
    x=90
    y-=180

    pygame.draw.rect(screen,LIGHT_GRAY,(x,y,width,25),border_radius = 4)

    colors = {
            "能源": YELLOW,
            "食物": YELLOW, 
            "水源": YELLOW,
            "氧气": YELLOW,
            "材料": YELLOW
    }

    # max是为了防止数值小于0，min是为了防止数值大于宽度
    fill_width = max(0,min(width,value/100*width))

    # 底色
    pygame.draw.rect(screen,colors[resource],(x,y,width,25),border_radius = 4)
    # 边框
    pygame.draw.rect(screen,WHITE,(x,y,width,25),2,border_radius =4)
    text = f"{resource}: {value}"
    text_surface = small_font.render(text,True,GREEN)
    screen.blit(text_surface,(x-80,y))

# ---逻辑---
# 主要游戏界面的逻辑---
# 结束本日行动

def end_day():
    global day,resources,message

    # 资源
    for module,info in modules.items():
        if module == "太阳能板":
            resources["能源"] += info["效率"]*info["等级"]
        elif module =="水循环系统":
            resources["水源"] += info["效率"]*info["等级"]
        elif module =="氧气生成器":
            resources["氧气"]+=info["效率"]*info["等级"]
        elif module =="温室":
            resources["食物"] += info["效率"]*info["等级"]
        elif module =="采矿机":
            resources["材料"] += info["效率"]*info["等级"]
    
    # 资源消耗
    totle_crew = sum(crew.values())
    consumption = {
        "能源": max(0,2+totle_crew),
        "食物": max(0,1+totle_crew),
        "水源": max(0,1+totle_crew),
        "氧气": max(0,1+totle_crew)
    }
#    资源制造
    production = {
        "能源": min(3 + totle_crew,resources["能源"]),
        "食物": min(2 + totle_crew,resources["食物"]),
        "水源": min(2 + totle_crew,resources["水源"]),
        "氧气": min(1 + totle_crew,resources["氧气"]),
        "材料": min(3 + totle_crew,resources["材料"])
    }

    # 应用资源消耗和制造
    for resource in resources:
        # 没有一一对应导致没有对应到的“材料”出错---解决办法：安全获取，没有消耗就返回0
        # resources[resource] -= consumption[resource]
        resources[resource] -= consumption.get(resource,0)
        resources[resource] += production.get(resource,0)

    day += 1

    # 每日随机事件
    if random.random() < 0.3:
        events = [
            "小行星雨袭击！部分资源受损。",
            "发现新的能源矿脉！",
            "船员健康状况良好。",
            "外星信号检测...但很快消失了。",
            "系统维护完成，效率提升。"
        ]

        message = random.choice(events)

        # 事件影响 
        if "小行星雨" in message:
            damage_resource = random.choice(["能源", "食物", "水源", "氧气"])
            damage = random.randint(10,20)
            resources[damage_resource] = max(0,resources[damage_resource] - damage)
            message += f" {damage_resource}受到了{damage}点伤害。"
        elif"新能源矿脉" in message:
            resources["能源"] += random.randint(10,20)
            message += f" 能源增加了{random.randint(10,20)}点。"
            snd2.play ()
    else:
        message = f"第{day}天结束！资源已更新。"

    check_game_over()

# 模块升级

def update_module():
    global resources,message

    module_name = list(modules.keys())[0]
    module = modules[module_name]
    cost =module["等级"]*20

    if resources["材料"] >=cost:
        resources["材料"] -= cost
        module["等级"] += 1
        message += f"你升级了{module_name}到等级{module['等级']}。"
        snd2.play ()
    else:
        message = "你没有足够的材料来升级模块。"
        snd3_损失.play ()



# 探索行动

def explore():
    global resources,message
    message = "你在附近探索了一会儿，发现了一些新的资源。"
    


    # 默认探索增加的
    resources["材料"] += random.randint(1,3)
    resources["能源"] += random.randint(1,3)
    resources["食物"] -= max(0,random.randint(0,2))
    resources["水源"] -= max(0,random.randint(0,1))
    resources["氧气"] -= max(0,random.randint(0,1))

    # 突发事件
    if resources["能源"]>=30:
        resources["能源"] -= 30
        discoveries = [
            "发现富含矿藏的小行星！获得材料。",
            "找到外星植物样本！获得食物。", 
            "探测到神秘能源信号！获得能源。",
            "发现适宜居住的星球！获得所有资源。"
        ]
        message = random.choice(discoveries)

        if"材料" in message:
            reward = random.randint(4,8)
            resources["材料"]+= reward
            message +=f"你获得了{reward}个材料。"
            snd2.play ()
        elif "食物" in message:
            reward = random.randint(4,8)
            resources["食物"]+= reward
            message +=f"你获得了{reward}个食物。"
            snd2.play ()
        elif"能源" in message:
            reward = random.randint(1,3)
            resources["能源"]+= reward
            message+=f"你获得了{reward}个能源。"
            snd2.play ()
        elif"所有资源" in message:
            for resource in ["能源", "食物", "水源", "氧气", "材料"]:
                resources[resource] +=random.randint(1,3)
                message += f"你获得了{resources[resource]}个{resource}。"
                snd2.play ()
    else:
        message +="目前资源无法支持远距离探索"
        snd3_损失.play ()

# 游戏结束界面的逻辑---
# 检查游戏结束没

def check_game_over():
    global game_over
    if any (value <=0 for value in[resources["能源"],resources["水源"],resources["氧气"],resources["食物"]] ) or day >=20:
        game_over = True
        return True
    else:
        return False

# 游戏重置

def reset_game():
    global day,resources,message,game_over,game_started,modules,crew

    resources = {
        "能源": 50,
        "食物": 30, 
        "水源": 10,
        "氧气": 30,
        "材料": 0
    }
    modules = {
        "太阳能板":{"等级": 1, "效率": 5},
        "水循环系统": {"等级": 1, "效率": 3},
        "氧气生成器": {"等级": 1, "效率": 4},
        "温室": {"等级": 1, "效率": 2},
        "采矿机": {"等级": 1, "效率": 2}
    }
    crew = {
        "工程师": 1,
        "科学家": 1,
        "医生": 1,
        "飞行员": 1
    }

# 界面
# 开始界面---

def draw_start_screen():
    screen.blit(pygame.transform.scale(pygame.image.load("python-game-spacecontrol - 副本/sources/photos/1.png"),(screen_width,screen_height)),(0,0))

    pygame.draw.rect(screen,(BLACK),(210,100,850,250))
    # screen.blit(pygame.transform.scale(pygame.image.load("python-game-spacecontrol - 副本/sources/photos/3.png"),(750,300)),(250,90))

    # 绘制标题
    title_surface = title_font.render("深空哨站-太空资源管理游戏", True, WHITE)
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 200))


    # 按钮
    buttonstart_width,buttonstart_heigh = 200,60
    buttonstart_x = screen_width // 2 - buttonstart_width // 2
    buttonstart_y = 550
    buttonstart_rect =pygame.Rect(buttonstart_x, buttonstart_y, buttonstart_width, buttonstart_heigh)
    draw_button(buttonstart_rect,"开始游戏",GREEN,YELLOW)

    return buttonstart_rect
# 主界面---
def draw_main_interface():
    try:
        screen.blit(pygame.transform.scale(pygame.image.load("python-game-spacecontrol - 副本/sources/photos/2.jpg"),(screen_width,screen_height)),(0,0))
    except :
        screen.fill(BLACK)
    day_surface = title_font.render(f"第{day}天",True,YELLOW)
    screen.blit(day_surface,(1050,30))

    start_y =210
    for resource,value in resources.items():
        draw_resource_bar(resource,value,50,start_y,250)
        start_y += 40

    # 模板面板
    pygame.draw.rect(screen,(0,255,255),(420,150,300,320),border_radius=10)
    panel_title = header_font.render("模板面板",True,(0,40,80))
    screen.blit(panel_title,(510,170))

    # 模块信息
    module_y = 210

    # 动态列表
    for module,info in modules.items():
        text = f"{module}: 等级{info['等级']}(效率{info['效率']})"
        text_surface = small_font.render(text,True,(0,20,40))
        screen.blit(text_surface,(440,module_y+25))
        module_y += 40

    # 船员面板
    pygame.draw.rect(screen,PANEL_BLUE,((screen_width //4)*3-125,150,250,330),border_radius=10)
    panel_title = header_font.render("船员面板",True,(0,40,80))
    screen.blit(panel_title,((screen_width //4)*3-panel_title.get_width() //2,170))

    # 绘制船员信息
    crew_y =210
    for role,count in crew.items():
        text = f"{role}: {count}人"
        text_surface = small_font.render(text,True,(0,20,40))
        screen.blit(text_surface,((screen_width //4)*3 - text_surface.get_width()//2-5,crew_y+20))
        crew_y += 40

    # 绘制消息面板括号里面代表x，y，宽度，高度
    pygame.draw.rect(screen,(0,40,80),(50,500,1190,170),border_radius = 10)
    message_surface = normal_font.render(message,True,PANEL_BLUE)
    screen.blit(message_surface,(screen_width // 2 - message_surface.get_width() // 2,550))

    # 绘制行动按钮
    button_y = 700
    button_width,button_height = 150,50

    buttons = {
        "end_day":pygame.Rect(10,button_y,button_width,button_height),
        "upgrade":pygame.Rect(170,button_y,button_width,button_height),
        "explore":pygame.Rect(330,button_y,button_width,button_height),
        "status":pygame.Rect(490,button_y,button_width,button_height)
    }

    

    # 括号里面的 是悬停状态的颜色（比正常颜色更亮）。因为定义的时候是def draw_button(rect, text, normal_color, hover_color, font):
    draw_button(buttons["end_day"],"结束本日",YELLOW,(255, 240, 100),normal_font)
    draw_button(buttons["upgrade"], "升级模块", YELLOW, (255, 240, 100), normal_font)
    draw_button(buttons["explore"], "探索", YELLOW, (255, 240, 100), normal_font)
    draw_button(buttons["status"], "状态", YELLOW, (255, 240, 100), normal_font)
    
    # 绘制返回按钮
    back_button_rect = pygame.Rect(1165,135,120,50)
    draw_button(back_button_rect,"返回",YELLOW, (0, 230, 120),normal_font)
    
    # print("绘制主界面")

    return buttons,back_button_rect

# 结束界面---
def draw_game_over_screen():
    screen.blit(pygame.transform.scale(pygame.image.load("python-game-spacecontrol - 副本\sources\photos\win.png"),(screen_width,screen_height)),(0,0))
    # screen.fill(BLACK)

    # 重新开始原因
    game_over_text = title_font.render("游戏结束",True,WHITE)
    screen.blit(game_over_text,(100,300))

    # game_over_reason =normal_font.render ("你的资源严重不足导致无人生还。",True,WHITE)
    # screen.blit(game_over_reason,(100,400))

    # 重新开始按钮
    restart_button_width,restart_button_heigh = 200,60
    restart_button_x = screen_width //2- restart_button_width // 2
    restart_button_y = 550

    # 重新开始按钮区域和写过的函数
    restart_button = pygame.Rect(restart_button_x,restart_button_y,restart_button_width,restart_button_heigh)
    draw_button(restart_button,"重新开始",BUTTON_GREEN,BUTTON_HOVER)

    # print("游戏结束")

    return restart_button,game_over_text
# 主游戏逻辑---

# 音乐
pygame.mixer.music.load('python-game-spacecontrol - 副本/sources/music/3_命运2.mp3')
pygame.mixer.music.play(-1,2,50)
print("开始播放音乐")

def main():
 


    # 对全局变量的管理
    global game_started,day,resources,message,game_over

    running = True
    # 存储按钮的位置
    # button_rect = None

    print("游戏启动...")
    
    while running:  
        # 处理事件

        # 游戏中检查是不是拥有游戏结束的条件
        if game_started and not game_over:
            if check_game_over():
                game_over = True
                
       

        
        # 游戏开始和主界面
        if not game_started and not game_over:
            # 开始界面
            # snd3_切换.play ()
            start_buttons_rect = draw_start_screen()
            # 按钮释放内存，防止悬空引用带来的报错
            buttons = None
            back_button_rect = None
        elif  game_started and not game_over:
            # 主界面
            # print("游戏开始")
            # snd3_切换.play ()
            buttons,back_button_rect = draw_main_interface()
        elif game_over :
            # 处理事件
        #    显示结束界面
            # snd3_结束.play ()
            restart_button = draw_game_over_screen()

            # 如果这里清空了值，那么这里就会报错
            # restart_button = None
            
            # reset_game()


         # 更新显示
        pygame.display.flip()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    game_started = True
                elif event.key == pygame.K_ESCAPE:
                    game_started = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    # 开始界面按钮检测
                    button_width, button_height = 200, 60
                    # 按钮的x为屏幕宽度的一半减去按钮宽度的一半
                    button_x = screen_width // 2 - button_width // 2
                    button_y = 550
                    # 按钮的碰撞箱是pygame的碰撞函数的按钮的长宽高和xy
                    start_button = pygame.Rect(button_x, button_y, button_width, button_height)
                    
                    if start_button.collidepoint(event.pos):
                        game_started = True
                        snd1.play ()
                        # snd1=pygame.mixer.music.Sound('python-game-spacecontrol - 副本/sources/music/音效 (2).mp3')
                        # snd1.play ()
                elif game_over:
                    # 对于返回的元组，取第一个元素即restart_button【0】
                    # hasattr是检查是否有某个属性，相当于if restart_button is not None and restart_button != False and restart_button != ""
                    if restart_button and hasattr(restart_button[0], 'collidepoint'):
                        if restart_button[0].collidepoint(event.pos):
                            snd1.play ()
                            reset_game()
                            game_started = False
                            game_over = False
                    
                    # 空格键是1天
                # elif event.key == pygame.K_SPACE and game_started:
                #     day += 1
                #     for resource in resources:
                #         # 获取了游戏运行的毫秒，进行了取模操作，得到了0-19的循环数，再减去了10（偏移）得到了-10到9之间的随机数
                #         change=pygame.time.get_ticks() % 20 - 10
                #         resources[resource] = max(0,resources[resource] + change)


                elif game_started:
                    if buttons and back_button_rect:
                        if buttons["end_day"].collidepoint(event.pos):
                            end_day()
                            snd1.play ()
                        elif buttons["upgrade"].collidepoint(event.pos):
                            update_module()
                            snd1.play ()
                        elif buttons["explore"].collidepoint(event.pos):
                            explore()
                            snd1.play ()
                        elif buttons["status"].collidepoint(event.pos):
                            message = f"状态检查：第{day}天，船员{sum(crew.values())}人"
                            snd1.play ()
                        elif back_button_rect.collidepoint(event.pos):
                            snd1.play ()
                            game_started = False
        clock.tick(FPS)
            
    # 退出游戏
    pygame.quit()
    sys.exit()

# 直接运行name就是main，被导入到其他文件的时候name是文件名
# 只有运行这个文件的时候才会调用main函数，就是运行这个文件
if __name__ == "__main__":
    main()