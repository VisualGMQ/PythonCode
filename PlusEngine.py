import pygame
import os
import re
import platform
import math
import math
import sys

__author__ = "Visual GMQ"
if __name__ == '__main__':
    print("This is a GameEngine to simplify classes in Pygame")

'''
    这个ImageEntrepot类是用来存储从外部载入的图像资源的，必须用在窗体创建之前。因为载入图片的函数里有convert函数
    该函数必须在窗体创建后才能使用
        构造函数：
            默认构造函数：初始化图片列表__image，初始化相对路径为本程序的路径
            __init__(path)：用来初始化相对路径
            __init__(dir[,keycolor])：在初始化的同时将路径path（相对路径）下的所有.bmp,.jpg,.gif,.png图片读取并保存。他们
                的key是图片本身的名称（不带后缀）.keycolor是关键色，默认为白色不透明
        InsertImage(path,key=""):
            加入图片。如果key不传值，则为加入的图片本身名称
            成功返回图片的Surface
            失败返回None
        SetPath(absolutepath):
            改变path，必须传入绝对路径
            返回path
        GetPath()：
            返回path
        FindImage(key):
            根据key找到图片
            成功返回图片surface
            失败返回None
        SetKeycolor(color):
            静态方法，设置关键色
        GetKeycolor():
            静态方法，获得关键色
        OutputItems:
            用于调试，输出图像列表里的所有item  
        关于关键色的说明：
            我们只指定一种keycolor而用于所有的图片。如果需要给图片另外附上keycolor则需另外操作
'''

SysInfo=platform.system()

class ImageEntrepot:
    __keycolor = pygame.Color(255, 255, 255)

    def __init__(self):
        self.__image = {}
        self.__path = os.getcwd()

    def __init__(self, keycolor):
        self.__image = {}
        self.__path = os.getcwd()
        ImageEntrepot.__keyword = keycolor

    def __init__(self, dir, keycolor=pygame.Color(255, 255, 255)):
        ImageEntrepot.__keyword = keycolor
        self.__path = os.getcwd()
        self.__image = {}
        if SysInfo=="Windows" or SysInfo=="Vista":
            split="\\"
        else:
            split="/"
        pics = os.listdir(self.__path + split + dir)
        for i in pics:
            try:
                if ".png" in i:
                    self.__image[str(i.split(".")[0])] = pygame.image.load(
                        self.__path + split + dir + split + i).convert_alpha()
                else:
                    self.__image[str(i.split(".")[0])] = pygame.image.load(
                        self.__path + split + dir + split + i).convert()
                for pic in self.__image.values():
                    pic.set_colorkey(ImageEntrepot.GetKeycolor())
            except pygame.error:
                print("Loaded Unsuported image or Openned unexsist path or Don't have a form\nthe pic is:" + i)

    def InsertImage(self, path, key=""):
        if key == "":
            key = re.findall(r"[\\(.*?)\.[JPG|jpg|bmp|png|ico|gif]|[(.*?)\.[jpg|bmp|png|ico]", path, re.I)[-1]
        try:
            if ".png" in path or ".PNG" in path:
                pic = pygame.image.load(self.__path + "\\" + path).convert_alpha()
            else:
                pic = pygame.image.load(self.__path + "\\" + path).convert()
            pic.set_colorkey(ImageEntrepot.GetKeycolor())
            self.__image[key] = pic
        except pygame.error:
            print("Loaded Unsuported image or Not find image")
            return None
        return pic

    def SetPath(self, absolutepath):
        self.__path += absolutepath
        return self.__path

    def GetPath(self):
        return self.__path

    def FindImage(self, key):
        try:
            surface = self.__image[key].copy()
        except KeyError:
            print("No this key")
            return None
        return surface

    def OutPutItems(self):
        print(self.__image.keys())

    def __del__(self):
        pygame.quit()

    @staticmethod
    def SetKeycolor(color):
        ImageEntrepot.__keycolor = color

    @staticmethod
    def GetKeycolor():
        return ImageEntrepot.__keycolor


'''
    Form 类是用来创建游戏窗口并操纵的类
class Form:
    def __init__(self):
        screen=pygame.display.set_mode((750,600),pygame.RESIZABLE,32)
        self.__visualble=True
    def __init__(self,size=(750,600),visualble=True):
        pygame.display.set_mode(size,pygame.RESIZABLE,32)
        self.__visualble=visualble
    def IsVisual(self):
        return self.__visualble
'''

