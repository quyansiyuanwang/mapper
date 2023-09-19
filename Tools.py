def c_r_fetch(size_string):
    """
    得到行列
    用于map的初始化
    """
    for index, letter in enumerate(size_string):
        if letter.lower() == 'x':
            try:
                row = int(size_string[:index])
                col = int(size_string[index + 1:])
            except Exception:
                raise ValueError('size string is not format!')
    return row, col
   
    
def turn_iterable(obj):
    """将其转换成为可迭代对象"""
    try:
        for item in obj:
            yield item
    except Exception:
        yield obj
        
        
class FunctionBindArgument:
    """用于将函数与参数绑定，方便存储与调用"""
    def __init__(self, function: callable, *arguments):
        self.function = function
        self.arguments = arguments

    def __call__(self):
        return self.runit()

    def release(self):
        """释放函数与参数"""
        return self.function, self.arguments

    def runit(self):
        """直接运行（带参数）"""
        return self.function(*self.arguments)

    def __repr__(self):
        """调试显示方法"""
        return f'func:{self.function}\n'\
               f'args:{tuple(self.arguments)}'

