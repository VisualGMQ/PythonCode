import pygame
import src.constants

def handleEvent():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            src.constants.isQuit = True

def quitGame():
    src.constants.isQuit = True