from GameSupport import *
# 导入支持库

class RuleMaze(RuleBase):  # 继承RuleBase基类
    def __init__(self, _map, player, game=None, allow_tp=False):
        super().__init__(_map, player, game)  # 向父类传参
        self.allow_tp = allow_tp
        # actions定义行为
        self.actions = {'tp':self.teleport, \
        'w': self.move,'a': self.move,'s': self.move,'d': self.move}
        
    def judge(self):
        """判断游戏是否结束"""
        if self.player.location == self.game.exit_point:
            return GameInfo.GameOver
        return GameInfo.GameRunning
    
    def teleport(self, location=None):
        """传送方法，也被用于移动"""
        
        # 判断传参是否为空
        # 若空则要求输入坐标并处理成Location
        if not isinstance(location, Location):
            loc_info = input('to\t')
            point = loc_info.find(',')
            location = Location(int(loc_info[:point]),int(loc_info[point + 1:]))
        # 判断传送位置是否合法
        # 如果不允许传送，则只能被传送到旁边(besides)，即移动一格
        if location in self.player.location.besides or self.allow_tp:
            # 目标位置即将被覆盖，下方变量作为临时存储
            target_pos_building = self._map[location]
            # 如果目标位置不是墙壁
            # 且目标位置存在（即未越界）
            if not isinstance(target_pos_building, Wall) and target_pos_building:
                # 返还玩家所占位置原有的实例（地板）
                self._map[self.player.location] = self.player.building_at
                # 更新临时存储实例
                self.player.building_at = target_pos_building
                # 更新玩家位置，并赋值于地图中
                self.player.location = location
                self.player.ut_loc()
                # 判断游戏状态
                return self.judge()
                
        return GameInfo.LocationError
   
    def move(self, action):
        """移动方法
        实现：得到移动后位置并调用tp方法
        """
        new_pos = self.get_position(action)
        return self.teleport(new_pos)    
    
    
if __name__=='__main__':
    # 游戏初始化
    coupler = GameInit(RuleMaze)
    # 设置地图
    coupler.setmap('5x5', 
    [
        {'location':[(range(5),range(5))],'content':Floor()},
        {'location':[((1,3), range(1,4)),(1,0),(3,4)],'content':Wall()}
    ],
        complete_trans=True)
    
    # 设置出生点和出口 并 初始化
    coupler._game.spawn_set(Location(0,0))
    coupler._game.exit_set(Location(4,4))
    coupler._game.init()
    # 循环运行
    coupler.mainloop()
    