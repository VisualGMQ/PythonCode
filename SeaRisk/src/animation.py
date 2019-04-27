import pygame
from src.tools import *

class frame:
    def __init__(self, image, delaytick = 1, colorKey = None):
        if type(image) == str:
            self.image = load_imageOnly(image, colorKey)
        elif type(image) == pygame.Surface:
            self.image = image
        self.delaytick = delaytick
    def flip(self, boolX, boolY):
        return frame(pygame.transform.flip(self.image, boolX, boolY), self.delaytick)

class animation(pygame.sprite.Sprite):
    def __init__(self, frames = None):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        if frames:
            self.frames = frames
        self.count = 0
        self.iterator = 0
        self.__oldStart = False
        self.__isStart = False
        self.__isLoop = False
        self.isStopped = False
        self.timecount = 0
    def flip(self, boolX, boolY):
        newFrames = []
        for i in range(len(self.frames)):
            newFrames.append(self.frames[i].flip(boolX, boolY))
        return animation(newFrames)
    def addFrame(self, frame, index = None):
        if not type(frame) == frame:
            raise Exception("not a frame")
        if not index:
            self.frames.append(frame)
        else:
            self.frames.insert(index, frame)
    def removeFrame(self, index = None):
        if len(self.frames) > 0:
            if not index:
                del self.frames[-1]
            else:
                del self.frames[index]
    def getLen(self):
        return len(self.frames)

    def setLoop(self, enable):
        self.__isLoop = enable

    #animation state
    def stop(self):
        if self.__isStart:
            self.__isStart = False
        self.count = 0
        self.iterator = 0
    def play(self):
        if not self.__isStart:
            self.__isStart = True
    def pause(self):
        if self.__isStart:
            self.__isStart = False
    def isStart(self):
        return self.__isStart
    def getCurrentFrame(self):
        return self.iterator
    def setCurrentFrame(self, index):
        self.iterator = index
    def update(self, *args):
        self.__oldStart = self.__isStart
        global image
        if self.iterator >= len(self.frames):
            image = self.frames[-1].image
        else:
            image = self.frames[self.iterator].image
        if self.__isStart:
            if self.iterator < self.getLen():
                image = self.frames[self.iterator].image
                if self.count < self.frames[self.iterator].delaytick:
                    self.count += 1
                else:
                    self.count = 0
                    self.iterator += 1
            else:
                self.count = 0
                self.iterator = 0
                if not self.__isLoop:
                    self.__isStart = False
        if self.__oldStart == True and self.__isStart == False:
            self.isStopped = True
        else:
            self.isStopped = False
        return image

