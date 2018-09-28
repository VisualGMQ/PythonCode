import pygame
import PlusEngine
import math
import random
import sys

__author__ = 'VisualGMQ'
__date__='2018.3.10'

count = 0
rocketcount=0
GRAVITY = 2
score = 0
FirstJump = False
scense = 1
pygame.init()
WNDSIZE = [700, 700]
screen = pygame.display.set_mode(WNDSIZE, 0, 32)
land_y = 600
land_points = [0, land_y, WNDSIZE[0], land_y]
DropSpeed = 2
fullscreen = False
started = False
SLable = PlusEngine.Text("Press SPACE  to start", 70)
clock = pygame.time.Clock()
# CAPTION PIC
try:
    caption_pic = pygame.image.load("pic/Cover.png").convert_alpha()
except:
    print("can't open the image!")
# score text
font = pygame.font.SysFont("Arial", 20, True)
scoretext = font.render(str(score), True, (0, 0, 0))
quittext=font.render("press esc to auit",True,(0,0,0))
retrytext=font.render("press 'r' to quit",True,(0,0,0))


# not finished
class destoryblock(pygame.sprite.Sprite):
    rect1 = pygame.Surface((15, 15))
    rect1.fill(pygame.Color(255, 255, 255))
    rect2 = rect1.copy()
    rect3 = rect1.copy()
    rect4 = rect1.copy()
    vspeed = 10
    '''
        1_|_2
        3_|_4 
    '''

    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.angles = [0] * 4
        self.pos = list(pos) * 4
        self.vspeed = destoryblock.vspeed

    def update(self, dest):
        # one rect can show others' state
        if destoryblock.rect1.get_rect().y <= WNDSIZE[1]:
            self.angles[0] -= 10
            self.angles[1] += 10
            self.angles[2] += 10
            self.angles[3] -= 10
            self.pos[0][0] -= 10
            self.pos[1][0] += 10
            self.pos[2][0] += 10
            self.pos[3][0] -= 10

