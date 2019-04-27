import pygame
import os

FONT_NAME = 'SimHei.ttf'

class fontInfo:
    def __init__(self, color=(0, 0, 0), bgColor=None, isBold=False, isItalic=False, isUnderline=False):
        self.color = color
        self.bgColor = bgColor
        self.isBold = isBold
        self.isItalic = isItalic
        self.isUnderline = isUnderline

def createSentence(sentence, ptsize, info):
    font = pygame.font.Font(FONT_NAME, ptsize)
    if info:
        font.set_bold(info.isBold)
        font.set_italic(info.isItalic)
        font.set_underline(info.isUnderline)
    surface = font.render(sentence, True, info.color, info.bgColor)
    surface.set_colorkey(surface.get_at((0, 0)))
    return surface

def drawText(dst, sentence, ptsize, point, info):
    surface = createSentence(sentence, ptsize, info)
    dst.blit(surface, point)

