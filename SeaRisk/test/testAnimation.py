from src.animation import *
import src.GameBody
import pygame
from src.UITools import uiButton, defaultStateChange

normSurface = pygame.image.load("button.jpg")
pressedSurface = pygame.image.load("buttonDown.png")
moveonSurface = pygame.image.load("buttonMoveOn.png")

class myButton(uiButton):
    def __init__(self, animation):
        uiButton.__init__(self, "play Animation", normSurface, pressedSurface, moveonSurface)
        self.ani = animation
    def buttonDown(self):
        self.ani.play()
    def stateChange(self):
        defaultStateChange(self)

class testbody(src.GameBody.GameBody):
    def __init__(self):
        src.GameBody.GameBody.__init__(self, (400, 400), "test Animation", (255, 255, 255), 30)
        self.ani = animation([frame("../../test/1.png", 5),frame("../../test/2.png", 5), frame("../../test/3.png", 5), frame("../../test/4.png", 5)])
        self.button = myButton(self.ani)
        self.button.moveTo((0, 300))
    def update(self):
        self.button.update(self.screen)
        self.screen.blit(self.ani.update(), (0,0))

if __name__ == '__main__':
    pygame.init()
    body = testbody()
    while not body.isQuit:
        body.step()

    pygame.quit()