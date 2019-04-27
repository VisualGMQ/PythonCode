from src.GameBody import *
from src.object import *

class garbage(object):
    def __init__(self, image):
        object.__init__(self, image)
    def update(self, dst):
        object.beginUpdate(self)
        if self.show:
            if self.rect.colliderect(GameBody.args['diverLocalRect']):
                self.isShow(False)
                GameBody.args['diver'].air.num += 1

        object.endUpdate(self, dst)