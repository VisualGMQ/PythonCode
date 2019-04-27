import pygame
from src.tools import *
from src.animation import *
import src.constants
from src.object import *
from src.GameBody import *
from src.font import *
from src.UITools import *
from src.mines import *
from src.fish import *

class diver(object):
    def __init__(self, pos, state):
        object.__init__(self, '/diverStand/1.png')
        standSur = animation([frame('/diverStand/1.png'), frame('/diverStand/2.png'), frame('/diverStand/3.png'), frame('/diverStand/4.png'), frame('/diverStand/5.png'), frame('/diverStand/6.png'), frame('/diverStand/7.png'), frame('/diverStand/8.png'), frame('/diverStand/9.png'), frame('/diverStand/10.png'),
                              frame('/diverStand/11.png'), frame('/diverStand/12.png'), frame('/diverStand/13.png'), frame('/diverStand/14.png'), frame('/diverStand/15.png'), frame('/diverStand/16.png'), frame('/diverStand/17.png'), frame('/diverStand/18.png'), frame('/diverStand/19.png'), frame('/diverStand/20.png')])
        swimani = animation([frame('diver/1.png', 1), frame('diver/2.png', 1), frame('diver/3.png', 1), frame('diver/4.png', 1), frame('diver/5.png', 1), frame('diver/6.png', 1), frame('diver/7.png', 1), frame('diver/8.png', 1), frame('diver/9.png', 1), frame('diver/10.png', 1),
                             frame('diver/11.png', 1), frame('diver/12.png', 1), frame('diver/13.png', 1), frame('diver/14.png', 1), frame('diver/15.png', 1), frame('diver/16.png', 1), frame('diver/17.png', 1), frame('diver/18.png', 1), frame('diver/19.png', 1), frame('diver/20.png', 1),
                             frame('diver/21.png', 1), frame('diver/22.png', 1), frame('diver/23.png', 1), frame('diver/24.png', 1), frame('diver/25.png', 1), frame('diver/26.png', 1), frame('diver/27.png', 1), frame('diver/28.png', 1), frame('diver/29.png', 1), frame('diver/30.png', 1),])
        swimani.setLoop(True)
        self.state = state
        self.action = {'stand'    : standSur ,
                       'swiming'  : swimani  ,
                       'jumpToSea': swimani  ,
                       'dash'     : swimani  ,
                       'digging'  : swimani  ,
                       'damaged'  : None}
        #self.image = standSur
        #self.rect = self.image.get_rect()
        self.moveTo(pos[0], pos[1])
        self.show = False
        self.oldrect = self.rect
        self.HSPEED = 10
        self.VSPEED = 15
        self.mine = None
        self.hp = Hp()
        self.hp.moveTo(900, 20)
        self.hp.isShow(False)
        self.air = airNum()
        self.air.moveTo(900, 50)
        self.air.isShow(False)
        self.mineBar = mineBar(1)
        self.mineBar.moveTo(1000, 80)
        self.mineBar.isShow(False)
        self.direction = -1
        self.invincible = False
        self.invincibleCount = 0
        self.isGrabbed = False
        self.keyLeft = 0
        self.keyRight = 0
        self.digCount = 0
    def onInit(self):
        standSur = load_imageOnly('/diver/1.png')
        self.mineBar.num = 0
        self.image = standSur
        self.rect = self.image.get_rect()
        self.setState('stand')
        self.moveTo(0, 0)
        self.show = False
        self.oldrect = self.rect
        self.HSPEED = 10
        self.VSPEED = 15
        self.mine = None
        self.hp.num = 10
        self.air.num = 10
        self.hp.moveTo(900, 20)
        self.hp.isShow(False)
        self.air = airNum()
        self.air.moveTo(900, 50)
        self.air.isShow(False)
        self.mineBar.moveTo(1000, 80)
        self.mineBar.isShow(False)
        self.invincible = False
        self.invincibleCount = 0
        self.isGrabbed = False
        self.keyLeft = 0
        self.keyRight = 0
        self.digCount = 0
    def setState(self, state):
        if type(self.action[state])==animation:
            self.action[state].isStopped = False
        self.state = state
        if type(self.action[state]) == animation:
            self.action[self.state].play()
    def backToOldPos(self):
        self.rect.topleft = GameBody.args['diverOldRect'].topleft
    def SwimingState(self):
        if GameBody.keys[K_k]:
            self.HSPEED = 30
            self.VSPEED = 40
        else:
            self.HSPEED = 15
            self.VSPEED = 20
        if not self.isGrabbed:
            if GameBody.keys[K_a]:
                self.move(-self.HSPEED, 0)
                self.direction = -1
            if GameBody.keys[K_d]:
                self.move(self.HSPEED, 0)
                self.direction = 1
            if GameBody.keys[K_w]:
                self.move(0, -self.VSPEED)
                self.directionY = -1
            if GameBody.keys[K_s]:
                self.move(0, self.VSPEED)
                self.directionY = 1
            #if GameBody.keys[K_j]:
            #    self.setState('shoot')
    def outOfGrab(self):
        if self.isGrabbed:
            self.timecount += 1
            if GameBody.keyState[K_a] == GameBody.BUTTON_DOWN:
                self.keyLeft += 1
            if GameBody.keyState[K_d] == GameBody.BUTTON_DOWN:
                self.keyLeft += 1
            if self.timecount <= 50 and self.keyLeft >= 5 and self.keyRight >= 5:
                self.isGrabbed = False
                self.keyLeft = 0
                self.keyRight = 0
                self.setState('swiming')
    def JumpToSeaState(self):
        CONVERT_TICK = 50
        if self.timecount < CONVERT_TICK:
            self.move((600 - 700) // CONVERT_TICK, -300 // CONVERT_TICK)
        else:
            self.setState('swiming')
        self.timecount += 1
    def dig(self):
        pass
    def setMine(self, mine):
        self.mine = mine
    def DiggingState(self, dst):
        if self.mine and self.digCount <= self.mine.diggingTime:
            #print("digging")
            #print(self.digCount)
            rate = self.digCount/self.mine.diggingTime
            surface = load_imageOnly('/UI/processBar.png')
            surface = surface.subsurface(pygame.Rect(0, 0, int(surface.get_width()*rate), surface.get_height()))
            dst.blit(surface, (GameBody.args['diver'].rect.x - 75, GameBody.args['diver'].rect.y - 10))
            self.digCount += 1
        else:
            self.digCount = 0
            if self.mine.type == NON_RENEWABLE:
                self.mine.isShow(False)
            else:
                self.mine.image = pygame.transform.scale(self.mine.image, (self.mine.rect.w, self.mine.rect.h//3))
                self.mine.isDigged = True
            self.mineBar.num += 1
            playMineSound()
            self.setState("swiming")
            GameBody.args['handbook'].addMine(self.mine.image.copy(), self.mine.info)
            self.setMine(None)
            #print("dig end")
    def helpState(self, dst):
        if self.mine and self.digCount <= self.mine.helpTime:
            rate = self.digCount / self.mine.helpTime
            surface = load_imageOnly('/UI/processBar.png')
            surface = surface.subsurface(pygame.Rect(0, 0, int(surface.get_width() * rate), surface.get_height()))
            dst.blit(surface, (GameBody.args['diver'].rect.x - 75, GameBody.args['diver'].rect.y - 10))
            self.digCount += 1
        else:
            self.digCount = 0
            self.mine.setState("helped")
            self.setState("swiming")
            self.setMine(None)
    def wasAttacked(self):
        self.invincible = True
        self.hp.num -= 1
    def invincibleState(self):
        self.invincibleCount += 1
        self.show = not self.show
        if self.invincibleCount >= 50:
            self.invincible = False
            self.invincibleCount = 0

    def update(self, dst):
        object.beginUpdate(self)

        self.oldrect = self.rect
        if self.state == 'swiming' or self.state == 'shoot':
            self.SwimingState()
        #if self.action['shoot'].isStopped:
        #    self.setState('swiming')
        if self.state == 'jumpToSea':
            self.JumpToSeaState()

        #draw status bars
        self.hp.update(dst)
        self.air.update(dst)
        self.mineBar.update(dst)

        object.endUpdate(self, dst)

        if GameBody.keys[K_j]:
            if type(self.mine) == mine:
                #self.setState('digging')
                self.DiggingState(dst)
            elif type(self.mine) == injuredFish:
                self.helpState(dst)

        if self.mine == None:
            self.digCount = 0

        if self.invincible:
            self.invincibleState()