class Rocket(pygame.sprite.Sprite):
    def __init__(self,y):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load("pic/rocket.bmp").convert()
            self.image.set_colorkey(pygame.Color(255, 255, 255))
        except:
            print("can't open the image")
        self.rect=self.image.get_rect().copy()
        self.size=self.image.get_size()
        self.hspeed=10
        self.angle=0
        self.direct=0
        self.RotateFrame()
        self.SetRandom()
        self.destoryed=False
        if self.direct == 1:  # 1 is direct to left
            self.image = pygame.transform.flip(self.image, True, False)
            self.MoveTo((0,y))
        elif self.direct==-1:
            self.MoveTo((WNDSIZE[0],y))
    def RotateFrame(self):
        self.angle=45*math.sin(math.radians(self.rect.x)//10)
    def MoveDelta(self,deltapos):
        self.rect.x+=deltapos[0]
        self.rect.y+=deltapos[1]
    def SetY(self,y):
        self.rect.y=y
    def MoveTo(self,npos):
        self.rect.x=npos[0]
        self.rect.y=npos[1]
    def SetRandom(self):
        result=random.randint(1,2)
        if result==1:
            self.direct=-1
        if result==2:
            self.direct=1
    def Collied(self):
        if pygame.sprite.collide_rect(man,self):
            man.death=True
    def update(self,dest):
        self.Collied()
        if self.direct==1:
            self.MoveDelta((self.hspeed,0))
            if self.rect.x>self.size[0]+WNDSIZE[0]:
                self.destoryed=True
        elif self.direct==-1:
            self.MoveDelta((-self.hspeed,0))
            if self.rect.x+self.size[0]<0:
                self.destoryed=True
        PlusEngine.DrawTool.BlitOnlyRotate(dest,self.image,(self.rect.x,self.rect.y),self.angle)

class Block(pygame.sprite.Sprite):
    def __init__(self, bgcolor=pygame.Color(255, 255, 255), boarderlen=30):
        pygame.sprite.Sprite.__init__(self)
        self.bgcolor = bgcolor
        surface = pygame.Surface((boarderlen, boarderlen))
        surface.fill(self.bgcolor)
        pygame.draw.rect(surface, pygame.Color(0, 0, 0), pygame.Rect(0, 0, boarderlen, boarderlen), 1)
        self.image = surface.copy()
        self.rect = surface.get_rect().copy()
        self.destory = False

    def GetSize(self):
        return (self.rect.width, self.rect.height)

    def GetPos(self):
        return (self.rect.x, self.rect.y)

    def GetRect(self):
        return self.rect

    def Move(self, npos):
        self.rect.x = npos[0]
        self.rect.y = npos[1]

    def MoveDelta(self, deltapos):
        self.rect.x += deltapos[0]
        self.rect.y += deltapos[1]

    def update(self, dest):
        if self.destory == False:
            PlusEngine.DrawTool.Blit(dest, self.image, self.GetPos())


class tetris(pygame.sprite.Sprite):
    type = []
    vspeed = 5
    type.append(list([[1, 0, 0], [1, 1, 1]]))
    type.append(list([[0, 0, 1], [1, 1, 1]]))
    type.append(list([[1], [1], [1], [1]]))
    type.append(list([[0, 1, 1], [1, 1, 0]]))
    type.append(list([[1, 0], [1, 1], [1, 0]]))
    type.append(list([[1, 1, 1], [0, 1, 0]]))
    type.append(list([[0, 1], [1, 1], [0, 1]]))
    type.append(list([[1, 1], [1, 0], [1, 0]]))
    type.append(list([[1, 1, 1], [1, 0, 0]]))
    type.append(list([[1, 1], [1, 1]]))
    type.append(list([[0, 1, 0], [1, 1, 1]]))
    type.append(list([[1, 1, 1, 1]]))
    type.append(list([[1, 1, 0], [0, 1, 1]]))

    def __init__(self, xinteval, yinteval,formery,distance):
        pygame.sprite.Sprite.__init__(self)
        self.type = tetris.type[random.randint(0, len(tetris.type) - 1)]
        self.color = pygame.Color(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.block = [Block(self.color), Block(self.color), Block(self.color), Block(self.color)]
        self.xinteval = xinteval
        self.yinterval = yinteval
        # order the blocks by self.type
        self.first = True
        #self.posy = random.randint(self.yinterval[0], self.yinterval[1])
        self.posy=formery-distance
        self.InitPos()
        for i in range(len(self.block)):
            Map.add(self.block[i])

    def ChangeType(self):
        self.type = tetris.type[random.randint(0, len(tetris.type) - 1)]

    def InitPos(self):
        #posx = random.randint(self.xinteval[0], self.xinteval[1])
        posx=random.randint(0,WNDSIZE[0]-100)
        if self.type == tetris.type[3]:
            if self.first == True:
                self.block[0].Move((posx, self.posy))
                self.first = False
            # else:
            #     self.posy = 0
            self.block[0].Move((posx, self.posy))
            self.block[1].Move((self.block[0].GetPos()[0] + self.block[0].GetSize()[0], 0))
            self.block[2].Move((self.block[1].GetPos()[0] + self.block[1].GetSize()[0], 0))
            self.block[3].Move((self.block[2].GetPos()[0] + self.block[2].GetSize()[0], 0))
        else:
            num = 0
            for y in range(len(self.type)):
                for x in range(len(self.type[y])):
                    if self.type[y][x] == 1:
                        self.block[num].Move(
                            (x * self.block[num].GetSize()[0] + posx, y * self.block[num].GetSize()[1] + self.posy))
                        num += 1
    def GetPosy(self):
        return self.posy
    def update(self, dest):
        # re-init tertris
        num = 0
        for ele in self.block:
            if ele.GetPos()[1] > spike.GetPos()[1]:
                num += 1
        if num == 4:
            self.InitPos()
            self.ChangeType()
        # draw block
        for i in range(len(self.block)):
            self.block[i].MoveDelta((0, tetris.vspeed))
            PlusEngine.DrawTool.Blit(dest, self.block[i].image, self.block[i].GetPos())


class spikes(pygame.sprite.Sprite):
    def __init__(self, width=WNDSIZE[0], height=30):
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.Surface((width, height))
        surface.fill(pygame.Color(255, 255, 255))
        self.rect = surface.get_rect().copy()

        # small help function to draw one triangle:
        def DrawOneTriangle(offx):
            pygame.draw.line(surface, pygame.Color(0, 0, 0), (offx, self.rect.height),
                             (math.floor(offx + math.tan(math.radians(30)) * self.rect.height), 0))
            pygame.draw.line(surface, pygame.Color(0, 0, 0),
                             (math.floor(offx + math.tan(math.radians(30)) * self.rect.height), 0),
                             (math.floor(offx + math.tan(math.radians(30)) * self.rect.height * 2), height))

        num = math.floor(self.rect.width // math.tan(math.radians(30)) * self.rect.height * 2)
        for i in range(num + 1):
            DrawOneTriangle(i * math.tan(math.radians(30)) * self.rect.height * 2)
        self.image = surface.copy()

    def GetPos(self):
        return (self.rect.x, self.rect.y)

    def GetSize(self):
        return (self.rect.width, self.rect.height)

    def GetRect(self):
        return self.rect.copy()

    def Move(self, npos):
        self.rect.x = npos[0]
        self.rect.y = npos[1]

    def MoveDelta(self, deltapos):
        self.rect.x += deltapos[0]
        self.rect.y += deltapos[1]

    def update(self, dest):
        PlusEngine.DrawTool.Blit(dest, self.image, self.GetPos())


class role(Block):
    def __init__(self, boarderlen=30):
        Block.__init__(self, pygame.Color(255, 255, 255), boarderlen)
        self.hspeed = 0
        self.runspeed = 10
        self.haccelerate = 2
        self.vspeed = 0
        self.x_bounded = 0  # if collied on left or right,-1 is left;1 is right
        self.jumpspeed = -30
        self.onland = True
        self.death = False
        self.oldrect = self.rect.copy()
        self.Move((0, land_y - self.GetSize()[0]))

    def MoveDelta(self, deltapos):
        self.rect.x += deltapos[0]
        self.rect.y += deltapos[1]

    def Run(self):
        if key[pygame.K_a]:
            self.hspeed -= self.haccelerate
        if key[pygame.K_d]:
            self.hspeed += self.haccelerate
        if (key[pygame.K_a] == 0 and key[pygame.K_d] == 0) or (key[pygame.K_a] == 1 and key[pygame.K_d] == 1):
            self.hspeed = 0

    def jump(self):
        if key[pygame.K_k]:
            if self.onland == True:
                self.vspeed = self.jumpspeed
                self.onland = False
            if self.x_bounded == 1:
                #print("the 1 speed:",self.runspeed)
                self.hspeed = -(self.runspeed)
                self.vspeed = self.jumpspeed // 2
                self.x_bounded = 0
            if self.x_bounded == -1:
                #print("the -1 speed:",self.runspeed)
                self.hspeed = self.runspeed
                self.vspeed = self.jumpspeed // 2
                self.x_bounded = 0

    def GetColiedDirect(self):
        col_list = pygame.sprite.spritecollide(self, Map, False)
        bound_list = [None] * 8
        for block in col_list:
            xcol = 0
            ycol = 0
            # get xcol and ycol
            if self.oldrect.x >= block.GetPos()[0] + block.GetSize()[0]:
                xcol = -1  # collied on right
            if self.oldrect.x + self.oldrect.width <= block.GetPos()[0]:
                xcol = 1  # collied on leftd
            if self.oldrect.y >= block.GetPos()[1] + block.GetSize()[1]:
                ycol = -1  # collied on bottom
            if self.oldrect.y + self.oldrect.height <= block.GetPos()[1]:
                ycol = 1  # collied on top

            # small help function:
            def helpfunction(num):
                if bound_list[num] == None:
                    bound_list[num] = block
                else:
                    if PlusEngine.Collision.GetPointDistance(block.GetRect().center,
                                                             self.oldrect.center) < PlusEngine.Collision.GetPointDistance(
                            bound_list[num].GetRect().center, self.oldrect.center):
                        bound_list[num] = block

            if ycol == -1 and xcol == 0:
                # collied on top
                helpfunction(0)
            # collied on top-right
            if ycol == -1 and xcol == 1:
                helpfunction(1)
            # on right
            if ycol == 0 and xcol == 1:
                helpfunction(2)
            # on right-bottom
            if ycol == 1 and xcol == 1:
                helpfunction(3)
            # on bottom
            if ycol == 1 and xcol == 0:
                helpfunction(4)
            # on bottom-left
            if ycol == 1 and xcol == -1:
                helpfunction(5)
            # on left
            if ycol == 0 and xcol == -1:
                helpfunction(6)
            # on top-left
            if ycol == -1 and xcol == -1:
                helpfunction(7)
        return bound_list

    def Collision(self):
        self.x_bounded=0
        # collied map:
        result = self.GetColiedDirect()
        # collied blocks:
        if result == None or result == [None] * 8:
            self.onland = False
        else:
            '''
               _7_|___0___|_1_
               _6_|_myself|_2_  the result array
               _5_|___4___|_3_
            '''
            if not result[0] == None:
                self.Move((self.GetPos()[0], result[0].GetPos()[1] + result[0].GetSize()[1]))
                self.vspeed = tetris.vspeed
            if not result[1] == None:
                self.Move((result[1].GetPos()[0] - self.GetSize()[0], self.GetPos()[1]))
            if not result[2] == None:
                self.Move((result[2].GetPos()[0] - self.GetSize()[0], self.GetPos()[1]))
                self.x_bounded = 1
            #elif not self.x_bounded==0:
            #    self.x_bounded = 0
            if not result[3] == None:
                self.Move((self.GetPos()[0], result[3].GetPos()[1] - self.GetSize()[1]))
                self.onland = True
            if not result[4] == None:
                self.Move((self.GetPos()[0], result[4].GetPos()[1] - self.GetSize()[1]))
                self.onland = True
            if not result[5] == None:
                self.Move((self.GetPos()[0], result[5].GetPos()[1] - self.GetSize()[1]))
            if not result[6] == None:
                self.Move((result[6].GetPos()[0] + result[6].GetSize()[0], self.GetPos()[1]))
                self.x_bounded = -1
            #elif not self.x_bounded==0:
            #    self.x_bounded = 0
            if not result[7] == None:
                self.Move((result[7].GetPos()[0] + result[7].GetSize()[0], result[7].GetPos()[1] + self.GetSize()[1]))

        if self.onland == True:
            if not result[4] == None:
                if self.vspeed > tetris.vspeed:
                    self.vspeed = tetris.vspeed
            else:
                self.vspeed = 0
        else:
            self.vspeed += GRAVITY
        # collied bottom land
        if self.GetPos()[1] + self.GetSize()[1] > land_y and self.GetPos()[0] + self.GetSize()[0] > land_points[0] and self.GetPos()[0] < land_points[2]:
            self.Move((self.GetPos()[0], land_y - self.GetSize()[0]))
            self.onland = True
        # collied strike:
        if self.GetPos()[1] + self.GetSize()[1] > spike.GetPos()[1]:
            self.death = True
        # collied boarder
        if self.GetPos()[0] < 0:
            self.Move((0, self.GetPos()[1]))
        if self.GetPos()[0] + self.GetSize()[0] > WNDSIZE[1]:
            self.Move((WNDSIZE[1] - self.GetSize()[0], self.GetPos()[1]))

    def update(self, dest):
        self.oldrect = self.rect.copy()
        if self.vspeed > 30:
            self.vspeed = 30
        # use acceleration to speed up object
        if self.hspeed > 15:
            self.hspeed = 15
        elif self.hspeed < -15:
            self.hspeed = -15
        self.MoveDelta((self.hspeed, self.vspeed))
        self.jump()
        self.Run()
        self.Collision()
        PlusEngine.DrawTool.Blit(screen, self.image, self.GetPos())


Map = pygame.sprite.Group()
man = role()
rocket=None
spike = spikes()
spike.Move((0, WNDSIZE[1]))
tetrises = [tetris((0, 100), (-300, -200), 0, 100), tetris((100, 200), (-200, -100), 0, 200),
                        tetris((200, 300), (-100, 0), 0, 300),
                        tetris((300, 400), (-400, -300), 0, 400), tetris((400, 500), (-800, -700), 0, 500),
                        tetris((500, 600), (-600, -500), 0, 600),
                        tetris((600, 700), (-700, -700), 0, 700), tetris((700, 800), (-500, -400), 0, 250),
                        tetris((800, 900), (-900, -800), 0, 450)]

def DrawStart():
    global scense
    DrawCaption()
    if key[pygame.K_SPACE] == True:
        scense = 2


def DrawGame():
    global scense,rocketcount,rocket
    # Render some surface and filp
    global score, started
    if key[pygame.K_SPACE]:
        started = True
    # draw rocket
    if started == True:
        if man.death == False:
            if rocketcount >= 300:
                rocket = Rocket(man.GetPos()[1])
                # rocket.SetY(man.GetPos()[1])
                rocketcount = 0
            if rocketcount < 300 and not rocket == None:
                rocket.update(screen)
        else:
            rocket == None
    # draw your score
    if started == True and FirstJump == True:
        if man.death == False:
            score += 1
            scoretext = font.render("score:" + str(score), True, (0, 0, 0))
            PlusEngine.DrawTool.Blit(screen, scoretext, (0, 0))
    if man.death == False:
        if started == True:
            DrawTetris()
        DrawRole()
        DrawMap()
    else:
        DeathText = PlusEngine.Text("GAME OVER" + ",Your Score is:" + str(score)+".    Press 'R' To Retry. Or press 'esc' to quit", 20)
        DeathText.Render(screen)


def DrawMap():
    # land init show and animate
    if FirstJump == True and land_points[0] <= land_points[2]:
        land_points[0] += 50
        land_points[2] -= 50
    if land_points[0] <= land_points[2]:
        pygame.draw.line(screen, pygame.Color(0, 0, 0), (land_points[0], land_points[1]),
                         (land_points[2], land_points[3]))
    # spike show animate
    if started == True and spike.GetPos()[1] > WNDSIZE[1] - spike.GetSize()[1]:
        spike.MoveDelta((0, -5))
    if started == True and spike.GetPos()[1] < WNDSIZE[1] - spike.GetSize()[1]:
        spike.Move((0, WNDSIZE[1] - spike.GetSize()[1]))
    spike.update(screen)
    if started == False:
        SLable.Render(screen)


def DrawCaption():
    PlusEngine.DrawTool.BlitOnlyResize(screen, caption_pic, (0, 0), WNDSIZE)


def DrawRole():
    man.update(screen)


def DrawTetris():
    for i in tetrises:
        i.update(screen)

while True:
    timepass = clock.tick(30)
    screen.fill(pygame.Color(255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            # change to full screen:
            if event.key == pygame.K_l:
                if fullscreen == False:
                    screen = pygame.display.set_mode(WNDSIZE, pygame.FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode(WNDSIZE, 0, 32)
                fullscreen = not fullscreen
            if event.key == pygame.K_k:
                # game started
                if started == True:
                    FirstJump = True
    key = pygame.key.get_pressed()
    if scense == 1:
        DrawStart()
    elif scense == 2:
        rocketcount+=1
        DrawGame()
    #restart game
    if man.death==True:
        if key[pygame.K_r]:
            scense=1
            land_points = [0, land_y, WNDSIZE[0], land_y]
            started=False
            FirstJump=False
            rocketcount=0
            score=0
            Map = pygame.sprite.Group()
            man = role()
            rocket = None
            spike = spikes()
            spike.Move((0, WNDSIZE[1]))
            tetrises = [tetris((0, 100), (-300, -200), 0, 100), tetris((100, 200), (-200, -100), 0, 200),
                        tetris((200, 300), (-100, 0), 0, 300),
                        tetris((300, 400), (-400, -300), 0, 400), tetris((400, 500), (-800, -700), 0, 500),
                        tetris((500, 600), (-600, -500), 0, 600),
                        tetris((600, 700), (-700, -700), 0, 700), tetris((700, 800), (-500, -400), 0, 250),
                        tetris((800, 900), (-900, -800), 0, 450)]
    pygame.display.flip()
    # pygame.time.delay(30)

'''
    基本框架完毕
    俄罗斯方块的位置随机算法需要改进（总是出现由于距离而根本无法跳上去的情况）
'''
