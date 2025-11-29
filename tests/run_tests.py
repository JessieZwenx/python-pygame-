#!/usr/bin/env python3
"""
python-game-spacecontrol - 副本 - 自动化测试运行器
"""

import unittest
import sys
import os

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行 python-game-spacecontrol 测试套件...")
    print("=" * 60)
    
    # 添加项目路径 - 更新为新的项目名称
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..')
    sys.path.append(project_root)
    
    try:
        # 发现并运行测试
        loader = unittest.TestLoader()
        start_dir = os.path.dirname(__file__)
        suite = loader.discover(start_dir, pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        print("=" * 60)
        if result.wasSuccessful():
            print("🎉 所有测试通过！游戏准备就绪！")
            return True
        else:
            print("❌ 部分测试失败，请检查代码！")
            return False
            
    except Exception as e:
        print(f"💥 测试运行出错: {e}")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)