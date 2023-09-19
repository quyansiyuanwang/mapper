class Item:
    disc = 'NoDiscription'  # 描述
    image = 'NoImage'  # 符号标识
    
    def __str__(self):
        """用于显示符号标识于地图或控制台"""
        return f'{self.image}'

 
class Building(Item):
    pushable = False  # 可推动的
    weight = None  # 重量
    
    getable = False  # 可得到的
    getlevel = None  # 可得到所需的等级
    
    interoperable = False  # 可交互的
    
                    
class Wall(Building):
    """墙壁"""
    def __init__(self):
        self.repr = 'wall'
        self.image = '#'



class Floor(Building):
    """地板"""
    def __init__(self):
        self.repr = 'floor'
        self.image = ' '
        

class ExitPoint(Building):
    """出口"""
    def __init__(self):
        self.repr = 'exit'
        self.image = 'X'
     
     
class SpawnPoint(Building):
    """出生点"""
    def __init__(self):
        self.repr = 'spawn'
        self.image = 'S'
        
        
class GameInfo:
    """存储各类游戏阶段状态(state)"""
    GameOver = 'the game is over!'
    GameRunning = 'the game is running'
    LocationError = 'the position is wrong'
    UserTypeError = 'the content user inputed is unsolvable'
    RunTimeError = 'the error raised while game running'
