from src.scene import *
from src.role import *
from src.font import *
import src.constants
from src.fish import *
from src.obstacle import *
from src.mines import *
from src.GameBody import GameBody
from src.garbage import *
import math

#the welcom scene
class WelcomeScene(Scene):
    def __init__(self):
        Scene.__init__(self, src.constants.SCREEN_SIZE)
        self.diver = GameBody.args['diver']
        self.fish = simpleFish('/fishes1/1.png', animation([frame('/fishes1/1.png'), frame('/fishes1/2.png'), frame('/fishes1/3.png'), frame('/fishes1/4.png'), frame('/fishes1/5.png'),
                                                            frame('/fishes1/6.png'), frame('/fishes1/7.png'), frame('/fishes1/8.png'), frame('/fishes1/9.png'), frame('/fishes1/10.png')]))
        self.titleImage = load_imageOnly('/UI/title.png', (255,255,255,255))
        self.flowTick = 0
        self.isChangeScene = False
        self.sceneAni = welcomeBGScene()
        self.onInit()
    def onInit(self):
        self.moveTo(0, 0)
        self.diver.isShow(True)
        self.diver.moveTo(700, 350)
        self.fish.moveTo(0, 500)
        self.fish.isShow(True)
        self.flowTick = 0
        self.isChangeScene = False
        self.sceneAni.moveTo(0, 0)
        self.sceneAni.isShow(True)
        load_bgm('bgm1.mp3')
    def drawWelcome(self):
        titlerect = self.titleImage.get_rect()
        titlerect.x = (src.constants.SCREEN_SIZE[0] - titlerect.w)//2
        titlerect.y = 50
        self.canva.blit(self.titleImage, titlerect)
        #pygame.draw.line(self.canva, (0, 0, 0), (0, 400), (src.constants.SCREEN_SIZE[0], 400))
        #self.canva.blit(load_imageOnly('ship.png'), (600, 350 + int(5 * math.sin(self.flowTick))))
    def drawSawtooth(self, x, y):
        pygame.draw.line(self.canva, (0, 0, 0), (x, y), (x+10, y-10))
        pygame.draw.line(self.canva, (0, 0, 0), (x+10, y-10), (x + 20, y))
    def update(self, dst):
        self.canva.fill(src.constants.BG_COLOR)

        self.sceneAni.update(self.canva)
        self.playBGM()

        self.drawWelcome()
        self.flowTick += 0.1
        #print("isChangeScene",GameBody.isChangeScene)
        if not GameBody.isChangeScene:
            self.fish.move(0, int(2 * math.sin(self.flowTick)))
            text = object(createSentence(u"按下空格开始游戏", 40, fontInfo()), "")
            text.moveTo(450, 600)
            text.isShow(True)
            text.update(self.canva)
            self.canva.blit(text.image, text.rect.topleft)

        self.fish.update(self.canva)
        #blit to screen
        dst.blit(self.canva, self.rect.topleft)
        #the condition to change scene


