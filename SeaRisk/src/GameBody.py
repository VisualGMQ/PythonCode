import pygame

class GameBody:
    keys = []
    keyState = []
    mouseButton = []
    mousePos = []
    BUTTON_DOWN = 1
    BUTTON_NORMAL = 0
    BUTTON_PRESSED = 2
    BUTTON_UP = 3
    scene = -2
    oldscene = -1
    args = {}
    isChangeScene = False

    def __init__(self, size, title, bgColor, delayTime, mode = 0, icon = None):
        self.screen = pygame.display.set_mode(size, mode)
        pygame.display.set_caption(title)
        self.bgColor = bgColor
        self.isQuit = False
        self.delayTime = delayTime
        GameBody.keyState = list(pygame.key.get_pressed())
        self.__inputHandle()
        self.__loadIcon(icon)
        self.__oldActiveState = 1

    def step(self):
        self.__fillScreen()
        self.__inputHandle()
        self.__eventHandle()
        self.handleK_Esc()
        self.update()
        self.__screenUpdate()

    #change to next scene
    @staticmethod
    def nextScene():
        GameBody.scene += 1

    #will be override
    def update(self):
        pass

    def __loadIcon(self, path):
        if path:
            surface = pygame.image.load(path)
            pygame.display.set_icon(surface)

    #will override,when game lost focus will be called
    def pause(self):
        pass

    #will override,when game get focus will be called
    def resume(self):
        pass

    def __eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isQuit = True
            '''
            if event.type == pygame.ACTIVEEVENT:
                print(event.state)
                if self.__oldActiveState == 1 and event.state == 3:
                    self.pause()
                elif self.__oldActiveState == 3 and event.state == 2:
                    self.resume()
                self.__oldActiveState = event.state
            '''
    def __getKey(self):
        newkey =  pygame.key.get_pressed()
        for i in range(len(self.keys)):
            if self.keys[i] == 0 and newkey[i] == 1:
                GameBody.keyState[i] = GameBody.BUTTON_DOWN
            if self.keys[i] == 1 and newkey[i] == 1:
                GameBody.keyState[i] = GameBody.BUTTON_PRESSED
            if self.keys[i] == 1 and newkey[i] == 0:
                GameBody.keyState[i] = GameBody.BUTTON_UP
            if self.keys[i] == 0 and newkey[i] == 0:
                GameBody.keyState[i] = GameBody.BUTTON_NORMAL
        return newkey


    def __getMouseButton(self):
        return pygame.mouse.get_pressed()

    def __getMousePos(self):
        return pygame.mouse.get_pos()

    def __getMouseRel(self):
        return pygame.mouse.get_rel()

    def __setMouseVisiable(self, visiable):
        pygame.mouse.set_visible(visiable)

    def __fillScreen(self):
        self.screen.fill(self.bgColor)

    def __screenUpdate(self):
        pygame.display.update()
        pygame.time.delay(self.delayTime)

    def __inputHandle(self):
        GameBody.keys = self.__getKey()
        GameBody.mouseButton = self.__getMouseButton()
        GameBody.mousePos = self.__getMousePos()

    #can be override
    def handleK_Esc(self):
        if self.keys[pygame.K_ESCAPE]:
            self.isQuit = True