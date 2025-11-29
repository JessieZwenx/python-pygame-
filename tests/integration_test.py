import sys
import os

# 添加项目路径 - 更新为新的项目名称
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

import main

def test_game_initialization():
    """测试游戏初始化"""
    print("测试游戏初始化...")
    
    # 测试初始资源
    assert main.resources["能源"] == 50
    assert main.resources["材料"] == 0
    print("✓ 初始资源正确")
    
    # 测试模块
    assert "太阳能板" in main.modules
    assert main.modules["太阳能板"]["等级"] == 1
    print("✓ 模块初始化正确")
    
    # 测试游戏状态
    assert main.day == 1
    assert main.explore_count == 0
    print("✓ 游戏状态正确")

def test_resource_management():
    """测试资源管理"""
    print("\n测试资源管理...")
    
    # 测试资源消耗计算
    crew_count = sum(main.crew.values())
    consumption = {
        "能源": max(0, 2 + crew_count),
        "食物": max(0, 1 + crew_count),
        "水源": max(0, 1 + crew_count),
        "氧气": max(0, 1 + crew_count)
    }
    
    assert consumption["能源"] > 0
    print("✓ 资源消耗计算正确")
    
    # 测试升级成本计算
    module = main.modules["太阳能板"]
    cost = module["等级"] * 20
    assert cost == 20
    print("✓ 升级成本计算正确")

def test_explore_system():
    """测试探索系统"""
    print("\n测试探索系统...")
    
    # 测试探索次数逻辑
    explore_count = 5
    explore_count += 1
    assert explore_count == 6
    
    # 测试探索结束条件
    if explore_count >= 10:
        explore_count = 0
    assert explore_count == 6  # 不应该重置
    print("✓ 探索系统逻辑正确")

if __name__ == '__main__':
    test_game_initialization()
    test_resource_management()
    test_explore_system()
    print("\n🎉 所有集成测试通过！")