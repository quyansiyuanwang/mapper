from Const import *
from MapLib import *


class Location(object):  # 位置信息类
    def __init__(self, col: int = None, row: int = None):
        self.col = 1 if col is None else col
        self.row = 1 if row is None else row
        
    def __ge__(self, other):
        return self.col >= other and self.row >= other

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

    def __getitem__(self, index):
        return self.col if index == 0 else self.row

    def __repr__(self):
        return f'Location({self.col},{self.row})'

    @property
    def besides(self):
        return Location(self.col + 1, self.row), Location(self.col - 1, self.row), Location(self.col, self.row - 1),	Location(self.col, self.row + 1)

    def read_loc(self):
        return self.col, self.row  # 行列
       

class Game:
    def __init__(self, _map, rule, player):
        self._map = _map
        self.rule = rule
        self.player = player
        
    def __str__(self):
        return self._map.__str__()
        
    def spawn_set(self, location):
        self._map[location] = SpawnPoint()
        self.spawn_point = location
        
    def exit_set(self, location):
        self._map[location] = ExitPoint()
        self.exit_point = location
    
    def start(self):
        self.player.location = self.spawn_point
        self.player.building_at = self._map[self.player.location]
    
    def end(self):
        print(self._map, 'end!')
        return GameInfo.GameOver
        
    def act(self):
        action = self.rule.analyse(input('your action:'))
        if action:
            run_result = action.runit()
            if run_result == GameInfo.GameRunning:
                return True
            elif run_result == GameInfo.GameOver:
                return self.end()
        return GameInfo.LocationError


class Player(Item):
    def __init__(self, _map):
        self.steps = 0
        self.location = None
        self._map = _map
        self.image = 'P'
        self.building_at =None
        
    def ut_loc(self):
        self._map[self.location] = self
        

class Init:
    def __init__(self, type_rule):
        self.type_rule = type_rule
        self._map = Map()
        self._player = Player(self._map)
        self._rule = type_rule(self._map, self._player)
        self._game = Game(self._map, self._rule, self._player)
        self._rule.game = self._game

    def setmap(self, *args, **kwargs):
        self._map = Map(*args, **kwargs)
        self._player = Player(self._map)
        self._rule = self.type_rule(self._map, self._player)
        self._game = Game(self._map, self._rule, self._player)
        self._rule.game = self._game
        