#the main game scene
class gameScene(Scene):
    def __init__(self):
        Scene.__init__(self, (1200, 4600))
        self.diver = GameBody.args['diver']
        #正式的关卡布局
        self.spritGroup = pygame.sprite.Group()
        self.fuguWall = []
        self.simpleFishes = []

        self.jellys = [jellyfish(), jellyfish(), jellyfish()]

        self.assassion = assassion()

        sFish1 = simpleFish('/fishes2/1.png', animation(
            [frame('/fishes2/1.png'), frame('/fishes2/2.png'), frame('/fishes2/3.png'), frame('/fishes2/4.png'),
             frame('/fishes2/5.png'),
             frame('/fishes2/6.png'), frame('/fishes2/7.png'), frame('/fishes2/8.png'), frame('/fishes2/9.png'),
             frame('/fishes2/10.png')]))
        sFish2 = simpleFish('/fishes1/1.png', animation([frame('/fishes1/1.png'), frame('/fishes1/2.png'), frame('/fishes1/3.png'), frame('/fishes1/4.png'), frame('/fishes1/5.png'),
                                                        frame('/fishes1/6.png'), frame('/fishes1/7.png'), frame('/fishes1/8.png'), frame('/fishes1/9.png'), frame('/fishes1/10.png')]))
        sFish3 = simpleFish('/fishes3/1.png', animation(
            [frame('/fishes3/1.png'), frame('/fishes3/2.png'), frame('/fishes3/3.png'), frame('/fishes3/4.png'),
             frame('/fishes3/5.png'),
             frame('/fishes3/6.png'), frame('/fishes3/7.png'), frame('/fishes3/8.png'), frame('/fishes3/9.png'),
             frame('/fishes3/10.png')]))
        self.simpleFishes.append(sFish1)
        self.simpleFishes.append(sFish2)
        self.simpleFishes.append(sFish3)

        self.mines = []
        mine1 = mine('/mines/mine1.png', "紫水晶", NON_RENEWABLE)
        mine2 = mine('/mines/mine2.png', "红水晶", NON_RENEWABLE)
        mine3 = mine('/mines/mine3.png', "蓝矿石", NON_RENEWABLE)
        self.mines.append(mine1)
        self.mines.append(mine2)
        self.mines.append(mine3)

        self.lowestSharks = [shark(), shark(), shark()]
        self.middleSharks = [shark(), shark(), shark(), shark()]
        self.middleFugus = [fugu(), fugu(), fugu(), fugu(), fugu(), fugu()]

        self.garbages = [garbage('/garbage/garbage1.png'), garbage('/garbage/garbage2.png'), garbage('/garbage/garbage3.png')]
        self.sceneAni = normalBGScene()
        self.onInit()
        self.isMoving = False
        self.spritGroup.add(self.fuguWall + self.simpleFishes)
        self.spritGroup.add(self.assassion)
        self.spritGroup.add(self.mines)
        self.spritGroup.add(self.lowestSharks)
        self.spritGroup.add(self.jellys)
        self.spritGroup.add(self.middleFugus)
        self.spritGroup.add(self.middleSharks)
        self.spritGroup.add(self.garbages)
    def onInit(self):
        self.sceneAni.isShow(True)
        self.moveTo(0, src.constants.SCREEN_SIZE[1])
        self.diver.setState('stand')

        self.assassion.moveTo(300, 4300)
        self.assassion.isShow(True)

        self.simpleFishes[0].moveTo(400, 200)
        self.simpleFishes[1].moveTo(700, 1500)
        self.simpleFishes[2].moveTo(0, 2500)
        for i in self.simpleFishes:
            i.isShow(True)

        for i in range(8):
            ele = fugu()
            ele.moveTo(i*120, 3200)
            ele.isShow(True)
            self.fuguWall.append(ele)

        self.mines[0].moveTo(100, 4400)
        self.mines[1].moveTo(600, 4250)
        self.mines[2].moveTo(900, 4300)
        for ele in self.mines:
            ele.isShow(True)


        self.lowestSharks[0].moveTo(0, 3600)
        self.lowestSharks[1].moveTo(1000, 4000)
        self.lowestSharks[2].moveTo(400, 4300)
        for ele in self.lowestSharks:
            ele.isShow(True)

        self.jellys[0].moveTo(300, 1000)
        self.jellys[1].moveTo(900, 2000)
        self.jellys[2].moveTo(450, 3000)
        for ele in self.jellys:
            ele.isShow(True)

        self.middleFugus[0].moveTo(0, 1600)
        self.middleFugus[1].moveTo(500, 2000)
        self.middleFugus[2].moveTo(900, 3000)
        self.middleFugus[3].moveTo(200, 3250)
        self.middleFugus[4].moveTo(700, 3400)
        self.middleFugus[5].moveTo(600, 2300)
        for ele in self.middleFugus:
            ele.isShow(True)

        self.middleSharks[0].moveTo(0, 2800)
        self.middleSharks[1].moveTo(400, 2400)
        self.middleSharks[2].moveTo(600, 3600)
        self.middleSharks[3].moveTo(1000, 1000)
        for ele in self.middleSharks:
            ele.isShow(True)


        self.garbages[0].moveTo(250, 1400)
        self.garbages[1].moveTo(700, 4400)
        self.garbages[2].moveTo(300, 2500)
        for ele in self.garbages:
            ele.isShow(True)
        GameBody.args['diver'].mineBar.maxnum = 3
        self.isMoving = False
    def suitToScreen(self):
        global delta
        delta = 0
        if self.diver.rect.y < src.constants.SCREEN_SIZE[1]//2:
            delta = self.diver.rect.y - src.constants.SCREEN_SIZE[1]//2
            self.move(0, -delta)
            self.isMoving = True
        if self.diver.rect.y > src.constants.SCREEN_SIZE[1]//2:
            delta = self.diver.rect.y - src.constants.SCREEN_SIZE[1]//2
            self.move(0, -delta)
            self.isMoving = True
        if self.rect.y >= 0:
            self.rect.y = 0
            self.isMoving = False
        if self.rect.y <= src.constants.SCREEN_SIZE[1] - self.rect.h:
            self.rect.y = src.constants.SCREEN_SIZE[1] - self.rect.h
            self.isMoving = False
        if self.isMoving:
            self.diver.move(0, -delta)

    def drawObjectes(self):
        #正在的布局
        # drawScene
        self.sceneAni.moveTo(0, 0)
        self.sceneAni.update(self.canva)
        #draw fuguWall
        self.spritGroup.update(self.canva)
    def diverBorderCollide(self):
        #rect = GameBody.args['diver'].rect.copy()
        #rect.y += math.fa=bs(self.rect.h)
        diver = GameBody.args['diver']
        if diver.rect.x < 0:
            diver.rect.x = 0
        if diver.rect.x + diver.rect.w > src.constants.SCREEN_SIZE[0]:
            diver.rect.x = src.constants.SCREEN_SIZE[0] - diver.rect.w
        if diver.rect.y + diver.rect.h > src.constants.SCREEN_SIZE[1]:
            diver.rect.y = src.constants.SCREEN_SIZE[1] - diver.rect.h
        if diver.rect.y < 0:
            diver.rect.y = 0
    def update(self, dst):
        self.canva.fill(src.constants.BG_COLOR)
        GameBody.args['diverLocalRect'] = pygame.Rect(self.g2l(GameBody.args['diverCollideRect'].topleft), (GameBody.args['diverCollideRect'].w, GameBody.args['diverCollideRect'].h))
        self.drawObjectes()

        #suit to screen
        if GameBody.scene == 2:
            self.suitToScreen()
            self.diverBorderCollide()

        #blit myself to screen
        dst.blit(self.canva, self.rect.topleft)

