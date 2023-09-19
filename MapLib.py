from Tools import *

class Map:
    """地图"""
    def __init__(self, size=None, map_content=None, T=False, complete_trans=False):
        self.size = size  # 地图大小
        self.map_content = map_content
        self.T = T
        self.complete_trans = complete_trans
        if size is not None:
            self.init()
    
    def init(self):
        """地图数据初始化"""
        # 创建二维结构
        self.row, self.col = c_r_fetch(self.size)
        self._map = [[None]*self.row for _ in range(self.col)]
        # 填充地图
        if self.map_content is not None:
            self.complete_map(self.complete_trans)
    
    def __getitem__(self, dest):
        """获取对应坐标的地图内容"""
        try:
            if dest >= 0:
                return self._map[dest[int(self.T) - 0]][dest[1 - int(self.T)]]
            else:  # 越界
                raise ValueError
        except Exception:  # 捕获越界错误并返回False
            return False
            
    def __setitem__(self, location, replace):
        """按坐标设置地图内容"""
        self._map[location[1]][location[0]] = replace
    
    def __str__(self):
        """地图显示方法，打印地图"""
        rep = ''
        for line in self._map:
            rep += 'Ⅰ'
            for line_item in line:
                rep += line_item.__str__() + ' '
            rep += '\n'
        return rep
    
    def complete_map(self, trans):
        """按照结构填充地图内容"""
        # 填充器
        def completer(x_com,y_com,content_info):
            self._map[x_com if trans else y_com][y_com if trans else x_com] = content_info
        
        # 进行填充每一设定项
        for item in self.map_content:
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
    
    def get_range(self, location, trans=False):
        """得到范围多矩形结构的内容耦合器"""
        collecter = lambda x,y: self._map[x if trans else y][y if trans else x]
        for x in turn_iterable(location[0]):
            for y in turn_iterable(location[1]):
                yield collecter(x, y)
