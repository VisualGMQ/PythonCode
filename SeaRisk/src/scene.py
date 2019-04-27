import pygame
import src.constants
import math

class Scene(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.canva = pygame.Surface(size).convert()
        self.canva.fill(src.constants.BG_COLOR)
        self.rect = pygame.Rect((0, 0), size)
        self.timecount = 0

    def playBGM(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(-1)
    def moveTo(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def g2l(self, point):
        return (point[0] - self.rect.x,point[1] -  self.rect.y )
    def l2g(self, point):
        return (point[0] + self.rect.x, point[1] + self.rect.y)
    def g2lX(self, x):
        return x - self.rect.x
    def g2lY(self, y):
        return y - self.rect.y
    def l2gX(self, x):
        return x + self.rect.x
    def l2gY(self, y):
        return y + self.rect.y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def update(self, dst):
        pass