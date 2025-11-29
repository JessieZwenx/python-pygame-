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
FPS = 60

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

# 创建游戏窗口
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("深空哨站 - 太空站资源管理游戏")



def main():
    # """主游戏循环"""
    running = True
    
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 屏幕填充为深蓝色
        screen.fill(DARK_BLUE)
        
        # 写界面的地方
        
        # 更新显示
        pygame.display.flip()
        clock = pygame.time.Clock()
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


