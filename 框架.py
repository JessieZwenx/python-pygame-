#引入游戏库
import pygame
#引入随机数
import random
#引入系统
import sys
#引入时间模块
import time
#导入数据类装饰器，创建简单数据类用
from dataclasses import dataclass
# 导入类型提示模块，用于类型注解
from typing import Dict,List,Optional


@dataclass
class Module:
    """模块数据类，表示太空站的功能模块"""
    # 模块名称
    name:str
    # 模块初始等级
    levelLint = 1
    # 模块初始效率
    efficiency:int = 0
    # 升级基本成本，默认值是20
    base_cost:int = 20

class SpaceStationGame:
    """主要游戏类，用于管理主要游戏的数据"""


    def __init__(self):
        """初始化游戏数据"""

        self.resources = {
            "energy":100,
            "food":100,
            "water":100,
            "oxyen":100,
            "material":50
        }


        #用module对象存储5个功能的模块信息
        self.modules ={
            "solor_panel":Module("太阳能版",efficiency=5),
            "water_recycler":Module("水循环系统",efficiency=3),
            "oxygen_generator":Module("氧气生成器",efficiency=4),
            "greenhouse":Module("温室系统",efficiency=2),
            "mining_drill":Module("采矿",efficiency=2)
        }


        #人员系统-四个职业
        self.crew={
            "engineer":2,
            "scientist":1,
            "doctor":1,
            "pilot":1
        }

        #游戏状态管理-存储游戏进度和状态信息
        self.game_state={
            # 当前游戏天数1开始
            "day":1,
            # 探索了的区域开始是0
            "explored_sectors":0,
            # 危机事件冷却时间，默认是0
            "crisis_cooldowm":0,
            # 游戏结束了吗
            "is_game_over":False,
            # 游戏结束的原因
            "game_over_reason":""

        }

        # 发现记录系统-存储玩家在探索中发现的项目

        # 发现列表，默认是空
        self.discoveries = []

        #游戏配置-存储游戏平衡参数，用于调整难度
        self.config={
            # 基础消耗的数值
            "base_consumption":{
                "energy":10,
                "food":8,
                "water":6,
                "oxygen":5
            },
            # 其他数值
            "crisis_probablity":0.1,
            "exploration_cost":30
        }

    # 更新游戏状态字典中的特定键值对，即新发现新推进
    # 更新类的任何字符串类型，只修改内部状态不返回值
    def update_game_state(self,key:str,value:any)->None:
        # 如果存在就更新，不存在就报错.用于更新，防止无效的被添加
        if key in self.game_state:
            self.game_state[key] = value
        else:
            print(f"错误,{ key }不存在")

    # 获取游戏状态字典中的特定键值对,存在就返回值，不存在就返回None，用于获取和表示，并防止无效的造成崩溃
    def get_game_state(self,key:str) -> any:
        return self.game_state.get(key,None)
    
    def increment_day(self)->None:
        """增加游戏天数"""
        self.game_state["day"] +=1

    # 完成添加用none，返回值用any
    def add_discovery(self,discovery:str) -> None:
        """添加新的发现"""

        if discovery not in self.discoveries:
            self.discoveries.append(discovery)
            print(f"发现{discovery}!")

    # 用dict【str，str】批量返回多个值
    # 检查所有资源等级并返回警告等级
    def check_resource_levels(self)->Dict[str,str]:
        warnings ={}
        for resource,amount in self.resources.items():
            if amount < 20:
                warnings[resource] = "严重警告！资源不足"
            if amount < 50:
                warnings[resource] = "警告！需要及时补充资源"
            else:
                warnings[resource] = "正常"
        return warnings

# 修改特定资源的数量，返回操作是否成功
def modify_resource(self,resource: str,amout:int) -> bool:
    # 如果更改后数值大于0就输出，不然就报错
    if resource in self.resources:
        new_amount = self.resources[resource] + amount
        if new_amount < 0:
            print(f"错误操作")
            return False
        self.resources[resource] = new_amount
        return True
    else:
        print(f"错误原因：未知")
        return False
    

def get_resource(self, resource: str) -> int:
    """获取特定资源的当前数量,如果不存在就返回0"""
    return self.resources.get(resource,0)

def has_sufficient_resources(self,requirements: dict[str,int]) -> bool:
    """检查是否有足够的资源满足需求,任意一个资源不足都返回False"""
    for resource,amount in requirements.items():
        if self.get_resource(resource) < amount:
            return False
    return True

