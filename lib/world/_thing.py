
class Thing:
    '''
    something that has coords on a map
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def coords(self):
        return self.x, self.y

    @coords.setter
    def coords(self, x, y):
        self.x = x
        self.y = y


