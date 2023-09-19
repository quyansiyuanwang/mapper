from GameSupport import *


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
        
        if location in self.player.location.besides or True:
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
        action = action.lower()
        for action_type, refl in self.fac.items():
            if action == action_type:
                return FunctionBindArgument(refl, action)

    
if __name__=='__main__':
    coupler = Init(RuleMaze)
    coupler.setmap('5x5', 
    [
        {'location':[(range(5),range(5))],'content':Floor()},
        {'location':[((1,3), range(1,4)),(1,0),(3,4)],'content':Wall()}
    ],
        T = True,
        complete_trans=True)
    
    coupler._game.spawn_set(Location(0,0))
    coupler._game.exit_set(Location(4,4))
    coupler._game.start()
    
    res = True
    while res != GameInfo.GameOver:
        print(m)
        res = coupler._game.act()
        