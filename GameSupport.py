from Const import *
from MapLib import *


class Location(object):  # 位置信息类
    def __init__(self, col: int = None, row: int = None):
        self.col = 1 if col is None else col
        self.row = 1 if row is None else row
        
    def __ge__(self, other):
        """大于等于"""
        return self.col >= other and self.row >= other

    def __eq__(self, other):
        """等于"""
        return self.col == other.col and self.row == other.row

    def __add__(self, other: iter):
        """加法运算"""
        return Location(self.col + other[0], self.row + other[1])

    def __getitem__(self, index):
        """获取xy的getitem方法，参考可迭代对象例如元组"""
        return self.col if index == 0 else self.row

    def __repr__(self):
        """解释内容，打印方法"""
        return f'Location({self.col},{self.row})'

    @property
    def besides(self):
        """目标位置周围四格的Location对象"""
        return Location(self.col + 1, self.row), Location(self.col - 1, self.row), Location(self.col, self.row - 1),	Location(self.col, self.row + 1)
        

class Game:
    def __init__(self, _map, rule, player):
        self._map = _map
        self.rule = rule
        self.player = player
        
    def __str__(self):
        """
        简略实现打印方法
        TO OPTIMIZE: 需要返回更多数据
        """
        return self._map.__str__()
        
    def spawn_set(self, location):
        """设置出生点"""
        self._map[location] = SpawnPoint()
        self.spawn_point = location
        
    def exit_set(self, location):
        """设置出口"""
        self._map[location] = ExitPoint()
        self.exit_point = location
    
    def init(self):
        """初始化
        将玩家定位于入口（出生点）
        记录被覆盖的内容
        """
        self.player.location = self.spawn_point
        self.player.building_at = self._map[self.player.location]
        self.player.ut_loc()
    
    def end(self):
        """游戏结束"""
        print(self._map, 'end!')
        return GameInfo.GameOver
        
    def act(self):
        """行动
        将玩家输入内容放入规则类(RuleType)进行行为解析
        返回对应函数并运行得到结果
        对结果进行判断
        """
        action = self.rule.analyse(input('your action:'))
        if action:
            run_result = action.runit()
            if run_result == GameInfo.GameRunning:
                return True
            elif run_result == GameInfo.GameOver:
                return self.end()
        return GameInfo.LocationError


class RuleBase:
    """规则基类
    tips：他最好被继承
    不仅仅是为了省时间"""
    def __init__(self, _map, player, game=None):
        self.game = game
        self._map = _map
        self.player = player
        self.actions = {}
        
    def get_position(self, action):
        """得到移动后的新位置坐标"""
        move_keys = {
            'w':(0, -1),
            'a':(-1, 0),
            's':(0, 1),
            'd':(1, 0)
        }
        refl = move_keys.get(action, None)
        if refl is not None:
            return self.player.location + refl
            
    def analyse(self, action):
        """分析行为，返回对应的函数参数集FuncBindArgs"""
        action = action.lower()
        refl = self.actions.get(action, None)
        if refl is not None:
            return FunctionBindArgument(refl, action)
        

class Player(Item):
    """玩家"""
    def __init__(self, _map):
        self.steps = 0  # 步数
        self.location = None  # 位置
        self._map = _map  # 数据通信用
        self.image = 'P'  # 玩家符号标识
        self.building_at = None  # 被替换的地图内容
        
    def ut_loc(self):
        """用玩家于地图中覆盖"""
        self._map[self.location] = self
        

class GameInit:
    """游戏初始化"""
    def __init__(self, type_rule):
        self.type_rule = type_rule  # 规则类
        self._map = None
        self.reset_RuleGame()

    def reset_RuleGame(self):
        """数据更新，重置关联"""
        self._player = Player(self._map)  
        self._rule = self.type_rule(self._map, self._player)
        self._game = Game(self._map, self._rule, self._player)
        self._rule.game = self._game
    
    def setmap(self, *args, **kwargs):
        """创设地图"""
        self._map = Map(*args, **kwargs)
        self.reset_RuleGame()
        self._map.T = True
        
    def mainloop(self, show_map: bool = True, ignore_error: bool = True, *others):
        """游戏进行主循环"""
        # 自定义参数解耦
        loop = [FuncBindArg for FuncBindArg in others]
        # 玩家操作函数参数集入栈
        loop = [FunctionBindArgument(self._game.act)] + loop
        if show_map:  # 在开头添加print的函数参数集
            loop = [FunctionBindArgument(print, self._map)] + loop
        
        while True:
            for operation in loop:
                run_result = operation.runit()
                # 游戏运行报错
                if run_result == GameInfo.RunTimeError and not ignore_error:
                    raise RuntimeError
                # 玩家键入数据错误或无法处理
                elif run_result == GameInfo.UserTypeError and not ignore_error:
                    raise SyntaxError
                # 游戏结束
                elif run_result == GameInfo.GameOver:
                    return run_result
                    