from GameSupport import *


class RuleMaze(RuleBase):
    def __init__(self, _map, player, game=None, allow_tp=False):
        super().__init__(_map, player, game)
        self.allow_tp = allow_tp
        self.actions = {'tp':self.teleport, \
        'w': self.move,'a': self.move,'s': self.move,'d': self.move}
        
    def judge(self):
        if self.player.location == self.game.exit_point:
            return GameInfo.GameOver
        return GameInfo.GameRunning
    
    def teleport(self, location=None):
        if not isinstance(location, Location):
            loc_info = input('to\t')
            point = loc_info.find(',')
            location = Location(int(loc_info[:point]),int(loc_info[point + 1:]))
        
        if location in self.player.location.besides or self.allow_tp:
            target_pos_building = self._map[location]
            if not isinstance(target_pos_building, Wall) and target_pos_building:
                
                self._map[self.player.location] = self.player.building_at
                self.player.building_at = target_pos_building
                
                self.player.location = location
                self.player.ut_loc()
                
                return self.judge()
                
        return GameInfo.LocationError
   
    def move(self, action):
        new_pos = self.get_position(action)
        return self.teleport(new_pos)    
    
    
if __name__=='__main__':
    coupler = Init(RuleMaze)
    coupler.setmap('5x5', 
    [
        {'location':[(range(5),range(5))],'content':Floor()},
        {'location':[((1,3), range(1,4)),(1,0),(3,4)],'content':Wall()}
    ],
        complete_trans=True)
        
    coupler._map.T = True
    coupler._game.spawn_set(Location(0,0))
    coupler._game.exit_set(Location(4,4))
    coupler._game.start()
    
    coupler.mainloop()
    