class secondScene(gameScene):
    def __init__(self):
        Scene.__init__(self, (1200, 4600))
        self.spritGroup = pygame.sprite.Group()
        self.injuredFishes = []
        self.diver = GameBody.args['diver']
        injuredfish1 = injuredFish('/blueFish/1.png', animation([frame('/blueFish/1.png'), frame('/blueFish/2.png'), frame('/blueFish/3.png'), frame('/blueFish/4.png'), frame('/blueFish/5.png'),
                                                                        frame('/blueFish/6.png'), frame('/blueFish/7.png'), frame('/blueFish/8.png'), frame('/blueFish/9.png'), frame('/blueFish/10.png')]))
        injuredfish2= injuredFish(load_imageOnly('/yellowFish/1.png', isAlpha=True, colorkey=-1), animation(
            [frame(load_imageOnly('/yellowFish/1.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/2.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/3.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/4.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/5.png', isAlpha=True, colorkey=-1)),
             frame(load_imageOnly('/yellowFish/6.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/7.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/8.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/9.png', isAlpha=True, colorkey=-1)), frame(load_imageOnly('/yellowFish/10.png', isAlpha=True, colorkey=-1))]))
        self.injuredFishes.append(injuredfish1)
        self.injuredFishes.append(injuredfish2)
        self.jellys = []
        for i in range(10):
            j = jellyfish()
            j.type = 2
            self.jellys.append(j)

        self.fugus = []
        for i in range(20):
            self.fugus.append(fugu())

        self.sharks = []
        for i in range(10):
            self.sharks.append(shark())

        self.mines = [mine('/mines/mine7.png', "钻石", NON_RENEWABLE), mine('/mines/mine8.png', "紫宝石", NON_RENEWABLE), mine('/mines/mine9.png', "红树林", RENEWABLE)]
        self.sceneAni = normalBGScene()
        self.spritGroup.add(self.injuredFishes)
        self.spritGroup.add(self.jellys)
        self.spritGroup.add(self.fugus)
        self.spritGroup.add(self.sharks)
        self.spritGroup.add(self.mines)
        self.onInit()
    def onInit(self):
        self.moveTo(0, 0)
        self.sceneAni.isShow(True)
        self.diver.onInit()
        self.diver.air.isShow(True)
        self.diver.hp.isShow(True)
        self.diver.mineBar.isShow(True)
        self.diver.isShow(True)
        self.diver.setState('swiming')
        self.diver.moveTo(600, 100)
        self.diver.mineBar.maxnum = 3
        
        self.injuredFishes[0].moveTo(0, 1000)
        self.injuredFishes[1].moveTo(0, 2500)
        for ele in self.injuredFishes:
            ele.isShow(True)

        self.jellys[0].moveTo(200, 600)
        self.jellys[1].moveTo(500, 1000)
        self.jellys[2].moveTo(700, 1200)
        self.jellys[3].moveTo(900, 1500)
        self.jellys[4].moveTo(100, 2000)
        self.jellys[5].moveTo(0, 2300)
        self.jellys[6].moveTo(600, 2700)
        self.jellys[7].moveTo(550, 3000)
        self.jellys[8].moveTo(250, 3500)
        self.jellys[9].moveTo(800, 3900)

        for ele in self.jellys:
            ele.isShow(True)

        self.fugus[0].moveTo(400, 700)
        self.fugus[1].moveTo(100, 750)
        self.fugus[2].moveTo(600, 1050)
        self.fugus[3].moveTo(800, 1400)
        self.fugus[4].moveTo(900, 130)
        self.fugus[5].moveTo(400, 2200)
        self.fugus[6].moveTo(500, 2600)
        self.fugus[7].moveTo(700, 3100)
        self.fugus[8].moveTo(600, 2900)
        self.fugus[9].moveTo(200, 3400)
        self.fugus[10].moveTo(100, 3800)
        self.fugus[11].moveTo(0, 4000)
        self.fugus[12].moveTo(1000, 4500)
        self.fugus[13].moveTo(500, 4400)
        self.fugus[14].moveTo(700, 4300)
        self.fugus[15].moveTo(300, 4300)
        self.fugus[16].moveTo(500, 4300)
        self.fugus[17].moveTo(900, 4300)
        self.fugus[18].moveTo(800, 2100)
        self.fugus[19].moveTo(600, 2100)
        for ele in self.fugus:
            ele.isShow(True)

        self.sharks[0].moveTo(0, 1200)
        self.sharks[1].moveTo(100, 2400)
        self.sharks[2].moveTo(300, 3600)
        self.sharks[3].moveTo(500, 4200)
        self.sharks[4].moveTo(100, 4300)
        self.sharks[5].moveTo(0, 1000)
        self.sharks[6].moveTo(1000, 3000)
        self.sharks[7].moveTo(90, 2800)
        self.sharks[8].moveTo(900, 4000)
        self.sharks[9].moveTo(250, 3500)
        for ele in self.sharks:
            ele.isShow(True)

        self.mines[0].moveTo(875, 4300)
        self.mines[1].moveTo(400, 4350)
        self.mines[2].moveTo(100, 4400)
        for ele in self.mines:
            ele.isShow(True)
        self.isMoving = False
    def drawObjectes(self):
        self.sceneAni.update(self.canva)
        self.spritGroup.update(self.canva)
    def update(self, dst):
        self.canva.fill(src.constants.BG_COLOR)
        self.drawObjectes()

        GameBody.args['diverLocalRect'] = pygame.Rect(self.g2l(GameBody.args['diverCollideRect'].topleft),
                                                      (GameBody.args['diverCollideRect'].w,
                                                       GameBody.args['diverCollideRect'].h))

        if GameBody.scene == 3:
            self.suitToScreen()
            self.diverBorderCollide()

        dst.blit(self.canva, self.rect.topleft)


