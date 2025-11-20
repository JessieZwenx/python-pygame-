import pygame
import sys
import random
from pygame.locals import *

# 初始化Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
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

class SpaceStationGameUI:
    def __init__(self):
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("深空哨站 - 太空站资源管理游戏")
        
        # 创建时钟对象
        self.clock = pygame.time.Clock()
        
        # 加载字体
        self.title_font = pygame.font.SysFont('microsoftyahei', 48, bold=True)
        self.header_font = pygame.font.SysFont('microsoftyahei', 32, bold=True)
        self.normal_font = pygame.font.SysFont('microsoftyahei', 24)
        self.small_font = pygame.font.SysFont('microsoftyahei', 20)
        
        # 游戏数据
        self.resources = {
            "能源": 100,
            "食物": 100, 
            "水源": 100,
            "氧气": 100,
            "材料": 50
        }
        
        self.modules = {
            "太阳能板": {"等级": 1, "效率": 5},
            "水循环系统": {"等级": 1, "效率": 3},
            "氧气生成器": {"等级": 1, "效率": 4},
            "温室": {"等级": 1, "效率": 2},
            "采矿机": {"等级": 1, "效率": 2}
        }
        
        self.crew = {
            "工程师": 2,
            "科学家": 1,
            "医生": 1,
            "飞行员": 1
        }
        
        self.day = 1
        self.selected_action = None
        self.message = "欢迎来到深空哨站！"
        
        # 按钮定义
        self.buttons = self.create_buttons()
        
    def create_buttons(self):
        """创建游戏中的按钮"""
        buttons = {
            # 行动按钮
            "end_day": {"rect": pygame.Rect(50, 600, 200, 50), "text": "结束本日", "color": BLUE},
            "upgrade": {"rect": pygame.Rect(270, 600, 200, 50), "text": "升级模块", "color": GREEN},
            "explore": {"rect": pygame.Rect(490, 600, 200, 50), "text": "探索新区域", "color": PURPLE},
            "status": {"rect": pygame.Rect(710, 600, 200, 50), "text": "查看状态", "color": YELLOW},
            
            # 模块升级按钮
            "solar": {"rect": pygame.Rect(300, 200, 150, 40), "text": "太阳能板", "color": LIGHT_GRAY, "visible": False},
            "water": {"rect": pygame.Rect(300, 250, 150, 40), "text": "水循环", "color": LIGHT_GRAY, "visible": False},
            "oxygen": {"rect": pygame.Rect(300, 300, 150, 40), "text": "氧气生成", "color": LIGHT_GRAY, "visible": False},
            "greenhouse": {"rect": pygame.Rect(300, 350, 150, 40), "text": "温室", "color": LIGHT_GRAY, "visible": False},
            "mining": {"rect": pygame.Rect(300, 400, 150, 40), "text": "采矿机", "color": LIGHT_GRAY, "visible": False},
            "back": {"rect": pygame.Rect(300, 450, 150, 40), "text": "返回", "color": RED, "visible": False}
        }
        return buttons
    
    def draw_button(self, button_key):
        """绘制单个按钮"""
        button = self.buttons[button_key]
        if not button.get("visible", True):
            return
            
        # 绘制按钮背景
        pygame.draw.rect(self.screen, button["color"], button["rect"], border_radius=8)
        pygame.draw.rect(self.screen, DARK_GRAY, button["rect"], 2, border_radius=8)
        
        # 绘制按钮文字
        text_surf = self.normal_font.render(button["text"], True, BLACK)
        text_rect = text_surf.get_rect(center=button["rect"].center)
        self.screen.blit(text_surf, text_rect)
    
    def draw_resource_bar(self, resource, value, x, y, width=200):
        """绘制资源条"""
        # 背景
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, width, 25), border_radius=4)
        
        # 填充（根据资源类型不同颜色）
        colors = {
            "能源": YELLOW,
            "食物": GREEN, 
            "水源": BLUE,
            "氧气": WHITE,
            "材料": PURPLE
        }
        fill_width = max(0, min(width, value / 100 * width))
        pygame.draw.rect(self.screen, colors[resource], (x, y, fill_width, 25), border_radius=4)
        
        # 文字
        text = f"{resource}: {int(value)}"
        text_surf = self.small_font.render(text, True, WHITE)
        self.screen.blit(text_surf, (x + 10, y + 4))
    
    def draw_main_interface(self):
        """绘制主界面"""
        # 绘制背景
        self.screen.fill(DARK_BLUE)
        
        # 绘制标题
        title_surf = self.title_font.render("深空哨站 - 太空站资源管理", True, WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 20))
        
        # 绘制天数
        day_surf = self.header_font.render(f"第 {self.day} 天", True, YELLOW)
        self.screen.blit(day_surf, (50, 100))
        
        # 绘制资源区域
        pygame.draw.rect(self.screen, (40, 40, 80), (50, 150, 300, 200), border_radius=10)
        title_surf = self.header_font.render("资源状态", True, WHITE)
        self.screen.blit(title_surf, (60, 160))
        
        # 绘制资源条
        resources_y = 210
        for resource, value in self.resources.items():
            self.draw_resource_bar(resource, value, 70, resources_y)
            resources_y += 35
        
        # 绘制模块区域
        pygame.draw.rect(self.screen, (40, 40, 80), (400, 150, 300, 200), border_radius=10)
        title_surf = self.header_font.render("模块状态", True, WHITE)
        self.screen.blit(title_surf, (410, 160))
        
        # 绘制模块信息
        modules_y = 210
        for module, info in self.modules.items():
            text = f"{module}: 等级{info['等级']} (效率:{info['效率']})"
            text_surf = self.small_font.render(text, True, WHITE)
            self.screen.blit(text_surf, (420, modules_y))
            modules_y += 35
        
        # 绘制船员区域
        pygame.draw.rect(self.screen, (40, 40, 80), (750, 150, 250, 200), border_radius=10)
        title_surf = self.header_font.render("船员状态", True, WHITE)
        self.screen.blit(title_surf, (760, 160))
        
        # 绘制船员信息
        crew_y = 210
        for role, count in self.crew.items():
            text = f"{role}: {count}人"
            text_surf = self.small_font.render(text, True, WHITE)
            self.screen.blit(text_surf, (770, crew_y))
            crew_y += 35
        
        # 绘制消息区域
        pygame.draw.rect(self.screen, (30, 30, 60), (50, 380, 700, 150), border_radius=10)
        message_surf = self.normal_font.render(self.message, True, WHITE)
        self.screen.blit(message_surf, (70, 400))
        
        # 绘制行动按钮
        for button_key in ["end_day", "upgrade", "explore", "status"]:
            self.draw_button(button_key)
    
    def draw_upgrade_interface(self):
        """绘制升级界面"""
        # 绘制背景
        self.screen.fill(DARK_BLUE)
        
        # 绘制标题
        title_surf = self.title_font.render("模块升级", True, WHITE)
        self.screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 50))
        
        # 显示当前材料
        materials_surf = self.header_font.render(f"当前材料: {self.resources['材料']}", True, YELLOW)
        self.screen.blit(materials_surf, (100, 120))
        
        # 显示可升级模块
        y_pos = 200
        for module, info in self.modules.items():
            cost = info["等级"] * 20
            color = GREEN if self.resources["材料"] >= cost else RED
            
            text = f"{module} - 等级{info['等级']} - 升级成本: {cost}材料"
            text_surf = self.normal_font.render(text, True, color)
            self.screen.blit(text_surf, (100, y_pos))
            y_pos += 50
        
        # 显示升级按钮
        for button_key in ["solar", "water", "oxygen", "greenhouse", "mining", "back"]:
            button = self.buttons[button_key]
            button["visible"] = True
            self.draw_button(button_key)
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # 检查按钮点击
                if self.selected_action is None:  # 主界面
                    if self.buttons["end_day"]["rect"].collidepoint(mouse_pos):
                        self.end_day_action()
                    elif self.buttons["upgrade"]["rect"].collidepoint(mouse_pos):
                        self.selected_action = "upgrade"
                    elif self.buttons["explore"]["rect"].collidepoint(mouse_pos):
                        self.explore_action()
                    elif self.buttons["status"]["rect"].collidepoint(mouse_pos):
                        self.message = "当前一切正常！"
                
                elif self.selected_action == "upgrade":  # 升级界面
                    if self.buttons["solar"]["rect"].collidepoint(mouse_pos):
                        self.upgrade_module("太阳能板")
                    elif self.buttons["water"]["rect"].collidepoint(mouse_pos):
                        self.upgrade_module("水循环系统")
                    elif self.buttons["oxygen"]["rect"].collidepoint(mouse_pos):
                        self.upgrade_module("氧气生成器")
                    elif self.buttons["greenhouse"]["rect"].collidepoint(mouse_pos):
                        self.upgrade_module("温室")
                    elif self.buttons["mining"]["rect"].collidepoint(mouse_pos):
                        self.upgrade_module("采矿机")
                    elif self.buttons["back"]["rect"].collidepoint(mouse_pos):
                        self.selected_action = None
                        # 隐藏升级界面按钮
                        for key in ["solar", "water", "oxygen", "greenhouse", "mining", "back"]:
                            self.buttons[key]["visible"] = False
    
    def end_day_action(self):
        """结束本日的行动"""
        # 模拟资源变化
        for resource in self.resources:
            change = random.randint(-10, 20)
            self.resources[resource] = max(0, self.resources[resource] + change)
        
        self.day += 1
        self.message = f"第{self.day}天开始！资源已更新。"
        
        # 随机事件
        if random.random() < 0.3:
            events = [
                "小行星雨袭击！部分模块受损。",
                "发现新的能源矿脉！",
                "船员健康状况良好。",
                "外星信号检测...但很快消失了。"
            ]
            self.message = random.choice(events)
    
    def upgrade_module(self, module_name):
        """升级模块"""
        cost = self.modules[module_name]["等级"] * 20
        
        if self.resources["材料"] >= cost:
            self.resources["材料"] -= cost
            self.modules[module_name]["等级"] += 1
            self.message = f"{module_name}升级到等级{self.modules[module_name]['等级']}！"
        else:
            self.message = "材料不足，无法升级！"
    
    def explore_action(self):
        """探索行动"""
        if self.resources["能源"] >= 30:
            self.resources["能源"] -= 30
            discoveries = [
                "发现富含矿藏的小行星！",
                "找到外星植物样本！", 
                "探测到神秘能源信号！",
                "发现适宜居住的星球！"
            ]
            self.message = random.choice(discoveries)
            
            # 探索奖励
            reward_type = random.choice(["材料", "食物", "能源"])
            reward_amount = random.randint(10, 30)
            self.resources[reward_type] += reward_amount
            self.message += f" 获得{reward_amount}{reward_type}！"
        else:
            self.message = "能源不足，无法进行探索！"
    
    def run(self):
        """主游戏循环"""
        running = True
        
        while running:
            # 处理事件
            self.handle_events()
            
            # 绘制界面
            if self.selected_action == "upgrade":
                self.draw_upgrade_interface()
            else:
                self.draw_main_interface()
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(FPS)

# 启动游戏
if __name__ == "__main__":
    game = SpaceStationGameUI()
    game.run()