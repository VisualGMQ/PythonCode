import src.UITools
import src.GameBody
import pygame

class myButton(src.UITools.uiButton):
    def __init__(self):
        src.UITools.uiButton.__init__(self)
    def stateChange(self):
        src.UITools.defaultStateChange(self)

class picButton(src.UITools.uiButton):
    def __init__(self, normSurface, downSurface, moveonSurface):
        src.UITools.uiButton.__init__(self, "button", normSurface, downSurface, moveonSurface)
    def stateChange(self):
        src.UITools.defaultStateChange(self)

class testUI(src.GameBody.GameBody):
    def __init__(self):
        src.GameBody.GameBody.__init__(self, (400, 400), "test UIs", (255,255,255), 30)
        self.button = myButton()
        normSurface = pygame.image.load('button.jpg').convert()
        downSurface = pygame.image.load('buttonDown.png').convert()
        moveonSurface = pygame.image.load('buttonMoveOn.png').convert()
        self.picbutton = picButton(normSurface, downSurface, moveonSurface)
        '''
        button1 = myButton()
        button2 = myButton()
        button3 = myButton()
        button1.moveTo((0,0))
        button2.moveTo((0,100))
        button3.moveTo(((0,200)))
        surface = pygame.Surface((300, 400))
        surface.convert()
        surface.fill((0,255,255))
        self.plane = src.UITools.plane((100,10), (0,0), (button1,button2,button3), surface)
        '''
    def update(self):
        self.button.update(self.screen)
        self.picbutton.moveTo((0,200))
        self.picbutton.update(self.screen)
        #self.plane.update(self.screen)

if __name__ == '__main__':
    pygame.init()
    testbody = testUI()

    while not testbody.isQuit:
        testbody.step()

    pygame.quit()