import pygame
from src.font import *
from src.object import *
from src.GameBody import *
import src.constants

class uiButton(pygame.sprite.Sprite):
    BUTTON_NORMAL  = 0
    BUTTON_DOWN    = 1
    BUTTON_UP      = 2
    BUTTON_SUSPEND = 3
    def initDefault(self):
        surface = pygame.Surface((150, 50)).convert()
        surface.fill((255, 255, 255))
        normSurface = surface.copy()
        pressedSurface = surface.copy()
        moveonSurface = surface.copy()
        drawText(normSurface, "default", 20, (10, 0), fontInfo())
        drawText(pressedSurface, "button pressed", 20, (10, 0), fontInfo())
        drawText(moveonSurface, "button moveon", 20, (10, 0), fontInfo())
        pygame.draw.rect(normSurface, (0, 0, 0), pygame.Rect(0 ,0 ,150, 50), 2)
        pygame.draw.rect(pressedSurface, (0, 0, 0), pygame.Rect(0, 0, 150, 50), 2)
        pygame.draw.rect(moveonSurface, (0, 0, 0), pygame.Rect(0, 0, 150, 50), 2)
        self.init("default", normSurface, pressedSurface, moveonSurface)

    def initPics(self, caption, normSurface, pressedSurface, moveonSurface):
        fontSurface = createSentence(caption, 20, fontInfo())
        normSurface.blit(fontSurface, (10, 10))
        pressedSurface.blit(fontSurface, (10, 10))
        moveonSurface.blit(fontSurface, (10, 10))
        self.init(caption, normSurface, pressedSurface, moveonSurface)
    def __init__(self, caption = None, normSurface = None, pressedSurface = None, moveonSurface = None):
        pygame.sprite.Sprite.__init__(self)
        if caption==None or normSurface==None or pressedSurface==None or moveonSurface==None:
            self.initDefault()
        else:
            self.initPics(caption, normSurface, pressedSurface, moveonSurface)

    def init(self, caption, normSurface, pressedSurface, moveonSurface):
        self.normSurface = normSurface
        self.pressedSurface = pressedSurface
        self.moveonSurface = moveonSurface
        self.state = uiButton.BUTTON_NORMAL
        self.image = normSurface
        self.rect = normSurface.get_rect()
        self.caption = caption
    def moveTo(self,point):
        self.rect.topleft = point

    #will be override
    def buttonDown(self):
        pass
    def buttonUp(self):
        pass
    def buttonSuspend(self):
        pass
    #how to change state,will be override
    def stateChange(self):
        pass

    def setStatus(self):
        return self.state
    def getStatus(self):
        return self.state
    def update(self, dst):
        self.stateChange()
        if self.state == uiButton.BUTTON_NORMAL:
            self.image = self.normSurface
        if self.state == uiButton.BUTTON_DOWN:
            self.image = self.pressedSurface
            self.buttonDown()
        if self.state == uiButton.BUTTON_SUSPEND:
            self.image = self.moveonSurface
            self.buttonSuspend()
        if self.state == uiButton.BUTTON_UP:
            self.image = self.normSurface
            self.buttonUp()
        dst.blit(self.image, self.rect.topleft)

def defaultStateChange(button):
    if button.rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            button.state = uiButton.BUTTON_DOWN
        else:
            button.state = uiButton.BUTTON_SUSPEND
    else:
        button.state = uiButton.BUTTON_NORMAL

class Hp(object):
    def __init__(self):
        object.__init__(self, load_imageOnly("/UI/life.png", colorkey=-1, isAlpha=True))
        self.num = 10
    def update(self, dst):
        if self.show:
            for i in range(self.num):
                dst.blit(self.image, (self.rect.x + i*(self.rect.w+10),self.rect.y))

class airNum(object):
    def __init__(self):
        object.__init__(self, load_imageOnly('/UI/bubble.png', colorkey=-1, isAlpha=True))
        self.num = 10
    def update(self, dst):
        if self.show:
            for i in range(self.num):
                dst.blit(self.image, (self.rect.x + i*(self.rect.w+10),self.rect.y))

class mineBar(object):
    def __init__(self, maxnum):
        object.__init__(self, load_imageOnly('/UI/minimine.png', colorkey=-1, isAlpha=True))
        self.nomine = load_imageOnly('/UI/minimineOutline.png', colorkey=-1, isAlpha=True)
        self.maxnum = maxnum
        self.num = 0
    def update(self, dst):
        if self.show:
            for i in range(0,self.num):
                dst.blit(self.image, (self.rect.x + i * (self.rect.w + 10), self.rect.y))
            for i in range(self.num, self.maxnum):
                dst.blit(self.nomine, (self.rect.x + i * (self.nomine.get_rect().w + 10), self.rect.y))

