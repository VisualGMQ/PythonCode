import src.GameBody
from src.font import *

class testBody(src.GameBody.GameBody):
    def __init__(self):
        src.GameBody.GameBody.__init__(self, (500, 500), 'testFont', (255, 255, 255), 30)

    def update(self):
        drawText(self.screen, 'this is a text', 20, pygame.Rect(0, 0, 300, 200), fontInfo())
        drawText(self.screen, 'this is a bold text', 20, pygame.Rect(0, 50, 300, 200), fontInfo(isBold=True))
        drawText(self.screen, 'this is a italic text', 20, pygame.Rect(0, 100, 300, 200), fontInfo(isItalic=True))
        drawText(self.screen, 'this is a underline text', 20, pygame.Rect(0, 150, 300, 200), fontInfo(isUnderline=True))
        drawText(self.screen, 'this is a red text', 20, pygame.Rect(0, 200, 300, 200), fontInfo(color=(255, 0, 0)))
        drawText(self.screen, 'this is a text has bgColor', 20, pygame.Rect(0, 250, 300, 200), fontInfo(bgColor=(0,255,0)))
        drawText(self.screen, u'这里是中文', 20, pygame.Rect(0, 300, 300, 200), fontInfo())

if __name__ == '__main__':
    pygame.init()

    body = testBody()
    while not body.isQuit:
        body.step()

    pygame.quit()
