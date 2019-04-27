import pygame
from src.tools import *
from src.object import *
from src.animation import *
import src.constants
from src.GameBody import *
from src.font import *

class fish(object):
    def __init__(self, image=None):
        object.__init__(self, image, "")
        self.show = False

class simpleFish(fish):
    def __init__(self, image, ani):
        fish.__init__(self, image)
        self.action = {'swiming': ani}
        self.setState('swiming')
        self.direction = 1
    def borderCollision(self):
        if self.rect.x < 0:
            self.moveTo(0, self.rect.y)
            self.direction = 1
        if self.rect.x + self.rect.w > src.constants.SCREEN_SIZE[0]:
            self.moveTo(src.constants.SCREEN_SIZE[0] - self.rect.w, self.rect.y)
            self.direction = -1
    def update(self, dst):
        fish.beginUpdate(self)
        self.borderCollision()
        #if self.state == 'swiming':
        self.move(5*self.direction, 0)
        #print(self.rect)
        fish.endUpdate(self, dst)

class fugu(fish):
    def __init__(self):
        fish.__init__(self, load_imageOnly('/fugu1/1.png'))
        self.state = 'swiming'
        self.action = {'swiming': animation([frame('/fugu1/1.png'), frame('/fugu1/2.png'),frame('/fugu1/3.png'), frame('/fugu1/4.png'), frame('/fugu1/5.png'),
                                             frame('/fugu1/6.png'), frame('/fugu1/7.png'), frame('/fugu1/8.png'), frame('/fugu1/9.png'), frame('/fugu1/10.png')]),
                        'attack': animation([frame('/fugu2/1.png'), frame('/fugu2/2.png'),frame('/fugu2/3.png'), frame('/fugu2/4.png'), frame('/fugu2/5.png'),
                                             frame('/fugu2/6.png'), frame('/fugu2/7.png'), frame('/fugu2/8.png'), frame('/fugu2/9.png'), frame('/fugu2/10.png')])}
        self.attackDist = 200
    def update(self, dst):
        fish.beginUpdate(self)
        #swiming:
        if self.state=='swiming' or self.state=='attack':
            if self.direction==1:
                self.move(10, 0)
                if self.rect.x+self.rect.w > src.constants.SCREEN_SIZE[0]:
                    self.direction=-1
            else:
                self.move(-10, 0)
                if self.rect.x < 0:
                    self.direction=1
        #is diver in arange of attack
        vector = pygame.math.Vector2(GameBody.args['diverLocalRect'].center[0] - self.rect.center[0],GameBody.args['diverLocalRect'].center[1] - self.rect.center[1])
        if self.state=='attack':
            colrect = pygame.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.w -10, self.rect.h -10)
            if colrect.colliderect(GameBody.args['diverLocalRect']) and not GameBody.args['diver'].invincible:
                GameBody.args['diver'].wasAttacked()
            #pygame.draw.rect(dst, (0,255,0), colrect, 1)

        if vector.length() < self.attackDist:
            self.setState('attack')
        else:
            if self.state=='attack':
                self.setState('swiming')
        #pygame.draw.circle(dst, (255,0,0), self.rect.center, self.attackDist,1 )

        fish.endUpdate(self, dst)

