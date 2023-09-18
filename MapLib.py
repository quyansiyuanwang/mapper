from Tools import *

class Map:
    def __init__(self, size=None, map_content=None, T=False, complete_trans=False):
        self.size = size
        self.map_content = map_content
        self.T = T
        self.complete_trans = complete_trans
        if size is not None:
            self.init()
    
    def init(self):
        self.row, self.col = c_r_fetch(self.size)
        self._map = [[None]*self.row for _ in range(self.col)]
        if self.map_content is not None:
            self.complete_map(complete_trans)
    
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
    
    def __str__(self):
        rep = ''
        for line in self._map:
            rep += 'Ⅰ'
            for line_item in line:
                rep += line_item.__str__() + ' '
            rep += '\n'
        return rep
    
    def complete_map(self, trans):
        def completer(x_com,y_com,content_info):
            self._map[x_com if trans else y_com][y_com if trans else x_com] = content_info
        
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
        collecter = lambda x,y: self._map[x if trans else y][y if trans else x]
        for x in turn_iterable(location[0]):
            for y in turn_iterable(location[1]):
                yield collecter(x,y)
