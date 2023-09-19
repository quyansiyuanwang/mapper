class Item:
    disc = 'NoDiscription'
    image = 'NoImage'
    
    def __str__(self):
        return f'{self.image}'

 
class Building(Item):
    pushable = False
    weight = None
    
    getable = False
    getlevel = None
    
    interoperable = False

    
    
                    
class Wall(Building):
    def __init__(self):
        self.repr = 'wall'
        self.image = '#'



class Floor(Building):
    def __init__(self):
        self.repr = 'floor'
        self.image = ' '
        

class ExitPoint(Building):
    def __init__(self):
        self.repr = 'exit'
        self.image = 'X'
     
     
class SpawnPoint(Building):
    def __init__(self):
        self.repr = 'spawn'
        self.image = 'S'
        
        
class GameInfo:
    GameOver = 'the game is over!'
    GameRunning = 'the game is running'
    LocationError = 'the position is wrong'
    UserTypeError = 'the content user inputed is unsolvable'
