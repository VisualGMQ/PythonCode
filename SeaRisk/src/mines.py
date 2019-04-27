from src.animation import *
from src.object import *
from src.GameBody import *
from src.tools import *
from src.UITools import *
from src.font import *

NON_RENEWABLE = 1
RENEWABLE = 2

class mine(object):
    def __init__(self, image, info, type):
        object.__init__(self, image, "normal")
        self.image = load_imageOnly(image, -1, True)
        self.fitRect2Image()
        self.MINDIST = 120
        self.type = type
        self.isDigged = False
        self.diggingTime = 50
        self.info = info
    def detectDiver(self, dst):
        diverLocalRect = GameBody.args['diverLocalRect']
        #if not GameBody.args['diver'].mine:
        #    GameBody.args['diver'].setMine(None)
        if getDistance(diverLocalRect.center, self.rect.center) <= self.MINDIST:
            if GameBody.args['diver'].state == 'swiming' and not self.isDigged:
                GameBody.args['diver'].setMine(self)
                drawText(dst, u"这里好像有矿!", 15, [diverLocalRect.x-20, diverLocalRect.y-20], fontInfo())
            elif self.type == RENEWABLE:
                drawText(dst, u"这里的矿已经被采集80%了，不能再采集了!", 15, [diverLocalRect.x - 20, diverLocalRect.y - 20], fontInfo(color=(255,0,0)))
        else:
            if GameBody.args['diver'].mine == self:
                GameBody.args['diver'].mine = None

    def drawDebug(self, dst):
        pygame.draw.circle(dst,(255,0,0,255), self.rect.center, self.MINDIST, 1)
    def update(self, dst):
        object.beginUpdate(self)

        if self.show:
            self.detectDiver(dst)

        object.endUpdate(self, dst)