import pygame
import src.myGame
import os
from src.functions import *

if __name__ == '__main__':
    pygame.init()
    game = src.myGame.myGame()
    while not game.isQuit:
        game.step()

    pygame.quit()