class darkScene(gameScene):
    def __init__(self):
        Scene.__init__(self, (1200, 4600))
        self.diver = GameBody.args['diver']
        #self.block = load_imageOnly('/UI/block.jpg')
        self.sceneAni = normalBGScene()
        self.darkmask = load_imageOnly('/UI/lightCircle.png', colorkey=-1, isAlpha=True)
        self.spriteGroup = pygame.sprite.Group()
        self.mines = [mine('/mines/mine4.png', "青金石", NON_RENEWABLE), mine('/mines/mine5.png', "珊瑚", RENEWABLE),
                      mine('/mines/mine6.png', "黄石头", NON_RENEWABLE)]
        self.assassions = []
        for i in range(20):
            self.assassions.append(assassion2())

        self.fugus = []
        for i in range(10):
            self.fugus.append(fugu())
        self.lights = []
        self.spriteGroup.add(self.mines)
        self.spriteGroup.add(self.assassions)
        self.spriteGroup.add(self.fugus)
        self.onInit()
    def onInit(self):
        self.moveTo(0, 0)
        self.sceneAni.isShow(True)
        self.diver.onInit()
        self.diver.air.isShow(True)
        self.diver.hp.isShow(True)
        self.diver.mineBar.isShow(True)
        self.diver.isShow(True)
        self.diver.setState('swiming')
        self.diver.moveTo(600, 100)
        self.diver.mineBar.maxnum = 3

        self.mines[0].moveTo(200, 4400)
        self.mines[1].moveTo(400, 4400)
        self.mines[2].moveTo(800, 4400)
        for ele in self.mines:
            self.bindLight(ele)
            ele.isShow(True)

        self.assassions[0].moveTo(200, 1000)
        self.assassions[1].moveTo(300, 1100)
        self.assassions[2].moveTo(400, 1200)
        self.assassions[3].moveTo(500, 1300)
        self.assassions[4].moveTo(700, 1400)
        self.assassions[5].moveTo(100, 1500)
        self.assassions[6].moveTo(500, 1600)
        self.assassions[7].moveTo(600, 1700)
        self.assassions[8].moveTo(200, 1800)
        self.assassions[9].moveTo(600, 1900)
        self.assassions[10].moveTo(200, 2000)
        self.assassions[11].moveTo(400, 2200)
        self.assassions[12].moveTo(800, 2400)
        self.assassions[13].moveTo(1000, 2600)
        self.assassions[14].moveTo(200, 2800)
        self.assassions[15].moveTo(100, 3000)
        self.assassions[16].moveTo(500, 3700)
        self.assassions[17].moveTo(600, 3500)
        self.assassions[18].moveTo(2700, 4000)
        self.assassions[19].moveTo(1200, 4200)

        for ele in self.assassions:
            pos = list(ele.rect.topright)
            pos[0] -= 25
            pos[1] += 40
            self.bindLight(ele, pos)
            ele.isShow(True)

        self.fugus[0].moveTo(600, 400)
        self.fugus[1].moveTo(0, 600)
        self.fugus[2].moveTo(300, 800)
        self.fugus[3].moveTo(900, 1200)
        self.fugus[5].moveTo(200, 2000)
        self.fugus[6].moveTo(300, 3200)
        self.fugus[7].moveTo(100, 4200)
        self.fugus[8].moveTo(0, 1600)
        self.fugus[9].moveTo(340, 2500)

        for ele in self.fugus:
            ele.isShow(True)

        load_bgm('bgm2.mp3')
        self.isMoving = False
    def drawObjectes(self):
        self.sceneAni.moveTo(0, 0)
        self.sceneAni.update(self.canva)
        self.spriteGroup.update(self.canva)
    def bindLight(self, obj, pos=None):
        l = light(obj)
        if pos == None:
            l.rect.center = obj.rect.center
        else:
            l.rect.center = pos
        self.lights.append(l)
    def drawMask(self, dst):
        surface = pygame.Surface(self.rect.size)
        surface.fill((0, 0, 0))
        pygame.draw.circle(surface, (255,255,255,255), GameBody.args['diverLocalRect'].center, 200)
        rect = self.darkmask.get_rect()
        rect.center = GameBody.args['diverLocalRect'].center
        dst.blit(self.darkmask, rect)
        surface.set_colorkey(pygame.Color(255, 255, 255, 255))
        dst.blit(surface, (0, 0))
    def update(self, dst):
        self.canva.fill(src.constants.BG_COLOR)
        self.playBGM()

        GameBody.args['diverLocalRect'] = pygame.Rect(self.g2l(GameBody.args['diverCollideRect'].topleft),
                                                      (GameBody.args['diverCollideRect'].w, GameBody.args['diverCollideRect'].h))
        self.drawObjectes()
        if GameBody.scene == 4:
            self.suitToScreen()
            self.diverBorderCollide()

        self.drawMask(self.canva)
        for l in self.lights:
            l.update(self.canva)
        dst.blit(self.canva, self.rect.topleft)


class gameOver(Scene):
    def __init__(self):
        Scene.__init__(self, src.constants.SCREEN_SIZE)
        self.text = load_imageOnly('/UI/gameOver.png', colorkey=-1, isAlpha=True)
        self.bgImage = load_imageOnly('/UI/overScene.png', colorkey=-1)
    def onInit(self):
        pass
    def drawGameOver(self, dst):
        dst.blit(self.bgImage, (0, 0))
        dst.blit(self.text, ((self.rect.w-self.text.get_width())//2, (self.rect.h - self.text.get_height())//2))
        #drawText(dst, "GameOver", 50, (400, 200), fontInfo((255 ,0 ,0), isBold=True))
        drawText(dst, "按下R键重新开始", 30, (500, 600), fontInfo((0, 0, 0), isBold=True))
    def update(self, dst):
        self.canva.fill(src.constants.BG_COLOR)
        GameBody.args['diverLocalRect'] = pygame.Rect(self.g2l(GameBody.args['diverCollideRect'].topleft),
                                                      (GameBody.args['diverCollideRect'].w,
                                                       GameBody.args['diverCollideRect'].h))

        self.drawGameOver(dst)