class shark(fish):
    def __init__(self):
        fish.__init__(self, load_imageOnly('/shark/1.png'))
        self.attackDist = 400
        ani = animation([frame('/shark/1.png'), frame('/shark/2.png'), frame('/shark/3.png'), frame('/shark/4.png'), frame('/shark/5.png'),
                         frame('/shark/6.png'), frame('/shark/7.png'), frame('/shark/8.png'), frame('/shark/9.png'), frame('/shark/10.png')])
        self.action = {'swiming': ani,
                        'attack': ani,
                       'dashAttack': ani,
                       'rest': ani}
        self.state = 'swiming'
        self.willAttack = False
        self.attackPos = None
    def update(self, dst):
        object.beginUpdate(self)
        # swiming:
        if self.state == 'swiming' or self.state == 'attack':
            if self.direction == 1:
                self.move(10, 0)
                if self.rect.x + self.rect.w > src.constants.SCREEN_SIZE[0]:
                    self.direction = -1
            else:
                self.move(-10, 0)
                if self.rect.x < 0:
                    self.direction = 1
        vector = pygame.math.Vector2(GameBody.args['diverLocalRect'].center[0] - self.rect.center[0],
                                     GameBody.args['diverLocalRect'].center[1] - self.rect.center[1])
        global theta
        theta = 0
        if self.direction == 1:
            theta = vector.angle_to(pygame.math.Vector2(1, 0))
        else:
            theta = 3.1415926 - vector.angle_to(pygame.math.Vector2(-1, 0))

        if self.state=='swiming':
            if vector.length() < self.attackDist and (GameBody.args['diverLocalRect'].x-self.rect.x)*self.direction >= 0 and not GameBody.isChangeScene:
                self.setState('attack')

        if self.state=='attack':
            self.image = pygame.transform.rotate(self.image, theta)
            #is in the same side
            if (GameBody.args['diverLocalRect'].x-self.rect.x)*self.direction < 0:
                self.setState('swiming')
            else:
                self.timecount += 1
                if self.timecount >= 10:
                    self.attackPos = (GameBody.args['diverLocalRect'].center[0], GameBody.args['diverLocalRect'].center[1])
                    self.setState('dashAttack')
                    self.timecount = 0

        if self.state == 'dashAttack':
            global attackVec
            attackVec = pygame.math.Vector2(self.attackPos[0] - self.rect.center[0],
                                                 self.attackPos[1] - self.rect.center[1])
            attackVec += attackVec.normalize()*20
            if getDistance(self.attackPos, self.rect.center) < 10:
                self.setState('rest')
                self.timecount = 0
            else:
                self.image = pygame.transform.rotate(self.image, theta)
                self.move(attackVec.x//4, attackVec.y//4)

        if self.rect.colliderect(GameBody.args['diverLocalRect']) and not GameBody.args['diver'].invincible:
            GameBody.args['diver'].wasAttacked()

        if self.state == 'rest':
            self.timecount += 1
            if self.timecount >= 10:
                self.setState('swiming')
                self.timecount = 0
        #pygame.draw.rect(dst, (0, 255, 0), self.rect, 1)
        #pygame.draw.circle(dst, (255, 0, 0), self.rect.center, self.attackDist, 1)
        fish.endUpdate(self, dst)

class assassion(fish):
    def __init__(self):
        fish.__init__(self, load_imageOnly('/UI/holl.png'))
        ani = [frame('/assassion/assassion2.png'), frame('/assassion/assassion2.png'), frame('/assassion/assassion3.png'), frame('/assassion/assassion1.png')]
        self.action = {'normal': load_imageOnly('/UI/holl.png'),
                       'attack': animation(ani)}
        self.bgImage = load_imageOnly('/UI/holl.png')
        self.setState('normal')
    def update(self, dst):
        fish.beginUpdate(self)

        if self.state == 'normal' and not GameBody.isChangeScene:
            if self.rect.collidepoint(GameBody.args['diverLocalRect'].center):
                self.setState('attack')
        if self.action['attack'].isStopped:
            self.setState('normal')
            self.action['attack'].isStopped = False

        if self.state == 'attack':
            if self.rect.colliderect(GameBody.args['diverLocalRect']) and self.action['attack'].getCurrentFrame() == 4:
                GameBody.args['diver'].hp.num = 0
        #pygame.draw.rect(dst, (255, 0, 0), self.rect, 1)
        dst.blit(self.bgImage, (self.rect.center[0] - self.bgImage.get_width()//2, self.rect.center[1] - self.bgImage.get_height()//2))
        fish.endUpdate(self, dst)

class assassion2(fish):
    def __init__(self):
        fish.__init__(self, load_imageOnly('/assassion2/1.png'))
        self.action = {'normal' : animation([frame('/assassion2/1.png'), frame('/assassion2/2.png'), frame('/assassion2/3.png'), frame('/assassion2/4.png'), frame('/assassion2/5.png'),
                                             frame('/assassion2/6.png'), frame('/assassion2/7.png'), frame('/assassion2/8.png'), frame('/assassion2/9.png'), frame('/assassion2/10.png')]),
                       'attack' : animation([frame('/assassion2/3.png'), frame('/assassion2/4.png'), frame('/assassion2/5.png')])}
        self.setState('normal')
    def update(self, dst):
        fish.beginUpdate(self)

        colliderect = self.rect.copy()
        if self.direction == 1:
            colliderect.x += 89
            colliderect.y += 40
            colliderect.w = 100
            colliderect.h = 90
        if self.state == 'normal' and colliderect.colliderect((GameBody.args['diverLocalRect'])):
            self.setState('attack')

        if self.state == 'attack':
            if self.action[self.state].getCurrentFrame() == 3:
                GameBody.args['diver'].hp.num = 0
            if self.action[self.state].isStopped:
                self.setState('normal')
        #pygame.draw.rect(dst, (0,255,0), colliderect, 1)
        fish.endUpdate(self, dst)

class jellyfish(fish):
    def __init__(self):
        fish.__init__(self, load_imageOnly('/jelly/1.png'))
        ani = animation([frame('/jelly/1.png'), frame('/jelly/2.png'),frame('/jelly/3.png'), frame('/jelly/4.png'),frame('/jelly/5.png'),
                         frame('/jelly/6.png'), frame('/jelly/7.png'), frame('/jelly/8.png'), frame('/jelly/9.png'), frame('/jelly/10.png')])
        self.action = {'swiming': ani,
                       'attack': ani,
                       'outOfGrab': ani}
        self.setState('swiming')
        self.type = 1
        self.grabcount = 0
        self.playedSound = False
        self.swimcount = 0
        self.sound = pygame.mixer.Sound('../resource/audio/current.wav')
    def SwimingState(self, dst):
        rect = self.rect.copy()
        rect.y += 30
        rect.h -= 30
        #pygame.draw.rect(dst, (255, 0, 0), rect, 1)
        if rect.colliderect(GameBody.args['diverLocalRect']):
            # 被缠住的样子
            GameBody.args['diver'].move(rect.x - GameBody.args['diverLocalRect'].topleft[0], (rect.y - GameBody.args['diverLocalRect'].topleft[1])//2)
            self.setState("attack")
            GameBody.args['diver'].isGrabbed = True
        else:
            if self.type == 2:
                self.swimcount += 1
                if self.direction == 1:
                    self.move(10, 30 * math.sin(self.swimcount))
                    if self.rect.x + self.rect.w > src.constants.SCREEN_SIZE[0]:
                        self.direction = -1
                else:
                    self.move(-10, 30 * math.sin(self.swimcount))
                    if self.rect.x < 0:
                        self.direction = 1
                if self.swimcount >= 100:
                    self.swimcount = 0
    def AttackState(self):
        self.grabcount += 1

        if not self.playedSound:
            self.playedSound = True
            self.sound.play()

        if GameBody.args['diver'].isGrabbed == False:
            self.setState("outOfGrab")

        #if self.action[self.state].isStopped:
        #    self.action[self.state].isStopped = False
        #    self.setState('swiming')
        if self.grabcount >= 50:
            GameBody.args['diver'].isGrabbed = False
            self.grabcount = 0
            self.playedSound = False
    def outOfGrabState(self):
        self.timecount += 1
        if self.timecount >= 20:
            self.timecount = 0
            self.setState('swiming')
    def update(self, dst):
        fish.beginUpdate(self)
        if self.state == 'swiming' and not GameBody.isChangeScene:
            self.SwimingState(dst)

        if self.state == 'attack':
            self.AttackState()

        if self.state == 'outOfGrab':
            self.outOfGrabState()

        fish.endUpdate(self, dst)

class cuttlefish(fish):
    def __init__(self):
        fish.__init__(self, '/cuttlefish/1.png')
        self.action = {'normal': animation([frame('/cuttlefish/1.png'), frame('/cuttlefish/2.png'),frame('/cuttlefish/3.png'),frame('/cuttlefish/4.png'),frame('/cuttlefish/5.png'),
                                            frame('/cuttlefish/6.png'), frame('/cuttlefish/7.png'),frame('/cuttlefish/8.png'),frame('/cuttlefish/9.png'),frame('/cuttlefish/10.png')]),
                       'attack': animation([frame('/cuttlefish/1.png'), frame('/cuttlefish/2.png'),frame('/cuttlefish/3.png'),frame('/cuttlefish/4.png'),frame('/cuttlefish/5.png'),
                                            frame('/cuttlefish/6.png'), frame('/cuttlefish/7.png'),frame('/cuttlefish/8.png'),frame('/cuttlefish/9.png'),frame('/cuttlefish/10.png')])
                       }
        self.inkAni = animation([frame('/UI/ink/1.jpg'), frame('/UI/ink/2.jpg'), frame('/UI/ink/3.jpg'),
                                 frame('/UI/ink/4.jpg'), frame('/UI/ink/5.jpg'), frame('/UI/ink/6.jpg'),
                                 frame('/UI/ink/7.jpg')])
        #self.inkAni.rect.center = ([self.rect.center[0], self.rect.center[1]])
        self.setState('normal')
    def update(self, dst):
        fish.beginUpdate(self)

        if self.rect.colliderect(GameBody.args['diverLocalRect']) and self.state == 'normal':
            self.setState('attack')
            self.inkAni.play()
            #GameBody.setFade(3, 10, 200)

        fish.endUpdate(self, dst)

        if self.state == 'attack':
            surface = self.inkAni.update()
            rect = surface.get_rect()
            rect.center = self.rect.center
            dst.blit(surface, rect)
            if self.inkAni.isStopped:
                self.setState('normal')

class injuredFish(fish):

    class Bubble(object):
        def __init__(self):
            object.__init__(self, "/UI/bubble.png")
            self.canGet = False
            self.sound = pygame.mixer.Sound('../resource/audio/bubble1.wav')
            self.soundPlayed = False
        def update(self, dst):
            if self.show:
                if not self.canGet:
                    if not self.soundPlayed:
                        self.sound.play()
                        self.soundPlayed = True
                    self.timecount += 1
                    if self.timecount <= 10:
                        self.move(0, -10)
                    else:
                        self.timecount = 0
                        self.canGet = True
                if self.canGet:
                    if self.rect.colliderect(GameBody.args['diverLocalRect']):
                        GameBody.args['diver'].air.num += 2
                        #print("goto show False")
                        if self.soundPlayed:
                            self.sound.stop()
                        self.isShow(False)

            if self.show:
                dst.blit(self.image, self.rect)

    def __init__(self, image, ani):
        fish.__init__(self, image)
        self.action = {'helped': ani}
        self.action['injured'] = ani.frames[0].image
        self.action['swiming'] = ani

        self.setState('injured')
        self.bubble = self.Bubble()
        self.ishelped = False
        self.helpTime = 50
    def drawHelp(self, dst):
        MINDIST = 200
        drawText(dst, "Help Me!", 25, (self.rect.x, self.rect.y - 50), fontInfo(color=(255, 0, 0)))
        if getDistance(self.rect.center ,GameBody.args['diverLocalRect'].center) <= MINDIST:
            if GameBody.args['diver'].state == 'swiming' and not self.ishelped:
                GameBody.args['diver'].setMine(self)
        else:
            if GameBody.args['diver'].mine == self:
                GameBody.args['diver'].mine = None
                GameBody.args['diver'].digCount = 0

    def drawNet(self, dst):
        surface = load_imageOnly("/UI/net.png")
        surface = pygame.transform.scale(surface, (surface.get_width(), self.rect.height))
        dst.blit(surface, (self.rect.center[0] - surface.get_width()//2 + 10, self.rect.center[1] - surface.get_height()//2))
    def update(self, dst):
        fish.beginUpdate(self)

        if self.state == 'helped':
            if tuple(self.bubble.rect.topleft) == (0, 0):
                self.bubble.rect.topleft = (self.rect.x + self.rect.w, self.rect.y - 10)

            if self.action['helped'].isStopped:
                self.bubble.isShow(True)
                self.setState("swiming")

        if self.state == 'swiming' and self.rect.x <= 2000:
            self.move(10, 0)

        self.bubble.update(dst)

        fish.endUpdate(self, dst)
        if self.state == 'injured':
            self.drawNet(dst)
            self.drawHelp(dst)