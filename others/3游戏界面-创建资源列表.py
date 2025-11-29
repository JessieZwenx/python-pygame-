# 引入需要的库
import pygame
import random
# 优雅退出游戏
import sys
# 不用每次都写pygame.xxx

# 初始化
pygame.init()

# 游戏常量
screen_width = 1024
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
    "能源": 100,
    "食物": 100, 
    "水源": 100,
    "氧气": 100,
    "材料": 50
}

# 模块
modules= {
     "太阳能板": {"等级": 1, "效率": 5},
    "水循环系统": {"等级": 1, "效率": 3},
    "氧气生成器": {"等级": 1, "效率": 4},
    "温室": {"等级": 1, "效率": 2},
    "采矿机": {"等级": 1, "效率": 2}
}

# 天数从1开始
day = 1

# 游戏状态,因为这里只写了游戏的封面，跳转后游戏才开始
game_started = False

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
def draw_intergace():
    # 背景
    screen.fill(BLACK)

    # 绘制标题
    # title_surface 是文字的表面，因为pygame会将文字变成图像也即是表面，然后再绘制
    # 就不能screen.draw_text（”你好“）
    # 分别是---字体对象：标题  （标题内容，抗锯齿，标题颜色）
    title_surface = title_font.render("深空哨站-太空资源管理游戏", True, WHITE)
    # screen.blit是绘制函数，用法是screen.blit(在那个表面，坐标位置)
    
    # screen_width // 2是屏幕宽度的一半，title_surface.get_width() // 2是标题表面的宽度的一半，y是30，表示标题的y坐标
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2,30))

    # 绘制副标题
    subtitle=normal_font.render("你将管理这个太空站，请合理管理资源，避免资源被耗尽！", True, YELLOW)
    screen.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2,100))

    
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
    day_surface = header_font.render(f"第 {day} 天",True,WHITE)
    screen.blit(day_surface,(50,100))

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
        hint_text = normal_font.render("按ESC键返回开始界面",True,(200,200,200))
        screen.blit(hint_text,(screen_width/2 - hint_text.get_width()//2,650))

def main():
    # """主游戏循环"""

    # 游戏正式开始了
    # 对全局变量的管理
    global game_started,day,resources

    running = True
    # 存储按钮的位置
    # button_rect = None
    
    while running:  
        # 处理事件
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    game_started = True
                elif event.key == pygame.K_ESCAPE:
                    game_started = False
                    # 空格键是1天
                elif event.key == pygame.K_SPACE and game_started:
                    day += 1
                    for resource in resources:
                        # 获取了游戏运行的毫秒，进行了取模操作，得到了0-19的循环数，再减去了10（偏移）得到了-10到9之间的随机数
                        change=pygame.time.get_ticks() % 20 - 10
                        resources[resource] = max(0,resources[resource] + change)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started and button_rect:
                    
                    # 如果点击范围在button的碰撞里面
                    if button_rect.collidepoint(event.pos):
                        game_started = True
            

        # 绘制开始界面
        if not game_started:
                button_rect = draw_start_screen()
        else:
                # 绘制游戏的界面
                # # 绘制界面，要在主循环里加这个上面写的标题等才会显示
                draw_intergace()


        
        
        
        # 屏幕填充为深蓝色, 之前的东西会被覆盖
        # screen.fill(DARK_BLUE)
        
        # 写界面的地方
        
        # 更新显示
        pygame.display.flip()
       
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


