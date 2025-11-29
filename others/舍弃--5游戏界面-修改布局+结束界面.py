# 引入需要的库
import pygame
import random
# 优雅退出游戏
import sys
# 不用每次都写pygame.xxx

# 才可以获取另一个文件的某个变量
import os

# 开发者模式
def setup_development_mode():
    """设置开发模式"""
    # 隐藏Pygame支持提示
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    
    # 开发模式信息
    print("🎮 Pygame游戏启动 - 开发模式")
    print("💡 修改代码后保存即可看到变化")
    print("⏹️ 按ESC退出游戏")

# 调用开发模式设置
setup_development_mode()


# 初始化
pygame.init()

# 游戏常量
screen_width = 1280
screen_height = 768


# 颜色定义
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
PANEL_BLUE = (40, 40, 80)
# hover-悬停
BUTTON_HOVER = (0, 220, 100)

# 创建游戏窗口
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("深空哨站 - 太空站资源管理游戏")

# 创建时钟对象
clock = pygame.time.Clock()
FPS = 60

# 加载字体
title_font = pygame.font.SysFont("microsoftyahei",48,bold=True)
header_font = pygame.font.SysFont("microsoftyahei",32,bold=True)
normal_font = pygame.font.SysFont("microsoftyahei",24)
small_font = pygame.font.SysFont("microsoftyahei",20)
button_font = pygame.font.SysFont('microsoftyahei', 32, bold=True)

# 游戏数据
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
     "工程师": 2,
    "科学家": 1,
    "医生": 1,
    "飞行员": 1
}

# 天数从1开始
day = 1

# 游戏状态,因为这里只写了游戏的封面，跳转后游戏才开始
game_started = False
message = "欢迎来到深空哨站"
game_over = False
game_over_reason = ""

# 全局存储按钮的位置存储
button_positions = {
    "buttonstart_rect": None,
    "buttonrestart_rect": None,
}
   


# 按钮的通用函数
def draw_button(rect,text,color,hover_color,font=button_font):
    # 获取鼠标点击where
    mouse_pos = pygame.mouse.get_pos()
    # 判断点击是不是在碰撞箱范围
    is_hover = rect.collidepoint(mouse_pos)

    # 悬停按钮变化
    button_color = hover_color if is_hover else color
    # 绘制按钮底色
    pygame.draw.rect(screen,button_color,rect,border_radius=8)
    # 绘制按钮边框
    pygame.draw.rect(screen,WHITE,rect,2,border_radius =8)

    # 按钮表面的文字
    text_surf = font.render(text,True,WHITE)
    # 按钮文字的where
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf,text_rect)

    # 只返回交互信息，比如悬停状态。而视觉信息比如颜色文字等在内部处理就好，不用返回
    return is_hover

