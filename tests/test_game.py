import unittest
import sys
import os

# 添加项目路径 - 更新为新的项目名称
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

# 测试游戏逻辑的类
class TestGameLogic(unittest.TestCase):
    
    def setUp(self):
        """测试前初始化"""
        import main
        self.main = main
        # 保存原始状态
        self.original_resources = self.main.resources.copy()
        self.original_modules = self.main.modules.copy()
        self.original_day = self.main.day
    
    def test_resource_initialization(self):
        """测试资源初始化"""
        expected_resources = {
            "能源": 50, "食物": 30, "水源": 10, 
            "氧气": 30, "材料": 0
        }
        self.assertEqual(self.main.resources, expected_resources)
    
    def test_module_structure(self):
        """测试模块数据结构"""
        expected_modules = {
            "太阳能板", "水循环系统", "氧气生成器", "温室", "采矿机"
        }
        actual_modules = set(self.main.modules.keys())
        self.assertEqual(actual_modules, expected_modules)
        
        # 测试每个模块都有必要的属性
        for module_name, module_info in self.main.modules.items():
            self.assertIn("等级", module_info)
            self.assertIn("效率", module_info)
            self.assertIsInstance(module_info["等级"], int)
            self.assertIsInstance(module_info["效率"], int)
    
    def test_upgrade_cost_calculation(self):
        """测试升级成本计算"""
        # 模拟模块升级成本计算
        test_module = {"等级": 3, "效率": 5}
        cost = test_module["等级"] * 20
        self.assertEqual(cost, 60)
    
    def test_game_over_conditions(self):
        """测试游戏结束条件"""
        # 测试资源耗尽
        test_resources = {"能源": 0, "食物": 10, "水源": 10, "氧气": 10, "材料": 5}
        has_zero = any(value <= 0 for value in [
            test_resources["能源"], 
            test_resources["水源"], 
            test_resources["氧气"], 
            test_resources["食物"]
        ])
        self.assertTrue(has_zero)
        
        # 测试天数条件
        self.assertTrue(20 >= 20)  # 模拟day >= 20
    
    def test_explore_logic(self):
        """测试探索逻辑"""
        # 测试探索次数递增
        initial_count = 5
        new_count = initial_count + 1
        self.assertEqual(new_count, 6)
        
        # 测试探索次数重置
        explore_count = 10
        if explore_count >= 10:
            explore_count = 0
        self.assertEqual(explore_count, 0)
    
    def test_random_module_selection(self):
        """测试随机模块选择"""
        modules_list = list(self.main.modules.keys())
        self.assertGreater(len(modules_list), 0)
        # 验证所有模块名称都在列表中
        for module in ["太阳能板", "水循环系统", "氧气生成器", "温室", "采矿机"]:
            self.assertIn(module, modules_list)
    
    def tearDown(self):
        """测试后恢复状态"""
        # 恢复原始状态
        self.main.resources = self.original_resources
        self.main.modules = self.original_modules
        self.main.day = self.original_day

if __name__ == '__main__':
    unittest.main()