class HandBook(object):
    class exitButton(object):
        def __init__(self, parent):
            object.__init__(self, "/UI/exitButton.jpg", -1)
            self.moveTo(975, 0)
            self.parent = parent

        def update(self, dst):
            # print(GameBody.mousePos)
            rect = self.rect.copy()
            rect.x += 100
            rect.y += 100
            #print(rect)
            #print("mousePos", GameBody.mousePos)
            if self.parent.isOpen:
                if rect.collidepoint(GameBody.mousePos) and GameBody.mouseButton[0]:
                    print("is collied")
                    self.parent.close()
                # if GameBody.keyState[K_m]:
                #    self.parent.close()
                dst.blit(self.image, self.rect)
    class MineInfo(object):
        def __init__(self, parent, image, info):
            object.__init__(self, image)
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.fitRect2Image()
            self.parent = parent
            self.info = info
        def update(self, dst, rect):
            dst.blit(self.image, rect)


    def __init__(self):
        object.__init__(self, load_imageOnly("/UI/handbook.png", isAlpha=True, colorkey=-1), (255, 0, 0))
        self.plane = load_imageOnly('/UI/bookContext.png', colorkey=-1)
        self.moveTo(10, 10)
        self.exitbutton = load_imageOnly('/UI/exitButton.jpg', colorkey=-1)
        self.isOpen = False
        self.planeRect = pygame.Rect(((src.constants.SCREEN_SIZE[0] - self.plane.get_width())//2, (src.constants.SCREEN_SIZE[1]-self.plane.get_height())//2), self.plane.get_size())
        self.mines = []
    def addMine(self, image, info):
        mineinfo = self.MineInfo(self, image, info)
        self.mines.append(mineinfo)
    def open(self):
        self.isOpen = True
    def close(self):
        self.isOpen = False
    def drawMines(self, dst):
        mineWidth = 94
        mineHeight = 94
        surface = self.plane.copy()
        rect = pygame.Rect(0, 0, mineWidth, mineHeight)
        for i in range(len(self.mines)):
            rect.center = (100 + mineWidth*(i%3), 100 + mineHeight*(i//3))
            self.mines[i].update(surface, (rect.x, rect.y))
            rect.x -= 25
            rect.y -= 15
            rect.x += self.planeRect.x
            rect.y += self.planeRect.y
            if rect.collidepoint(GameBody.mousePos):
                drawText(surface, self.mines[i].info, 20, (mineWidth*3 + 50, 150), fontInfo(color=(255, 255, 255, 255)))
            #pygame.draw.rect(dst, (0, 0, 255), rect, 1)
        surface.blit(self.exitbutton, (self.planeRect.w - self.exitbutton.get_width(), 0))
        dst.blit(surface, self.planeRect.topleft)
    def update(self, dst):
        #print(self.isOpen)
        if self.rect.collidepoint(GameBody.mousePos) and GameBody.mouseButton[0]:
            self.isOpen = True
        if pygame.Rect(((src.constants.SCREEN_SIZE[0]-self.plane.get_width())//2 + self.plane.get_width()-self.exitbutton.get_width(), (src.constants.SCREEN_SIZE[1]-self.plane.get_height())//2), self.exitbutton.get_size()).collidepoint(GameBody.mousePos) and GameBody.mouseButton[
            0]:
            self.isOpen = False

        #print("mouseButton:",GameBody.mouseButton[0])
        #print(self.isOpen)
        if self.show:
            if self.isOpen:
                #dst.blit(self.plane, (self.planeRect.topleft)
                #self.exitbutton.update(self.plane)
                #dst.blit(self.exitbutton, ((src.constants.SCREEN_SIZE[0]-self.plane.get_width())//2 + self.plane.get_width()-self.exitbutton.get_width(), (src.constants.SCREEN_SIZE[1]-self.plane.get_height())//2))
                self.drawMines(dst)
            else:
                dst.blit(self.image, self.rect)

class sceneBackAni(object):
    def __init__(self, image, ani):
        object.__init__(self, None)
        self.image = load_imageOnly(image, -1)
        self.fitRect2Image()
        self.rect.topleft = (0, 0)
        self.action = {'normal': ani}
        self.setState('normal')
    def update(self, dst):
        object.beginUpdate(self)

        object.endUpdate(self, dst)

class normalBGScene(sceneBackAni):
    def __init__(self):
        sceneBackAni.__init__(self, '/scene/12.png', animation(
            [frame('/scene/12.png', colorKey=-1), frame('/scene/22.png', colorKey=-1), frame('/scene/32.png', colorKey=-1), frame('/scene/42.png', colorKey=-1),
             frame('/scene/52.png', colorKey=-1),
             frame('/scene/62.png', colorKey=-1), frame('/scene/72.png', colorKey=-1), frame('/scene/82.png', colorKey=-1), frame('/scene/92.png', colorKey=-1),
             frame('/scene/102.png', colorKey=-1)]))
    def update(self, dst):
        sceneBackAni.update(self, dst)

class welcomeBGScene(sceneBackAni):
    def __init__(self):
        sceneBackAni.__init__(self, '/scene/11.png', animation(
            [frame('/scene/11.png', colorKey=-1), frame('/scene/21.png', colorKey=-1), frame('/scene/31.png', colorKey=-1), frame('/scene/41.png', colorKey=-1),
             frame('/scene/51.png', colorKey=-1),
             frame('/scene/61.png', colorKey=-1), frame('/scene/71.png', colorKey=-1), frame('/scene/81.png', colorKey=-1), frame('/scene/91.png', colorKey=-1),
             frame('/scene/101.png', colorKey=-1)]))
    def update(self, dst):
        sceneBackAni.update(self, dst)

class light(object):
    def __init__(self, item):
        object.__init__(self, '/UI/light/1.png')
        self.action = {'normal': animation([frame('/UI/light/1.png'), frame('/UI/light/2.png'), frame('/UI/light/3.png'),
                                            frame('/UI/light/4.png'), frame('/UI/light/5.png')])}
        self.action['normal'].setLoop(True)
        self.setState('normal')
        self.item = item
    def update(self, dst):
        if self.item.show:
            self.isShow(True)
        else:
            self.isShow(False)
        object.beginUpdate(self)
        object.endUpdate(self, dst)