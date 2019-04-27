import pygame
from pygame.locals import *
import sys
import math
import os

def getDistance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def load_bgm(name):
    pygame.mixer.music.load('../resource/audio/' + name)

def playMineSound():
    sound = pygame.mixer.Sound('../resource/audio/mine.wav')
    sound.play()

def load_imageOnly(name, colorkey=None, isAlpha = False):
    fullname = os.path.join('../resource/pic/')
    try:
        image = pygame.image.load(fullname + name)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    if isAlpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    if colorkey is None:
        colorkey = image.get_at((0, 0))
    if not colorkey==-1:
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def load_image(name, colorkey=None):
    surface = load_imageOnly(name, colorkey)
    return surface, surface.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('../src/resource/pic')
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print('Cannot load sound:', name)
        raise SystemExit
    return sound