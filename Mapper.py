#Mapper
def c_r_fetch(size_string):
    for index, letter in enumerate(size_string):
        if letter.lower() == 'x':
            try:
                row = int(size_string[:index])
                col = int(size_string[index + 1:])
            except Exception:
                raise ValueError('size string is not format!')
    return row, col
   
    
def turn_iterable(obj):
    try:
        for item in obj:
            yield item
    except Exception:
        yield obj                


class Location(object):  # 位置信息类
    def __init__(self, col: int = None, row: int = None):
        self.col = 1 if col is None else col
        self.row = 1 if row is None else row

    def __getitem__(self, index):
        return self.col if index == 0 else self.row

    def besides(self):
        return Location(self.col + 1, self.row), Location(self.col - 1, self.row), Location(self.col, self.row - 1),	Location(self.col, self.row + 1)

    def __repr__(self):
        return f'Location({self.col},{self.row})'

    def __ge__(self, other):
        return self.col >= other and self.row >= other

    def read_loc(self):
        return self.col, self.row  # 行列
       
    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

        
class Map:
    def __init__(self, size, map_content=None, T=False, complete_trans=False):
        self.row, self.col = c_r_fetch(size)
        self._map = [[None]*self.row for _ in range(self.col)]
        self.__map_content = map_content      
        self.T = T
        if self.__map_content is not None:
            self.complete_map(complete_trans)
        
        
    def complete_map(self, trans):
        def completer(x_com,y_com,content_info):
            self._map[x_com if trans else y_com][y_com if trans else x_com] = content_info
        
        for item in self.__map_content:
            for loc_iter in item['location']:
                index = 0
                content = tuple(turn_iterable(item['content']))
                x_group = tuple(turn_iterable(loc_iter[int(self.T) - 0]))
                y_group = tuple(turn_iterable(loc_iter[1 - int(self.T)]))
                if len(content) == 1:
                    content *= len(x_group)*len(y_group)
                for x in x_group:
                    for y in y_group:
                        completer(y,x,content[index])
                        index += 1
        return self._map  
    
    def __getitem__(self, dest):
        try:
            if dest >= 0:
                resp = self._map[dest[int(self.T) - 0]][dest[1 - int(self.T)]]
                return resp
            else:
                raise ValueError
        except Exception:
            return False
            
    def __setitem__(self, location, replace):
        self._map[location[1]][location[0]] = replace
    
    def get_range(self, location, trans=False):
        collecter = lambda x,y: self._map[x if trans else y][y if trans else x]
        for x in turn_iterable(location[0]):
            for y in turn_iterable(location[1]):
                yield collecter(x,y)
                    
    def __str__(self):
        rep = ''
        for line in self._map:
            rep += 'Ⅰ'
            for line_item in line:
                rep += line_item.__str__() + ' '
            rep += '\n'
        return rep
 
class Item:
    disc = 'NoDiscription'
    image = 'NoImage'
    
    def __str__(self):
        return f'{self.image}'

 
class Building(Item):
    pushable = False
    interoperable = False
    
                    
class Wall(Building):
    def __init__(self):
        self.repr = 'wall'
        self.image = '#'

class ExitPoint(Building):
    def __init__(self):
        self.repr = 'exit'
        self.image = 'X'
     
     
class SpawnPoint(Building):
    def __init__(self):
        self.repr = 'spawn'
        self.image = 'S'
        
        
class Floor(Building):
    def __init__(self):
        self.repr = 'floor'
        self.image = ' '
        

class GameInfo:
    GameOver = 'the game is over!'
    GameRunning = 'the game is running'
    LocationError = 'the position is wrong'
    

class FunctionBindArgument:
    def __init__(self, function: callable, *arguments):
        self.function = function
        self.arguments = arguments

    def release(self):
        return self.function, self.arguments

    def runit(self):
        return self.function(*self.arguments)

    def __repr__(self):
        return f'func:{self.function}\n'\
               f'args:{tuple(self.arguments)}'


class Game:
    def __init__(self, _map, rule, player):
        self._map = _map
        self.rule = rule
        self.player = player
        
    def spawn_set(self, location):
        self._map[location] = SpawnPoint()
        self.spawn_point = location
        
    def exit_set(self, location):
        self._map[location] = ExitPoint()
        self.exit_point = location
    
    def __str__(self):
        return self._map.__str__()

    def act(self):
        action = self.rule.analyse(input('your action:'))
        if action:
            run_result = action.runit()
            if run_result == GameInfo.GameRunning:
                return True
            elif run_result == GameInfo.GameOver:
                return self.end()
        return GameInfo.LocationError

    def start(self):
        self.player.location = self.spawn_point
        self.player.building_at = self._map[self.player.location]
    
    def end(self):
        print(self._map, 'end!')
        return GameInfo.GameOver
        

class Player(Item):
    def __init__(self, _map):
        self.steps = 0
        self.location = None
        self._map = _map
        self.image = 'P'
        self.building_at =None
        
    def ut_loc(self):
        self._map[self.location] = self
        
class RuleMaze:
    def __init__(self, _map, player, game=None):
        self.game = game
        self._map = _map
        self.player = player
        self.fac = {'tp':self.teleport, \
        'w': self.move_key,'a': self.move_key,'s': self.move_key,'d': self.move_key}
        
    def judge(self):
        if self.player.location == self.game.exit_point:
            return GameInfo.GameOver
        return GameInfo.GameRunning
    
    def teleport(self, location=None):
        if not isinstance(location, Location):
            loc_info = input('to\t')
            point = loc_info.find(',')
            location = Location(int(loc_info[:point]),int(loc_info[point + 1:]))
        
        if location in self.player.location.besides() or True:
            target_pos_building = self._map[location]
            if not isinstance(target_pos_building, Wall) and target_pos_building:
                
                self._map[self.player.location] = self.player.building_at
                self.player.building_at = target_pos_building
                
                self.player.location = location
                self.player.ut_loc()
                
                return self.judge()
                
        return GameInfo.LocationError
   
    def move_key(self, action):
        def move_left(self):
            return Location(self.player.location[0] - 1, self.player.location[1])
   
        def move_right(self):
            return Location(self.player.location[0] + 1, self.player.location[1])
    
        def move_up(self):
            return Location(self.player.location[0], self.player.location[1] - 1)
        
        def move_down(self):
            return Location(self.player.location[0], self.player.location[1] + 1)
        
        fac = {'a':move_left,'d':move_right,'w':move_up,'s':move_down}
        for key_fac, refl in fac.items():
            if action == key_fac:
                return self.teleport(refl(self))            
                
    def analyse(self, action):
        for action_type, refl in self.fac.items():
            if action == action_type:
                return FunctionBindArgument(refl, action)

    
if __name__=='__main__':   
    m = Map('5x5', 	[{'location':[(range(5),range(5))],'content':Floor()},\
    {'location':[((1,3), range(1,4)),(1,0),(3,4)],'content':Wall()}],\
    complete_trans=True)
    m.T = True

    print('-'*15)
    p = Player(m)
    ru = RuleMaze(m,p)
    game = Game(m, ru, p)
    ru.game = game
    game.spawn_set(Location(0,0))
    game.exit_set(Location(4,4))
    game.start()
    
    res = True
    while res != GameInfo.GameOver:
        print(m)
        res = game.act()
        
        
    