import pygame
from src.tools import *
from src.animation import *

class object(pygame.sprite.Sprite):
    def __init__(self, image=None, state=""):
        pygame.sprite.Sprite.__init__(self)
        self.state = state
        if type(image)==str:
            self.image = load_imageOnly(image)
        elif type(image)==pygame.Surface:
            self.image = image
        else:
            self.image = None
        if self.image:
            self.rect = self.image.get_rect()
        else:
            self.rect = pygame.Rect(0, 0, 0, 0)
        self.show = False
        self.action = None
        self.direction = 1
        self.directionY = 1
        self.timecount = 0
        self.FlipX = False
        self.FlipY = False
    def setState(self, state):
        self.state = state
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def moveTo(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def isShow(self, enable):
        self.show = enable
    def fitRect2Image(self):
        rectcenter = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = rectcenter
    def getState(self):
        return self.state
    def showImage(self, dst):
        if self.show:
            dst.blit(self.image, self.rect.topleft)
    def beginUpdate(self):
        if self.action:
            if type(self.action[self.state])==pygame.Surface:
                self.image = self.action[self.state].copy()
                self.fitRect2Image()
            elif type(self.action[self.state])==animation:
                self.action[self.state].play()
                self.image = self.action[self.state].update().copy()
                self.fitRect2Image()
    def endUpdate(self, dst):
        if self.direction == -1:
            self.FlipX = True
        else:
            self.FlipX = False

        if self.directionY == -1:
            self.FlipY = True
        else:
            self.FlipY = False

        self.image = pygame.transform.flip(self.image, self.FlipX, self.FlipY)
        self.showImage(dst)

