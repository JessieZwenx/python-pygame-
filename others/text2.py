import pygame
import sys
import random
import os

# 初始化Pygame
pygame.init()

# 设置窗口尺寸
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 60, 120)
PANEL_BLUE = (40, 40, 80)
YELLOW = (255, 220, 0)
GREEN = (0, 200, 100)
BLUE = (0, 120, 255)
RED = (255, 80, 80)
PURPLE = (180, 100, 240)
BUTTON_GREEN = (0, 180, 80)
BUTTON_HOVER = (0, 220, 100)
RED_HOVER = (255, 120, 120)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("深空哨站 - 太空站资源管理游戏")

# 创建时钟对象
clock = pygame.time.Clock()
FPS = 60

# 加载字体
title_font = pygame.font.SysFont('microsoftyahei', 48, bold=True)
header_font = pygame.font.SysFont('microsoftyahei', 32, bold=True)
normal_font = pygame.font.SysFont('microsoftyahei', 24)
small_font = pygame.font.SysFont('microsoftyahei', 20)
button_font = pygame.font.SysFont('microsoftyahei', 32, bold=True)

# 游戏数据
resources = {
    "能源": 100,
    "食物": 100, 
    "水源": 100,
    "氧气": 100,
    "材料": 50
}

modules = {
    "太阳能板": {"等级": 1, "效率": 5},
    "水循环系统": {"等级": 1, "效率": 3},
    "氧气生成器": {"等级": 1, "效率": 4},
    "温室": {"等级": 1, "效率": 2},
    "采矿机": {"等级": 1, "效率": 2}
}

crew = {
    "工程师": 2,
    "科学家": 1,
    "医生": 1,
    "飞行员": 1
}

day = 1
game_started = False
# ==================== 红色修改开始 ====================
game_over = False
game_over_reason = ""
# ==================== 红色修改结束 ====================
message = "欢迎来到深空哨站！"

