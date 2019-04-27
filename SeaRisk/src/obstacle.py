from src.object import *
from src.tools import *
from src.animation import *
from src.GameBody import *

class block(object):
    def __init__(self):
        object.__init__(self, '/UI/obstacle.png')
        self.state = 'static'
        self.oldrect = GameBody.args['diver'].rect
    def update(self, dst):
        object.beginUpdate(self)

        if GameBody.args['diver'].rect.colliderect(self.rect):
            GameBody.args['diver'].backToOldPos()

        object.endUpdate(self, dst)

class riptide(object):
    def __init__(self):
        object.__init__(self, "/UI/riptide.jpg")
    def update(self, dst):
        object.beginUpdate(self)
        if self.show:
            if self.rect.colliderect(GameBody.args['diverLocalRect']):
                GameBody.args['diver'].move(50, 50)
        object.endUpdate(self, dst)