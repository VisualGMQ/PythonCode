import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('1.mp3')
    pygame.mixer.music.play()
    sound1 = pygame.mixer.Sound('2.wav')
    sound1.play()
    while pygame.mixer.music.get_busy():
        pass