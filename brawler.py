###################
import pygame
import sys, os
import player as p
import camera as c
from pygame.locals import *
from sprites import SpriteStripAnim

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound

#
#
#surface = pygame.display.set_mode((resolution_x,resolution_y))
#FPS = 60
#
#clock = pygame.time.Clock()
#
## set up assorted sprites - later, we should load this from XML
#background = pygame.image.load("images/map01.jpg")
#
#def pause():
#    while true:
#        # game paused
#        for e in pygame.event.get():
#            if e.type == KEYDOWN:
#                if e.key == K_ESCAPE:
#                    sys.exit()
#                elif e.key == K_RETURN:
#                    return true
#
#def walk_up():
#    return true
#def walk_down():
#    return true
#def walk_left():
#    return true
#def walk_right():
#    return true
#
#
#
#while true:
#    for e in pygame.event.get():
#        if e.type == KEYDOWN:
#            if e.key == K_ESCAPE:
#                pause()
#            elif e.key == K_RETURN:

class BrawlerGame():
    width = 1024
    height = 576

    def __init__(self):
        # some initialization, creates the window, loads the background
        pygame.init()
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height))

        self.background = pygame.image.load(os.path.join('images', 'map01.png')).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen.blit(self.background, [0,0])

        self.overlay = pygame.image.load(os.path.join('images', 'overlay.png')).convert_alpha()
        self.overlay = pygame.transform.scale(self.overlay, (self.width, self.height))

        self.sprites = pygame.sprite.OrderedUpdates()
        self.actorsprites = pygame.sprite.Group()
        self.jump = False
        self.attack = False
        self.ticks = 0

        self.camera = c.Camera(self.width, self.height)
        self.playerSprite = p.Player((500,500))
        self.actorsprites.add(self.playerSprite)

        # need to load some enemies somewhere

        self.sprites.add(self.playerSprite)


    def update(self):
        print 'Update'
        off = self.camera.update(self.playerSprite.pos)
        self.actorsprites.update(off)

    def draw(self):
        print 'Draw'
        self.sprites.clear(self.screen, self.background)
        things = self.sprites.draw(self.screen)
        pygame.display.update(things)
        pygame.display.flip()

    def levelInit(self):
        print 'Level Init'
        return true

    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause()
                    elif event.key == K_w or event.key == K_UP:
                        self.playerSprite.up = True
                    elif event.key == K_s or event.key == K_DOWN:
                        self.playerSprite.down = True
                    elif event.key == K_a or event.key == K_LEFT:
                        self.playerSprite.left = True
                    elif event.key == K_d or event.key == K_RIGHT:
                        self.playerSprite.right = True
                    #elif event.key == K_SPACE:
                        #if self.recording:
                        #    self.stopRecording()
                        #elif pygame.sprite.spritecollideany(self.playerSprite, self.recordersprites):
                        #    self.startRecording()

                elif event.type == pygame.KEYUP:
                    if event.key == K_a or event.key == K_LEFT:
                        self.playerSprite.left = False
                    elif event.key == K_d or event.key == K_RIGHT:
                        self.playerSprite.right = False
                    elif event.key == K_w or event.key == K_UP:
                        self.playerSprite.up = False
                    elif event.key == K_s or event.key == K_DOWN:
                        self.playerSprite.down = False





    def pause(self):
        print 'Paused';
        while True:
        # game paused
            self.screen.blit(self.overlay, [0,0])
            self.draw()
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        print 'Exiting';
                        sys.exit()
                    elif e.key == K_RETURN:
                        print 'Resume';
                        self.screen.blit(self.background, [0,0])
                        self.draw()
                        return True



if __name__ == '__main__':
    redo = BrawlerGame()
    redo.mainLoop()