def draw_button(rect, text, color, hover_color, font=button_font):
    """绘制按钮的通用函数"""
    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse_pos)
    
    button_color = hover_color if is_hover else color
    pygame.draw.rect(screen, button_color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    return is_hover

def draw_resource_bar(resource, value, x, y, width=200):
    """绘制资源条"""
    # 背景
    pygame.draw.rect(screen, BLACK, (x, y, width, 25), border_radius=4)
    
    # 填充（根据资源类型不同颜色）
    colors = {
        "能源": YELLOW,
        "食物": GREEN, 
        "水源": BLUE,
        "氧气": WHITE,
        "材料": PURPLE
    }
    fill_width = max(0, min(width, value / 100 * width))
    pygame.draw.rect(screen, colors[resource], (x, y, fill_width, 25), border_radius=4)
    
    # 边框
    pygame.draw.rect(screen, WHITE, (x, y, width, 25), 2, border_radius=4)
    
    # 文字
    text = f"{resource}: {int(value)}"
    text_surf = small_font.render(text, True, WHITE)
    screen.blit(text_surf, (x + 10, y + 4))

def draw_start_screen():
    """绘制开始界面"""
    screen.fill(DARK_BLUE)
    
    # 星空背景
    for i in range(100):
        x = pygame.time.get_ticks() % SCREEN_WIDTH + i * 10
        y = (i * 7) % SCREEN_HEIGHT
        size = (i % 3) + 1
        brightness = 150 + (i % 105)
        pygame.draw.circle(screen, (brightness, brightness, brightness), 
                          (x % SCREEN_WIDTH, y), size)
    
    # 标题
    title_surface = title_font.render("深空哨站", True, WHITE)
    subtitle_surface = title_font.render("太空站资源管理游戏", True, YELLOW)
    
    screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 150))
    screen.blit(subtitle_surface, (SCREEN_WIDTH//2 - subtitle_surface.get_width()//2, 220))
    
    # 游戏描述
    descriptions = [
        "在遥远的太空中管理你的空间站",
        "平衡资源分配，应对各种危机",
        "探索未知星域，发现新的科技",
        "确保船员的生存和发展"
    ]
    
    for i, desc in enumerate(descriptions):
        desc_surface = normal_font.render(desc, True, WHITE)
        screen.blit(desc_surface, (SCREEN_WIDTH//2 - desc_surface.get_width()//2, 320 + i * 40))
    
    # 开始按钮
    button_width, button_height = 200, 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = 550
    start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    draw_button(start_button_rect, "开始游戏", BUTTON_GREEN, BUTTON_HOVER)
    
    # 提示文字
    hint_text = normal_font.render("点击开始按钮或按任意键开始游戏", True, (200, 200, 200))
    screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 630))
    
    return start_button_rect

# ==================== 红色修改开始 ====================
def draw_game_over_screen():
    """绘制游戏结束界面"""
    screen.fill((30, 0, 0))  # 深红色背景
    
    # 绘制游戏结束标题
    game_over_text = title_font.render("游戏结束", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 200))
    
    # 绘制失败原因
    reason_text = header_font.render(f"因为 {game_over_reason} 耗尽", True, YELLOW)
    screen.blit(reason_text, (SCREEN_WIDTH//2 - reason_text.get_width()//2, 280))
    
    # 绘制统计信息
    stats_font = normal_font
    stats_text = stats_font.render(f"你生存了 {day} 天，", True, WHITE)
    screen.blit(stats_text, (SCREEN_WIDTH//2 - stats_text.get_width()//2, 340))
    
    # 绘制重新开始按钮
    button_width, button_height = 200, 60
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_y = 450
    restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    draw_button(restart_button_rect, "重新开始", BUTTON_GREEN, BUTTON_HOVER)
    
    # 绘制提示文字
    hint_text = normal_font.render("点击重新开始按钮返回开始界面", True, (200, 200, 200))
    screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 530))
    
    return restart_button_rect

def check_game_over():
    """检查游戏是否结束"""
    global game_over, game_over_reason
    
    critical_resources = ["能源", "水源", "氧气"]
    for resource in critical_resources:
        if resources[resource] <= 0:
            game_over = True
            game_over_reason = resource
            return True
    return False

def reset_game():
    """重置游戏状态"""
    global resources, modules, crew, day, game_over, game_over_reason, message
    
    # 重置资源
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
    
    # 重置游戏状态
    day = 1
    game_over = False
    game_over_reason = ""
    explored_sectors = 0
    message = "游戏已重新开始！"
# ==================== 红色修改结束 ====================

def draw_main_interface():
    """绘制主游戏界面"""
    global message
    
    # 绘制背景
    screen.fill(DARK_BLUE)
    
    # 绘制标题
    title_surface = title_font.render("深空哨站 - 太空站资源管理", True, WHITE)
    screen.blit(title_surface, (SCREEN_WIDTH//2 - title_surface.get_width()//2, 20))
    
    # 绘制天数信息
    day_surface = header_font.render(f"第 {day} 天", True, YELLOW)
    screen.blit(day_surface, (50, 100))
    
    # 绘制资源面板
    pygame.draw.rect(screen, PANEL_BLUE, (50, 150, 300, 250), border_radius=10)
    panel_title = header_font.render("资源状态", True, WHITE)
    screen.blit(panel_title, (60, 160))
    
    # 绘制资源条
    start_y = 210
    for resource, value in resources.items():
        draw_resource_bar(resource, value, 70, start_y, 250)
        start_y += 40
    
    # 绘制模块面板
    pygame.draw.rect(screen, PANEL_BLUE, (400, 150, 300, 250), border_radius=10)
    panel_title = header_font.render("模块状态", True, WHITE)
    screen.blit(panel_title, (410, 160))
    
    # 绘制模块信息
    module_y = 210
    for module, info in modules.items():
        text = f"{module}: 等级{info['等级']} (效率:{info['效率']})"
        text_surface = small_font.render(text, True, WHITE)
        screen.blit(text_surface, (420, module_y))
        module_y += 40
    
    # 绘制船员面板
    pygame.draw.rect(screen, PANEL_BLUE, (750, 150, 250, 250), border_radius=10)
    panel_title = header_font.render("船员状态", True, WHITE)
    screen.blit(panel_title, (760, 160))
    
    # 绘制船员信息
    crew_y = 210
    for role, count in crew.items():
        text = f"{role}: {count}人"
        text_surface = small_font.render(text, True, WHITE)
        screen.blit(text_surface, (770, crew_y))
        crew_y += 40
    
    # 绘制消息面板
    pygame.draw.rect(screen, PANEL_BLUE, (50, 420, 700, 100), border_radius=10)
    message_surface = normal_font.render(message, True, WHITE)
    screen.blit(message_surface, (70, 450))
    
    # 绘制行动按钮
    button_y = 550
    button_width, button_height = 150, 50
    
    buttons = {
        "end_day": pygame.Rect(50, button_y, button_width, button_height),
        "upgrade": pygame.Rect(220, button_y, button_width, button_height),
        "explore": pygame.Rect(390, button_y, button_width, button_height),
        "status": pygame.Rect(560, button_y, button_width, button_height)
    }
    
    draw_button(buttons["end_day"], "结束本日", BLUE, (0, 150, 255), normal_font)
    draw_button(buttons["upgrade"], "升级模块", GREEN, (0, 230, 120), normal_font)
    draw_button(buttons["explore"], "探索", PURPLE, (200, 120, 255), normal_font)
    draw_button(buttons["status"], "状态", YELLOW, (255, 240, 100), normal_font)
    
    # 绘制返回按钮
    back_button_rect = pygame.Rect(750, button_y, 120, 50)
    draw_button(back_button_rect, "返回", RED, RED_HOVER, normal_font)
    
    # 绘制提示文字
    hint_text = normal_font.render("按ESC键或点击返回按钮返回开始界面", True, (200, 200, 200))
    screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 620))
    
    return buttons, back_button_rect

def end_day():
    """结束本日的行动"""
    global day, resources, message
    
    # 资源生产
    for module, info in modules.items():
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
    
    # 资源消耗
    total_crew = sum(crew.values())
    consumption = {
        "能源": 10 + total_crew,
        "食物": 8 + total_crew,
        "水源": 6 + total_crew,
        "氧气": 5 + total_crew
    }
    
    for resource, amount in consumption.items():
        resources[resource] = max(0, resources[resource] - amount)
    
    day += 1
    
    # 随机事件
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
            damaged_resource = random.choice(["能源", "食物", "水源", "氧气"])
            damage = random.randint(10, 20)
            resources[damaged_resource] = max(0, resources[damaged_resource] - damage)
        elif "能源矿脉" in message:
            resources["能源"] += random.randint(15, 25)
    else:
        message = f"第{day}天开始！资源已更新。"

def upgrade_module():
    """升级模块"""
    global resources, message
    
    # 简单的升级逻辑：升级第一个模块
    module_name = list(modules.keys())[0]
    module = modules[module_name]
    cost = module["等级"] * 20
    
    if resources["材料"] >= cost:
        resources["材料"] -= cost
        module["等级"] += 1
        message = f"{module_name}升级到等级{module['等级']}！"
    else:
        message = "材料不足，无法升级！"

def explore():
    """探索行动"""
    global resources, message, explored_sectors
    
    if resources["能源"] >= 30:
        resources["能源"] -= 30
        discoveries = [
            "发现富含矿藏的小行星！获得材料。",
            "找到外星植物样本！获得食物。", 
            "探测到神秘能源信号！获得能源。",
            "发现适宜居住的星球！获得所有资源。"
        ]
        message = random.choice(discoveries)
        explored_sectors += 1
        
        # 探索奖励
        if "材料" in message:
            reward = random.randint(10, 20)
            resources["材料"] += reward
        elif "食物" in message:
            reward = random.randint(10, 20)
            resources["食物"] += reward
        elif "能源" in message:
            reward = random.randint(15, 25)
            resources["能源"] += reward
        else:  # 所有资源
            for resource in ["能源", "食物", "水源", "氧气", "材料"]:
                resources[resource] += random.randint(5, 15)
    else:
        message = "能源不足，无法进行探索！"

def main():
    """主游戏循环"""
    global game_started, day, resources, message, game_over, game_over_reason
    
    running = True
    explored_sectors = 0
    
    print("游戏启动成功！")
    
    while running:
        # ==================== 红色修改开始 ====================
        # 检查游戏是否结束
        if game_started and not game_over:
            check_game_over()
        # ==================== 红色修改结束 ====================
        
        # 绘制界面
        if not game_started:
            start_button_rect = draw_start_screen()
            buttons = None
            back_button_rect = None
        # ==================== 红色修改开始 ====================
        elif game_over:
            restart_button_rect = draw_game_over_screen()
            buttons = None
            back_button_rect = None
        # ==================== 红色修改结束 ====================
        else:
            buttons, back_button_rect = draw_main_interface()
        
        # 更新显示
        pygame.display.flip()
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if not game_started:
                    game_started = True
                    message = "欢迎来到深空哨站管理界面！"
                elif event.key == pygame.K_ESCAPE:
                    game_started = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    # 开始界面按钮检测
                    button_width, button_height = 200, 60
                    button_x = SCREEN_WIDTH // 2 - button_width // 2
                    button_y = 550
                    start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                    
                    if start_button_rect.collidepoint(event.pos):
                        game_started = True
                        message = "欢迎来到深空哨站管理界面！"
                
                # ==================== 红色修改开始 ====================
                elif game_over:
                    # 游戏结束界面按钮检测
                    button_width, button_height = 200, 60
                    button_x = SCREEN_WIDTH // 2 - button_width // 2
                    button_y = 450
                    restart_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                    
                    if restart_button_rect.collidepoint(event.pos):
                        reset_game()
                        game_started = False
                # ==================== 红色修改结束 ====================
                
                else:
                    # 主游戏界面按钮检测
                    if buttons and back_button_rect:
                        if buttons["end_day"].collidepoint(event.pos):
                            end_day()
                        elif buttons["upgrade"].collidepoint(event.pos):
                            upgrade_module()
                        elif buttons["explore"].collidepoint(event.pos):
                            explore()
                        elif buttons["status"].collidepoint(event.pos):
                            message = f"状态检查：第{day}天，船员{sum(crew.values())}人"
                        elif back_button_rect.collidepoint(event.pos):
                            game_started = False
        
        # 控制帧率
        clock.tick(FPS)
    
    # 退出游戏
    pygame.quit()
    sys.exit()

try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"程序出错: {e}")
    input("按回车键退出...")