'''
    DrawTool类简单的封装了一些绘图的函数。这是一个静态类。
    Blit(dest,src,pos[,size=0][,xflip=False][,yflip=False][,angle=0]):
        综合的绘图函数。可以同时提供改变大小，水平和竖直翻转，旋转操作。也可以在省略这几个参数的情况下普通blit
    BlitOnlyFlip(dest,src,pos,xflip=False,yflip=False)
    BlitOnlyRotate(dest,src,pos,angle)
    BlitOnlyResize(dest,src,pos,size)
        这三个韩函数分别调用Blit函数来执行特定功能
'''


class DrawTool:
    @staticmethod
    def Blit(dest, src, pos, size=0, xflip=False, yflip=False, angle=0):
        if xflip == True or yflip == True:
            try:
                src = pygame.transform.flip(src, xflip, yflip)
            except:
                print("can't flip in 'Blit'")
                return None
        if not angle == 0:
            try:
                rsize = src.get_size()
                centerpoint = (pos[0] + rsize[0] // 2, pos[1] + rsize[1] // 2)
                src = pygame.transform.rotate(src, angle)
                rsize = src.get_size()
                # changedpoint=(pos[0]+src.get_size()[0]//2,pos[1]+src.get_size()[1]//2)
                pos = (centerpoint[0] - rsize[0] // 2, centerpoint[1] - rsize[1] // 2)
            except:
                print("can.t rotate in 'Blit'")
                return None
        if size == 0:
            try:
                size = src.get_size()
            except:
                print("can't resize in Blit")
                return None
        else:
            try:
                src = pygame.transform.scale(src, size)
            except:
                print("can't resize in 'Blit'")
                return None
        try:
            dest.blit(src, pos)
        except:
            print("can't blit in Blit")
            return None
        return src

    @staticmethod
    def BlitOnlyFlip(dest, src, pos, xflip=False, yflip=False):
        try:
            sur = DrawTool.Blit(dest, src, pos, 0, xflip, yflip)
        except:
            print("Can't Blit by BlitOnlyFlip")
            return None
        return sur

    @staticmethod
    def BlitOnlyRotate(dest, src, pos, angle):
        try:
            sur = DrawTool.Blit(dest, src, pos, 0, False, False, angle)
        except:
            print("can't rotate in 'BlitOnlyRotate'")
            return None
        return sur

    @staticmethod
    def BlitOnlyResize(dest, src, pos, size):
        try:
            sur = DrawTool.Blit(dest, src, pos, size)
        except:
            print("can't resizein 'BlitOnlyResize'")
            return None
        return sur

    @staticmethod
    def BlitResizeRotate(dest,src,pos,size,angle):
        try:
            sur=DrawTool.Blit(dest,src,pos,size,False,False,angle)
        except:
            print("can't resize and rotate blit\n")
            return None
        return sur
'''
    Object 用于继承的物体基类
'''


class Object:
    def __init__(self):
        self.__pos = None
        self.__size = None
        self.__image = None

    def __init__(self, size, pos, image=None):
        self.__pos = pos
        self.__size = size
        self.__image = image

    def SetImage(self, NImage):
        self.__image = NImage

    def GetImage(self):
        return self.__image

    def Move(self, npos):
        self.__pos = npos

    def Resize(self, nsize):
        self.__size = nsize

    def GetPos(self):
        return self.__pos

    def GetSize(self):
        return self.__size


'''
    Lable类用于描述字体，将字体封装成对象
'''


class Lable(Object):
    def __init__(self, text, width=15, tcolor=pygame.Color(0, 0, 0), bgcolor=pygame.Color(255, 255, 255)):
        Object.__init__(self, None, None)
        self.__pos = (0, 0)
        self.__surface = None
        self.__text = None
        self.__width = None
        self.SetCover(text, tcolor, bgcolor, width)
        self.Resize(self.__surface.get_size())
    def SetCover(self, text, tcolor, bgcolor, width):
        self.__text = text
        self.__width = width
        font = pygame.font.SysFont("Arial", width)
        if not self.__surface==None:
            pygame.draw.rect(self.__surface,self.__tcolor,pygame.Rect(self.__pos,self.__size),self.__width)
        self.__surface = font.render(self.__text, True, tcolor, bgcolor)
        pygame.draw.rect(self.__surface, tcolor,
                         pygame.Rect((0, 0), (self.__surface.get_size()[0], self.__surface.get_size()[1])), 1)

    def GetCover(self):
        return self.__surface

    def Render(self, dest):
        self.Move(self.__pos)
        DrawTool.Blit(dest, self.__surface, self.__pos)


'''
    Button类使用两个Lable类作为按下前和按下后的情况来模拟按钮（注意，构造函数传入的表面不能是你要额外用到的。不然会改变那个表面的参数)
'''

class Text(Object):
    def __init__(self,text,width=30,tcolor=pygame.Color(0,0,0)):
        Object.__init__(self,None,(0,0))
        self.__text=text
        self.__width=width
        self.__tcolor=tcolor
        self.__surface=None
        self.SetCover(text,self.__tcolor,self.__width)
    def ChangeText(self,text):
        self.SetCover(text,self.__tcolor,self.__bgcolor,self.__width)
    def GetText(self):
        return self.__text
    def ChangeWidth(self,width):
        self.__width=width
    def SetCover(self, text, tcolor, width):
        self.__text = text
        self.__width = width
        font = pygame.font.SysFont("Arial", width)
        if not self.__surface==None:
            pygame.draw.rect(self.__surface,self.__tcolor,pygame.Rect(self.__pos,self.__size),self.__width)
        self.__surface = font.render(self.__text, True, tcolor)
    def GetCover(self):
        return self.__surface
    def Render(self,dest):
        DrawTool.Blit(dest,self.__surface,self.GetPos())

class Button(Object):
    def __init__(self, Front, Back=None, Click=None, OnClick=None):
        Object.__init__(self, Front.GetSize(), (0, 0))
        if not (type(Front) == Lable):
            try:
                raise Exception
            except:
                print("Button class:Gived Wrong arguments")
        self.front = Front
        self.OnClick = OnClick
        if Back == None:
            self.back = Front
        else:
            self.back = Back
        if Click == None:
            self.click = Front
        else:
            self.click = Click

    def ChangeFront(self, text, tcolor, bgcolor, width):
        self.front.SetCover(text, tcolor, bgcolor, width)
        return self.front

    def ChangeBack(self, text, tcolor, bgcolor, width):
        self.back.SetCover(text, tcolor, bgcolor, width)
        return self.back

    def ChangeClick(self, text, tcolor, bgcolor, width):
        self.click.SetCover(text, tcolor, bgcolor, width)
        return self.click

    def Render(self, dest):
        mpos = pygame.mouse.get_pos()
        mstate = pygame.mouse.get_pressed()
        DrawTool.Blit(dest, self.front.GetCover(), self.GetPos())
        if Collision.RectPoint(pygame.Rect(self.GetPos(), self.GetSize()), mpos):
            DrawTool.Blit(dest, self.back.GetCover(), self.GetPos())
        else:
            DrawTool.Blit(dest, self.front.GetCover(), self.GetPos())
        if (mstate[1] == True or mstate[0] == True or mstate[2] == True) and not self.OnClick == None and Collision.RectPoint(pygame.Rect(self.GetPos(), self.GetSize()),mpos):
            DrawTool.Blit(dest, self.click.GetCover(), self.GetPos())
            self.OnClick()

class maptexture(pygame.sprite.Sprite):
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.rect=self.image.get_rect()
        self.mappos=None
    def SetPos(self,npos,mappos):
        self.rect.x=npos[0]
        self.rect.y=npos[1]
        self.mappos=mappos   #mappos[0] is colum mappos[1] is row
    def GetPos(self):
        return (self.rect.x,self.rect.y)
    def SetSize(self,nsize):
        self.image=pygame.transform.scale(self.image,nsize)
    def GetSize(self):
        return self.image.get_size()
    def SetRect(self,nrect):
        self.rect=nrect
    def GetRect(self):
        return self.rect
    def update(self,dest):
        DrawTool.Blit(dest,self.image,self.GetPos())

'''
    Map
'''
class Map:
    def __init__(self):
        self.file=None
        self.context=None
        self.dic={}
        self.offpos=[0,0]
        self.outsize=None   #the total map size
        self.group=pygame.sprite.Group()
        self.col_group=pygame.sprite.Group()
        self.persize=None
    def __init__(self,path,outsize,dic,col_list,picstore,offpos=[0,0]):
        self.dic={}
        self.offpos=list(offpos)
        self.col_group=pygame.sprite.Group()
        try:
              self.file=open(path,"r+")
        except Exception:
            print("can't open map\n")
        try:
            for key in dic.keys():
                 self.dic[key]=picstore.FindImage(dic[key])
        except:
            print("Finded False image in map\n")
        self.group=pygame.sprite.Group()
        self.outsize=outsize
        self.context=self.file.readlines()
        #Why there must 'len(self.context[0])-1'?,It must think.
        self.persize=(round(self.outsize[0]/(len(self.context[0])-1)),round(self.outsize[1]/len(self.context)))
        for i in range(len(self.context)):
            self.context[i]=self.context[i].split("\n")[0]
        for row in range(len(self.context)):
            for colum in range(len(self.context[0])):
                if self.context[row][colum] in self.dic.keys():
                    mapblock=maptexture(self.dic[self.context[row][colum]])
                    mapblock.SetRect(pygame.Rect((colum*self.persize[0]+self.offpos[0],row*self.persize[1]+self.offpos[1]),self.persize))
                    mapblock.SetSize(self.persize)
                    mapblock.mappos=(colum,row)
                    if self.context[row][colum] in col_list:
                        self.col_group.add(mapblock)
                    self.group.add(mapblock)
    def MoveDelta(self,offpos):
        self.offpos[0]+=offpos[0]
        self.offpos[1]+=offpos[1]
    def Move(self,newpos):
        self.offpos=newpos
    def GetPos(self):
        return self.offpos
    def OutPut(self):
        print(self.group.sprites())
        print(self.col_group.sprites())
        for i in self.group.sprites():
            print(i.GetRect())
    def update(self,dest):
        for ele in self.group:
            ele.SetRect(pygame.Rect((ele.mappos[0]*self.persize[0]+self.offpos[0],ele.mappos[1]*self.persize[1]+self.offpos[1]),self.persize))
        self.group.update(dest)
    def __del__(self):
        self.file.close()

'''
    Collision是一个静态类，用于一些碰撞检测（尽管Group已经做得很好了，但是我们仍旧需要封装以下用于我们自己的类）
'''
class Collision:
    TOP=1
    TOPRIGHT=1
    RIGHT=3
    RIGHTBOTTOM=4
    BOTTOM=5
    LEFTBOTTOM=6
    LEFT=7
    LEFTTOP=8
    @staticmethod
    def Rect2(rect1, rect2):
        if (rect1.x > rect2.x + rect2.width and rect1.y > rect2.y + rect2.height) or (
                rect1.x + rect1.width < rect2.x and rect1.y + rect1.height < rect2.y) or (
                rect1.x > rect2.x + rect2.width and rect1.y + rect1.height < rect2.y) or (
                rect1.x + rect1.width < rect2.x and rect1.y >= rect2.y + rect2.height):
            return False
        else:
            return True
    @staticmethod
    def LineSeg1D(pointlist):
        max=pointlist[0]
        min=pointlist[0]
        for i in pointlist:
            if max<i:
               max=i
        for j in pointlist:
            if min>j:
               min=j
        if abs(max-min)>(abs(pointlist[0]-pointlist[1])+abs(pointlist[2]-pointlist[3])):
            return False
        else:
            return True
    @staticmethod
    def RectPoint(rect, point):
        if point[0] >= rect.x and point[0] <= rect.width + rect.x and point[1] >= rect.y and point[
            1] <= rect.y + rect.height:
            return True
        else:
            return False
    @staticmethod
    def SpriteColMap(sprite,map_group,oldrect):
        collist=pygame.sprite.spritecollide(sprite,map_group,False)
        if len(collist)==0:
            return None,None
        else:
            for ele in collist:
                vcol = Collision.LineSeg1D([ele.GetPos()[1], ele.GetPos()[1] + ele.GetSize()[1], oldrect.y,oldrect.y + oldrect.height])
                hcol = Collision.LineSeg1D([ele.GetPos()[0], ele.GetPos()[0] + ele.GetSize()[0], oldrect.x,oldrect.x + oldrect.width])
                #if len(collist)==1:
                if hcol==True:
                    if oldrect.y+oldrect.height<=ele.GetPos()[1]:
                        return Collision.TOP,ele
                    if oldrect.y<=ele.GetPos()[1]+ele.GetSize()[1]:
                        return Collision.BOTTOM,ele
                # else:
                #     if oldsprite.GetPos()[1]<ele.GetPos()[1]+ele.GetSize()[1]:
                #         if oldsprite.GetPos()[0]>ele.GetPos()[0]+ele.GetSize()[0]:
                #             return Collision.RIGHTBOTTOM
                #         if oldsprite.GetSize()[0]+oldsprite.GetPos()[0]<ele.GetPos()[0]:
                #             return Collision.LEFTBOTTOM
                if vcol==True:
                    if oldrect.x>=ele.GetSize()[0]+ele.GetPos()[0]:
                        return Collision.RIGHT,ele
                    if oldrect.width+oldrect.x<=ele.GetPos()[0]:
                        return Collision.LEFT,ele
                if hcol==False and vcol==False:
                    if oldrect.x+oldrect.width<=ele.GetPos()[0]:
                        if oldrect.y<=ele.GetPos()[1]+ele.GetSize()[1]:
                            return Collision.LEFTBOTTOM,ele
                        if oldrect.height+oldrect.y<ele.GetPos()[0]:
                            return Collision.LEFTTOP,ele
                    if oldrect.x>=ele.GetPos()[0]+ele.GetSize()[0]:
                        if oldrect.y <= ele.GetPos()[1] + ele.GetSize()[1]:
                            return Collision.RIGHTBOTTOM,ele
                        if oldrect.height + oldrect.y <= ele.GetPos()[0]:
                            return Collision.TOPRIGHT,ele
        return None,None
    @staticmethod
    def GetPointDistance(point1,point2):
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)


class LineSeg:
    def __init__(self,point1,point2):
        self.__LineSeg=(point1,point2)
    def GetLine(self):
        return self.__LineSeg
    def SetPoint1(self,npoint1):
        self.__LineSeg=(npoint1,self.__LineSeg[1])
    def SetPoint2(self,npoint2):
        self.__LineSeg = (self.__LineSeg[0],npoint2)
    def SetLineSeg(self,npoint1,npoint2):
        self.__LineSeg=(npoint1,npoint2)

class Role(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect=None
        self.image=None
        self.onland=False
        self.direct=1
        self.speed=0
        self.oldrect=self.GetRectCopy()
    def __init__(self,image,speed,pos=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.speed=speed
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.onland=False
        self.direct=1
        self.oldrect=self.GetRectCopy()
    def GetPos(self):
        return (self.rect.x,self.rect.y)
    def GetSize(self):
        return (self.rect.width,self.rect.height)
    def MoveTo(self,npos):
        self.rect.x=npos[0]
        self.rect.y=npos[1]
    def MoveDelta(self,deltax,deltay):
        self.rect.x += deltax
        self.rect.y += deltay
    def GetRectCopy(self):
        return self.rect.copy()
    def functop(self,block):
        self.MoveTo((self.GetPos()[0],block.GetPos()[1] - self.GetSize()[1]))
    def funcleft(self,block):
        self.MoveTo((block.GetPos()[0]-self.GetSize()[0],self.GetPos()[1]))
    def funcright(self,block):
        self.MoveTo((block.GetPos()[0]+block.GetSize()[0],self.GetPos()[1]))
    def funcbottom(self,block):
        self.MoveTo((block.GetPos()[1]+block.GetSize()[1],self.GetPos()[0]))
    def IsOnLand(self,map):
        #col_list=pygame.sprite.spritecollide(self,map.col_group,False)
        col_direct,block=Collision.SpriteColMap(self,map.col_group,self.oldrect)
        if col_direct==None and block==None:
            self.onland=False
        else:
            if col_direct==Collision.Top:
                self.functop(block)
            if col_direct==Collision.LEFT:
                self.funcleft(block)
            if col_direct==Collision.RIGHT:
                self.funcright(block)
            if col_direct==Collision.BOTTOM:
                self.funcbottom(block)
    def draw(self,dest):
        DrawTool.Blit(dest,self.image,self.GetPos())
    def update(self, dest):
        self.oldrect=self.GetRectCopy()
        self.rect.width=self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        #DrawTool.Blit(dest,self.image,(self.rect.x,self.rect.y))