# 开始界面
def draw_start_screen():
    screen.fill(BLACK)

    # 绘制标题
    title_surface = title_font.render("深空哨站-太空资源管理游戏", True, WHITE)
    subtitle_surface=title_font.render("请合理管理资源，避免资源被耗尽！", True, YELLOW)
    screen.blit(title_surface,(screen_width //2 - title_surface.get_width() // 2,150))
    screen.blit(subtitle_surface,(screen_width // 2 - subtitle_surface.get_width() // 2,220))

    # 一些描述
    descriptions = [
        "在遥远的太空中管理你的空间站",
        "平衡资源分配，应对各种危机",
        "探索未知星域，发现新的科技",
        "确保船员的生存和发展"
    ]
    # 对于描述的样式
    # enumerate(元素)--可以获取索引和元素
    for i,desc in enumerate(descriptions):
        desc_surface = normal_font.render(desc,True,WHITE)
        screen.blit(desc_surface,(screen_width // 2 - desc_surface.get_width() // 2,320+i*40))

        # 开始按钮
        buttonstart_width,buttonstart_heigh = 200,60
        buttonstart_x = screen_width // 2 - buttonstart_width // 2
        buttonstart_y = 550

       

        # 检测鼠标是否在按钮上
        mouse_pos = pygame.mouse.get_pos()
        buttonstart_rect = pygame.Rect(buttonstart_x,buttonstart_y,buttonstart_width,buttonstart_heigh)
        # collidepoint检测碰撞是否在矩形内
        is_hover = buttonstart_rect.collidepoint(mouse_pos)

        

        # 悬停按钮变化
        buttonstart_color = BUTTON_HOVER  if is_hover else BUTTON_GREEN
        # 按钮的内部填充
        pygame.draw.rect(screen,buttonstart_color,buttonstart_rect,border_radius=12)
        # 按钮的边框样式，区别在于中间有参数2是边框粗细
        pygame.draw.rect(screen,WHITE,buttonstart_rect,3,border_radius=12)

        # 按钮的文字
        start_text = button_font.render("开始游戏",True,WHITE)
        # 让start_text获取按钮矩形范围，然后按钮的中心作为中心，居中，达成文字整体居中
        text_rect = start_text.get_rect(center=buttonstart_rect.center)
        screen.blit(start_text,text_rect)

        # 绘制提示文字(200,200,200)是颜色
        # hint_text=normal_font.render("鼠标点击任意位置开始游戏",True,(200,200,200))
        # screen.blit(hint_text,(screen_width //2 - hint_text.get_width() // 2,630))
        # # 返回按钮区域用于点击检测，不然就只是图片不会返回按钮点击，一定要有
        return buttonstart_rect
    
    # 绘制资源条
    # 进度条都是bar

# 游戏结束画面
def draw_game_over_screen():
    screen.fill(30,0,0)

    # 绘制游戏结束标题
    title_surface = title_font.render("游戏结束",True,WHITE)
    screen.blit(title_surface,(screen_width //2 - title_surface.get_width() // 2,200))

    # 绘制失败原因
    reason_text = normal_font.render(f"由于{game_over_reason}耗尽，无人生还...",True,YELLOW)
    screen.blit(reason_text,(screen_width //2 - reason_text.get_width() // 2,300))

    # 绘制统计信息
    stats_text = normal_font.render(f"此次生存了{day}天",True,WHITE)
    screen.blit(stats_text,(screen_width //2 - stats_text.get_width() // 2,340))

    # 重新开始按钮
    buttonrestart_width,buttonrestart_heigh = 200,60
    buttonrestart_x = screen_width // 2 - buttonrestart_width // 2
    buttonrestart_y = 450
    buttonrestart_rect = pygame.Rect(buttonrestart_x,buttonrestart_y,buttonrestart_width,buttonrestart_heigh)

    draw_button(buttonrestart_rect,"重新开始",BUTTON_GREEN,BUTTON_HOVER)

    return buttonrestart_rect

# 检查游戏是否结束
def check_game_over():
    global game_over, game_over_reason

    creitical_resources = ["能源","食物","水源","氧气"]
    for resource in creitical_resources:
        if resources[resource]<=0:
            game_over = True
            game_over_reason = f"{resource}耗尽"
            # 游戏结束条件满足，返回true，出现游戏结束画面
            return True
    # 条件不满足，返回false，游戏继续进行
    return False


def reset_game():
    global resources,modules,crew,day,game_over,game_over_reason,message

    resources = {
        "能源": 100,
        "食物": 100, 
        "水源": 100,
        "氧气": 100,
        "材料": 50
    }
    
    # 重置模块
    modules = {
        "太阳能板": {"等级": 1, "效率": 5},
        "水循环系统": {"等级": 1, "效率": 3},
        "氧气生成器": {"等级": 1, "效率": 4},
        "温室": {"等级": 1, "效率": 2},
        "采矿机": {"等级": 1, "效率": 2}
    }
    
    # 重置船员
    crew = {
        "工程师": 2,
        "科学家": 1,
        "医生": 1,
        "飞行员": 1
    }

    day=1
    game_over = False
    game_over_reason = ""
    explored_sectors = 0
    message = ""

# 这里注意缩进，是一个新的函数，要顶左边缩进，不然会报错
def draw_resource_bar(resource,value,x,y,width=200):
    pygame.draw.rect(screen,LIGHT_GRAY,(x,y,width,25),border_radius=4)

    colors = {
            "能源": YELLOW,
            "食物": GREEN, 
            "水源": BLUE,
            "氧气": WHITE,
            "材料": PURPLE
        }

        # max是为了防止数值小于0，min是为了防止数值大于宽度
    fill_width = max(0,min(width,value /100 * width))
        # 底色
    pygame.draw.rect(screen,colors[resource],(x,y,width,25),border_radius=4)
    #    边框
    pygame.draw.rect(screen,WHITE,(x,y,width,25),2,border_radius=4)
    text =f"{resource}: {value}"
    text_surface = small_font.render(text,True,WHITE)
    screen.blit(text_surface,(x+10,y+4))
       
       

    
    


# 绘制用户界面的函数，intergace是接口的意思
# 绘制游戏界面
def draw_main_interface():
    # 背景
    screen.fill(BLACK)

    # 绘制标题
    # title_surface 是文字的表面，因为pygame会将文字变成图像也即是表面，然后再绘制
    # 就不能screen.draw_text（”你好“）
    # 分别是---字体对象：标题  （标题内容，抗锯齿，标题颜色）
    # title_surface = title_font.render("深空哨站-太空资源管理游戏", True, WHITE)
    # screen.blit是绘制函数，用法是screen.blit(在那个表面，坐标位置)
    
    # screen_width // 2是屏幕宽度的一半，title_surface.get_width() // 2是标题表面的宽度的一半，y是30，表示标题的y坐标

    # 绘制副标题
    # subtitle=normal_font.render("你将管理这个太空站，请合理管理资源，避免资源被耗尽！", True, YELLOW)
    # screen.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2,100))

    
    # bug：本来打算直接复制一份之前的，但是后面已知报错显示buttonstart_rect，但是buttonstart_rect在函数里没有定义，所以报错。最后决定用按钮的通用函数返回上一级菜单
    # # 返回按钮
    # buttonsreturn_width,buttonreturn_heigh = 200,60
    # buttonreturn_x = screen_width // 2 - buttonsreturn_width // 2
    # buttonreturn_y = 650
    
    # # 检测鼠标是否在按钮上
    # mouse_pos = pygame.mouse.get_pos()
    # buttonreturn_rect = pygame.Rect(buttonreturn_x,buttonreturn_y,buttonsreturn_width,buttonreturn_heigh)
    #     # collidepoint检测碰撞是否在矩形内
    # is_hover = buttonreturn_rect.collidepoint(mouse_pos)

        

    #     # 悬停按钮变化
    # buttonreturn_color = BUTTON_HOVER  if is_hover else BUTTON_GREEN
    #     # 按钮的内部填充
    # pygame.draw.rect(screen,buttonreturn_color,buttonreturn_rect)
    #     # 按钮的边框样式，区别在于中间有参数2是边框粗细
    # pygame.draw.rect(screen,WHITE,buttonreturn_rect,3)

    #     # 按钮的文字
    # start_text = button_font.render("返回",True,WHITE)
    #     # 让start_text获取按钮矩形范围，然后按钮的中心作为中心，居中，达成文字整体居中
    # text_rect = start_text.get_rect(center=buttonreturn_rect.center)
    # screen.blit(start_text,text_rect)

    #     # 绘制提示文字(200,200,200)是颜色
    #     # hint_text=normal_font.render("鼠标点击任意位置开始游戏",True,(200,200,200))
    #     # screen.blit(hint_text,(screen_width //2 - hint_text.get_width() // 2,630))
    #     # # 返回按钮区域用于点击检测，不然就只是图片不会返回按钮点击，一定要有
    # return buttonreturn_rect

    # 绘制天数
    day_surface = title_font.render(f"第 {day} 天",True,WHITE)
    screen.blit(day_surface,(screen_width //2-day_surface.get_width() //2,60))

    # 资源面板
    pygame.draw.rect(screen,PANEL_BLUE,(400,150,300,250),border_radius=10)
    panel_title = header_font.render("资源面板",True,WHITE)
    screen.blit(panel_title,(60,160))


# 注意缩进，这些都是再第二个界面中的绘制的，所以应该是再函数里面的锁进位置

# 资源显示条的布局
# 开始y
    start_y = 210
    for resource,value in resources.items():
       draw_resource_bar (resource,value,40,start_y,250)
       start_y += 40

# 绘制模块面板
# 中间括号是长宽高
    pygame.draw.rect(screen,PANEL_BLUE,(400,150,300,250),border_radius=10)
    panel_title = header_font.render("模块状态",True,WHITE)
    screen.blit(panel_title,(410,160))

# 绘制模块信息
    module_y = 210
# 动态列表，遍历所有模块。如果有info.append（）或者有info.pop（）就是长度或内容随时变化啊 的动态列表
    for module,info in modules.items():
        # 等级就是获取等级，以此类推
        text = f"{module}: 等级{info['等级']} (效率:{info['效率']})"
        text_surface = small_font.render(text,True,WHITE)
        screen.blit(text_surface,(420,module_y))
        module_y += 40

        # 绘制返回提示
        # hint_text = normal_font.render("按ESC键返回开始界面",True,(200,200,200))
        # screen.blit(hint_text,(screen_width/2 - hint_text.get_width()//2,650))

    # 绘制船员面板
    pygame.draw.rect(screen,PANEL_BLUE,(750,150,250,250),border_radius=10)
    panel_title = header_font.render("船员状态",True,WHITE)
    screen.blit(panel_title,(760,160))

    # 绘制船员信息
    crew_y = 210
    for role,count in crew.items():
        text = f"{role}: {count}人"
        text_surface = small_font.render(text,True,WHITE)
        screen.blit(text_surface,(770,crew_y))
        crew_y +=40

    # 绘制消息面板括号里面代表x，y，宽度，高度
    pygame.draw.rect(screen,PANEL_BLUE,(screen_width //2 -  600,500,1200,190),border_radius=10)
    message_surface = normal_font.render(message,True,WHITE)
    screen.blit(message_surface,(screen_width //2 - message_surface.get_width() //2,550))

    # 绘制行动按钮
    button_y = 700
    button_width,button_height = 150,50

    buttons = {
        "end_day":pygame.Rect(1120,button_y,button_width,button_height),
        "upgrade":pygame.Rect(10,button_y,button_width,button_height),
        "explore":pygame.Rect(180,button_y,button_width,button_height),
        "status":pygame.Rect(350,button_y,button_width,button_height)
    }
    # 括号里面的 是悬停状态的颜色（比正常颜色更亮）。因为定义的时候是def draw_button(rect, text, normal_color, hover_color, font):
    draw_button(buttons["end_day"],"结束本日",BLUE,(0,150,255),normal_font)
    draw_button(buttons["upgrade"], "升级模块", GREEN, (0, 230, 120), normal_font)
    draw_button(buttons["explore"], "探索", PURPLE, (200, 120, 255), normal_font)
    draw_button(buttons["status"], "状态", YELLOW, (255, 240, 100), normal_font)
    
    # 绘制返回按钮
    back_button_rect = pygame.Rect(10,10,120,50)
    draw_button(back_button_rect,"返回",GREEN, (0, 230, 120),normal_font)
    
    return buttons,back_button_rect

def end_day():
    # 结束本日行动
    global day,resources,message

    # 对于资源
    for module,info in modules.items():
        if module == "太阳能板":
            resources["能源"] += info["效率"] * info["等级"]
        elif module == "水循环系统":
            resources["水源"] += info["效率"] * info["等级"]
        elif module == "氧气生成器":
            resources["氧气"] += info["效率"] * info["等级"]
        elif module == "温室":
            resources["食物"] += info["效率"] * info["等级"]
        elif module == "采矿机":
            resources["材料"] += info["效率"] * info["等级"]

    # 对于资源损耗
    totle_crew = sum(crew.values())
    consumption = {
        "能源": 10 + totle_crew,
        "食物": 8 + totle_crew,
        "水源": 6 + totle_crew,
        "氧气": 5 + totle_crew
    }
    # 从资源中减去消耗
    for resource,anmount in consumption.items():
        resources[resource] = max(0,resources[resource] - anmount)

    day += 1

    # 随机事件
    # 有百分之三十的概率发生随机事件
    if random.random() < 0.3:
        events = [
            "小行星雨袭击！部分资源受损。",
            "发现新的能源矿脉！",
            "船员健康状况良好。",
            "外星信号检测...但很快消失了。",
            "系统维护完成，效率提升。"
        ]

        message = random.choice(events)

        # 事件带来的影响
        if "小行星雨" in message:
            damaged_resource = random.choice(["能源", "食物", "水源", "氧气"])
            damage = random.randint(10, 20)
            resources[damaged_resource] = max(0,resources[damaged_resource] - damage)
            message += f" {damaged_resource}受到了{damage}点伤害。"
        elif "能源矿脉" in message:
            resources["能源"] += random.randint(10,20)
            message += f" 能源增加了{random.randint(10,20)}点。"
    else:
        message = f"第{day}天结束！资源已更新。"

# 模块升级
def upgrade_module():
    global resources,message

    module_name = list(modules.keys())[0]
    module = modules[module_name]
    cost = module["等级"] * 20

    if resources["材料"] >=cost:
        resources["材料"] -= cost
        module["等级"] += 1
        message = f"{module_name}升级到等级{module['等级']}！"
    else:
        message = "材料不足，无法升级！"

# 探索行动
def explore():
    global resources,message
    message = "你在附近探索了一会儿，发现了一些新的资源。"

    # 默认探索增加的
    resources["材料"] += random.randint(5,10)
    resources["能源"] += random.randint(5,10)
    resources["食物"] -= random.randint(0,5)
    resources["水源"] -= max(0,random.randint(0,5))
    resources["氧气"] -= max(0,random.randint(0,5))

    # 事件影响的
    if resources["能源"] >=30:
        resources["能源"] -= 30
        discoveries = [
            "发现富含矿藏的小行星！获得材料。",
            "找到外星植物样本！获得食物。", 
            "探测到神秘能源信号！获得能源。",
            "发现适宜居住的星球！获得所有资源。"
        ]
        message = random.choice(discoveries)

        if"材料"in message:
            reward = random.randint(10,20)
            resources["材料"] += reward
            message += f" 获得{reward}点材料。"
        elif "食物"in message:
            reward = random.randint(10,20)
            resources["食物"]+=reward
            message += f" 获得{reward}点食物。"
        elif "能源" in message:
            reward = random.randint
            resources["能源"]+=reward
            message += f" 获得{reward}点能源。"
        elif "所有资源" in message:
            for resource in ["能源", "食物", "水源", "氧气", "材料"]:
                resources[resource] += random.randint(5,15)
                message += f" 获得{resources[resource]}点{resource}。"
    else:     
        message += " 目前资源无法支持远距离探索。"

def main():
    # """主游戏循环"""

    # 游戏正式开始了
    # 对全局变量的管理
    global game_started,day,resources,message

    running = True
    # 存储按钮的位置
    # buttonstart_rect = None

    print("游戏启动...")
    
    while running:  

        if game_started and not game_over:
            check_game_over()


        # 处理事件
        
        if not game_started:
            # 开始界面
            buttonstart_rect = draw_start_screen()
            # 按钮释放内存，防止悬空引用带来的报错
            buttons = None
            buttonrestart_rect = None
        elif game_over:
            buttonrestart_rect = draw_game_over_screen()
            buttons = None
            buttonrestart_rect = None
        else:
            # 主界面
            buttons,buttonrestart_rect = draw_main_interface()

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
                    buttonstart_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                    
                    if buttonstart_rect.collidepoint(event.pos):
                        game_started = True
            
            # 游戏结束界面的按钮
                elif game_over:
                    button_width,button_height = 200,60
                    button_x = screen_width // 2 - button_width // 2
                    button_y = 550
                    restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                    if restart_button_rect.collidepoint(event.pos):
                        reset_game()
                        game_started = False
                    
                    # 空格键是1天
                # elif event.key == pygame.K_SPACE and game_started:
                #     day += 1
                #     for resource in resources:
                #         # 获取了游戏运行的毫秒，进行了取模操作，得到了0-19的循环数，再减去了10（偏移）得到了-10到9之间的随机数
                #         change=pygame.time.get_ticks() % 20 - 10
                #         resources[resource] = max(0,resources[resource] + change)


                    else:
                        if buttons and buttonrestart_rect:
                            if buttons["end_day"].collidepoint(event.pos):
                                end_day()
                            elif buttons["upgrade"].collidepoint(event.pos):
                                upgrade_module()
                            elif buttons["explore"].collidepoint(event.pos):
                                explore()
                            elif buttons["status"].collidepoint(event.pos):
                                message = f"状态检查：第{day}天，船员{sum(crew.values())}人"

                            elif buttonrestart_rect.collidepoint(event.pos):
                                game_started = False
                

        # 绘制开始界面
        # if not game_started:
        #         button_rect = draw_start_screen()
        # else:
        #         # 绘制游戏的界面
        #         # # 绘制界面，要在主循环里加这个上面写的标题等才会显示
        #         draw_main_interface()
        

        
        
        
        # 屏幕填充为深蓝色, 之前的东西会被覆盖
        # screen.fill(DARK_BLUE)
        
       
       
            # 控制帧率
        clock.tick(FPS)
    
    # 退出游戏
    pygame.quit()
    sys.exit()

# 直接运行name就是main，被导入到其他文件的时候name是文件名
# 只有运行这个文件的时候才会调用main函数，就是运行这个文件
if __name__ == "__main__":
    main()


# 例子 # 只有明确运行时才执行初始化
# if __name__ == "__main__":
#     print("你确定要初始化数据库吗？")
#     response = input("输入 'YES' 确认: ")
#     if response == "YES":
#         init_database()


