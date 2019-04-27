import src.GameBody
from src.font import *
import pygame
from src.tools import *
from src.animation import *
from src.role import *
import src.constants
from src.object import *
from src.UITools import *
from src.myScene import *

class myGame(src.GameBody.GameBody):
    def __init__(self):
        src.GameBody.GameBody.__init__(self, src.constants.SCREEN_SIZE, src.constants.TITLE, src.constants.BG_COLOR, src.constants.DELAY_TIME)
        GameBody.args['diver'] = diver((0, 0), 'stand')
        GameBody.args['handbook'] = HandBook()
        GameBody.args['handbook'].isShow(True)
        self.gameOverScene = gameOver()
        self.darkScene = darkScene()
        self.secondScene = secondScene()
        self.gameScene = gameScene()
        self.welcomeScene = WelcomeScene()
        self.gameScene.moveTo(0, src.constants.SCREEN_SIZE[1])
        self.timecount = 0
        self.textcount = 0
        self.worldTime = 0
        self.airDecreaseTime = 100
        self.isfullScreen = False
        self.currentScene = 2
        GameBody.args['diver'].isShow(False)
        GameBody.args['diver'].hp.isShow(False)
        GameBody.args['diver'].air.isShow(False)
        GameBody.args['diver'].mineBar.isShow(False)
        GameBody.args['handbook'].isShow(False)
    def slideScene(self):
        if not GameBody.scene == -1:
            GameBody.scene = -1
        self.timecount += 1
        self.welcomeScene.diver.setState('jumpToSea')
        CONVERT_TICK = 50
        if self.timecount < CONVERT_TICK:
            self.welcomeScene.move(0, -src.constants.SCREEN_SIZE[1]//CONVERT_TICK)
            self.gameScene.moveTo(0, self.welcomeScene.rect.y+self.welcomeScene.rect.h)
            self.gameScene.update(self.screen)
            self.welcomeScene.update(self.screen)
        else:
            GameBody.scene = 1
            GameBody.nextScene()
            self.timecount = 0
            GameBody.isChangeScene = False
            self.gameScene.moveTo(0, 0)
            GameBody.args['diver'].air.isShow(True)
            GameBody.args['diver'].hp.isShow(True)
            GameBody.args['diver'].mineBar.isShow(True)
    def gotoScene(self, scenenum, scene):
        GameBody.scene = -1
        self.timecount += 1
        drawText(self.screen, u"宝藏收集完成！", 50, (300, 300), fontInfo())
        if self.timecount >= 10:
            self.timecount = 0
            GameBody.scene = scenenum
            self.currentScene = GameBody.scene
            GameBody.args['diver'].mineBar.num = 0
            GameBody.args['diver'].air.num = 10
            scene.onInit()

    def gotoGameOver(self, dst):
        self.gameOverScene.update(dst)
        GameBody.scene = 0

    def restartGame(self):
        GameBody.args['handbook'].mines = []
        GameBody.scene = 1
        self.currentScene = 2
        GameBody.args['diver'].onInit()
        self.darkScene.onInit()
        self.gameScene.onInit()
        self.welcomeScene.onInit()

    def decreaseAir(self):
        self.worldTime += 1
        if GameBody.keys[K_k]:
            self.airDecreaseTime = 50
        else:
            self.airDecreaseTime = 100
        if self.worldTime >= self.airDecreaseTime:
            self.worldTime = 0
            if GameBody.args['diver'].air.num > 0:
                GameBody.args['diver'].air.num -= 1
            else:
                GameBody.args['diver'].hp.num -= 1
    def fullScreen(self):
        self.screen = pygame.display.set_mode(src.constants.SCREEN_SIZE, pygame.FULLSCREEN, 32)
        self.isfullScreen = True
    def exitFullScreen(self):
        self.screen = pygame.display.set_mode(src.constants.SCREEN_SIZE, 0, 32)
        self.isfullScreen = False

    def beginScene(self, dst):
        dst.fill((0,0,0))
        self.textcount += 1
        surface = load_imageOnly('/UI/sayFrame.png', isAlpha=True, colorkey=-1)
        str1 = u"首领：南海包括中沙，西沙，南沙，北沙四个群岛，是我国的固有领土，         "
        str2 = u"为了合理开发和保护南海的海洋资源，我国准备让你下潜深海          "
        str3 = u"我们给你最先进的装备，确保你的安全          "
        str4 = u"小桂：谢谢首领，保证完成任务                 "
        if self.textcount < len(str1):
            drawText(surface, str1[:self.textcount], 25, (100, 100), fontInfo(color=(0,0,0,255)))
        elif self.textcount < len(str1) + len(str2):
            drawText(surface, str2[:self.textcount - len(str1)], 25, (100, 100), fontInfo(color=(0, 0, 0, 255)))
        elif self.textcount < len(str1) + len(str2) + len(str3):
            drawText(surface, str3[:self.textcount - len(str1) - len(str2)], 25, (100, 100), fontInfo(color=(0, 0, 0, 255)))
        elif self.textcount < len(str1) + len(str2) + len(str3) + len(str4):
            drawText(surface, str4[:self.textcount - len(str1) - len(str2) - len(str3)], 25, (100, 100), fontInfo(color=(0, 0, 0, 255)))
        self.textcount += 1
        if self.textcount > len(str1) + len(str2) + len(str3) + len(str4):
            GameBody.scene = 1
            self.currentScene = 2
            diver = GameBody.args['diver']
            diver.isShow(True)
            diver.hp.isShow(True)
            diver.air.isShow(True)
            diver.mineBar.isShow(True)
            GameBody.args['handbook'].isShow(True)
            self.textcount = 0
        dst.blit(surface, (0, 200))

    def endScene(self, dst):
        diver = GameBody.args['diver']
        diver.isShow(False)
        diver.hp.isShow(False)
        diver.air.isShow(False)
        diver.mineBar.isShow(False)
        GameBody.args['handbook'].isShow(False)
        dst.fill((0, 0, 0))
        self.textcount += 1
        surface = load_imageOnly('/UI/sayFrame.png', isAlpha=True, colorkey=-1)
        str1 = u"首领：小桂，你已经充分完成了上级给你分配的任务         "
        str2 = u"小桂：为祖国贡献力量是我的使命和荣耀         "
        str3 = u"首领：本次下潜成果为下一步合理开发南海资源提供了宝贵资料         "
        str4 = u"向你们这群默默奉献的人致敬               "
        if self.textcount < len(str1):
            drawText(surface, str1[:self.textcount], 25, (100, 100), fontInfo(color=(0, 0, 0, 255)))
        elif self.textcount < len(str1) + len(str2):
            drawText(surface, str2[:self.textcount - len(str1)], 25, (100, 100), fontInfo(color=(0, 0, 0, 255)))
        elif self.textcount < len(str1) + len(str2) + len(str3):
            drawText(surface, str3[:self.textcount - len(str1) - len(str2)], 25, (100, 100),
                     fontInfo(color=(0, 0, 0, 255)))
        elif self.textcount < len(str1) + len(str2) + len(str3) + len(str4):
            drawText(surface, str4[:self.textcount - len(str1) - len(str2) - len(str3)], 25, (100, 100),
                     fontInfo(color=(0, 0, 0, 255)))
        self.textcount += 1
        if self.textcount > len(str1) + len(str2) + len(str3) + len(str4):
            GameBody.scene = 0
            self.currentScene = 2
            diver = GameBody.args['diver']
            diver.isShow(True)
            diver.hp.isShow(True)
            diver.air.isShow(True)
            diver.mineBar.isShow(True)
            GameBody.args['handbook'].isShow(True)
            self.textcount = 0
            #self.gotoScene(1, self.welcomeScene)
        dst.blit(surface, (0, 400))
    def update(self):
        diverRect = GameBody.args['diver'].rect.copy()
        #diverRect.x += 20
        diverRect.y += 40
        #diverRect.w -= 10
        diverRect.h -= 50
        GameBody.args['diverCollideRect'] = diverRect
        #print("old rect:", GameBody.args['diverOldRect'])
        if GameBody.isChangeScene:
            self.slideScene()

        if GameBody.keyState[K_F1] == GameBody.BUTTON_DOWN:
            if not self.isfullScreen:
                self.fullScreen()
            else:
                self.exitFullScreen()
        if GameBody.scene == -2:
            self.beginScene(self.screen)

        if GameBody.scene == -3:
            self.endScene(self.screen)

        if GameBody.scene == 0:
            self.gameOverScene.update(self.screen)
            if GameBody.keyState[K_r] == GameBody.BUTTON_DOWN:
                self.restartGame()

        if GameBody.scene == 1:
            #print("welcomeScene is updating")
            if GameBody.keyState[pygame.K_SPACE] == GameBody.BUTTON_DOWN:
                GameBody.isChangeScene = True
            self.welcomeScene.update(self.screen)

        if GameBody.scene == 2:
            self.gameScene.update(self.screen)
            self.decreaseAir()

        if GameBody.scene == 3:
            self.secondScene.update(self.screen)
            self.decreaseAir()

        if GameBody.scene == 4:
            self.darkScene.update(self.screen)
            self.decreaseAir()

        if GameBody.args['diver'].mineBar.num == GameBody.args['diver'].mineBar.maxnum:
            if self.currentScene == 2:
                self.gotoScene(3, self.secondScene)
            elif self.currentScene == 3:
                self.gotoScene(4, self.darkScene)
            elif self.currentScene == 4:
                self.currentScene = 2
                GameBody.args['diver'].mineBar.num = 0
                GameBody.scene = -3

        print(self.currentScene)
        print("scene", GameBody.scene)

        if GameBody.args['diver'].hp.num <= 0:
            self.gotoGameOver(self.screen)
        else:
            #pygame.draw.rect(self.screen, (0, 255, 0), diverRect, 1)
            GameBody.args['diver'].update(self.screen)
            GameBody.args['handbook'].update(self.screen)