def consume_resources(self,costs:Dict[str,int]) -> bool:
    """消耗资源,返回是否成功"""
    for resource,amount in costs.items():
        if self.get_resource(resource) < amount:
            return False
    for resource,amount in costs.items():
        self.resources[resource] -= amount
    return True

def upgrade_module(self,module_name:str) -> bool:
    """升级模块,如果模块存在且有足够资源,返回是否成功"""
    if module_name not in self.modules:
       print("错误：未知模块{module_name}")
       return False
    
    # 获取模块对象
    module = self.modules[module_name]
    # 计算成本：模块等级乘模块基础成本
    upgrade_cost = module.level * module.base_cost()
    
    # 尝试消耗材料资源
    if self.consume_resources({"materials":upgrade_cost}):
        module.level +=1
        print(f"{module.name}升级成功！等级为{module.level}")
        return True
    else:
        print(f"{module.name}材料不足，升级失败~")
        return False
    
    # 获取指定模块的总效率（等级*基础效率）
    def get_module_efficiency(self,module_name:str)->int:
        # 获取模块对象
        module =self.modules.get(module_name)
        # 如果模块存在，则返回模块的等级*基础效率
        if module:
            return module.level* module.efficiency
        return 0
    
    # 获取可升级模块的详细信息列表
    def list_availiable_modules(self)-> List[Dict]:
        # 创建一个空列表，用于存储可升级模块的详细信息

        # 创建存储信息的列表
        available = []
        # 遍历所有模块
        for module_id, module in self.modules.items():
            # 如果模块可升级，则添加模块的详细信息到列表中
            available.append({
                # 模块id
                "id":module_id,
                # 模块名称
                "name":module.name,
                # 模块等级
                "level":module.level,
                # 模块效率
                "efficiency":module.efficiency,
                # 升级所需要的cost
                "upgrade_cost":module.level * module.base_cost
            })
            return avaliable
        
        def get_total_crew(self) -> int:
            """获取当前总船员数量"""
            return sum(self.crew.values())
        
        def modify_crew(self,role:str,change:int) -> bool:
            """修改船员数量"""
            if role in self.crew:
                new_count = self.crew[role] + change
                if new_count < 0:
                    print(f"船员数量太少")
                    return False
                self.crew[role] = new_count
                return True
            else:
                print(f"未知的船员角色：{role}")
                return False
            
        def caculate_crew_consumption(self) -> Dict[str,int]:
            """
            计算船员消耗(基础损失+船员数量带来的损失)
            """

            # 获取船员数量
            total_crew = self.get_total_crew()
            # 复制基础消耗字典
            consumption = self.config["base_consumption"].copy()

            # 对于每个资源类型，计算总的人员带来的损hao
            for resource,amount in consumption:
                consumption[resource] = amount + total_crew * self.config["crew_consumption"][resource]

            return consumption
        
        def validate_game_state(self) -> bool:
            """
            验证游戏所有数值是否正确
            """
            for resource,amount in self.resources.items():
                if amount < 0:
                    print(f"{resource}数量不能小于0")
                    return False
                
            for role,count in self.crew.items():
                    if count <0:
                        print(f"{role}数量不能小于0")
                        return False
            for module_name,module in self.modules.items():
                if count <0:
                    print(f'错误：模块{module_name}等级不能小于0')
                return False
            
            return True
        
        def __str__(self) -> str:
            """返回游戏状态的字符串表示"""
            return f"太空站游戏 -第{self.game_state['day']}天 -船员{self.get_total_crew()}人 -探索区域： {self.game_state['exxpored_sector']}个"
        
        # 测试代码块
        if __name__ == "__main__":
            # 创建游戏实例
            game = SpaceStationGame()

            #显示初始状态
            print(game)
            print("资源：",game.resources)
            print("船员：",game.crew)

            # 测试资源修改功能
            # 增加50个资源
            game.modify_resource("energy",50)
            # 打印能源
            print("增加能源后：",game.get_resource("energy"))

            # 测试模块列表
            # 获取模块列表
            modules = game.List_available_modules()
            # 打印
            print("可升级模块：",modules)

            # 验证游戏状态
            if game.validate_game_state():
                print("游戏状态验证成功")
            else:
                print("游戏状态验证失败")