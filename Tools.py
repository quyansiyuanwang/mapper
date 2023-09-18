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

