###################
import pygame
import sys, os
import player as p
import camera as c
from pygame.locals import *
from sprites import SpriteStripAnim

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


def load_image(file_name, colorkey=False, image_directory='images'):
    'Loads an image, file_name, from image_directory, for use in pygame'
    file = os.path.join(image_directory, file_name)
    _image = pygame.image.load(file)
    if colorkey:
        if colorkey == -1:
        # If the color key is -1, set it to color of upper left corner
            colorkey = _image.get_at((0, 0))
        _image.set_colorkey(colorkey)
        _image = _image.convert()
    else: # If there is no colorkey, preserve the image's alpha per pixel.
        _image = _image.convert_alpha()
    return _image

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

class overlay(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.pos = [width/2,height/2]
        self.image = load_image('overlay.png')
        self.image = pygame.transform.scale(self.image, (width-40, height-40))
        self.rect = self.image.get_rect()
        self.initialpos = self.rect.center = self.pos

class BrawlerGame():
    width = 1024
    height = 576

    def __init__(self):
        # some initialization, creates the window, loads the background
        pygame.init()
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height))

        self.overlay = overlay(self.width,self.height)

        self.sprites = pygame.sprite.OrderedUpdates()
        self.actorsprites = pygame.sprite.Group()
        self.jump = False
        self.attack = False
        self.ticks = 0

        self.camera = c.Camera(self.width, self.height)
        self.playerSprite = p.Player((200,450))
        self.actorsprites.add(self.playerSprite)

        # need to load some enemies somewhere

        self.sprites.add(self.playerSprite)


    def update(self):
        #off = self.camera.update(self.playerSprite.pos)
        self.actorsprites.update()

    def draw(self):
        #print 'Draw'
        self.sprites.clear(self.screen, self.background)
        things = self.sprites.draw(self.screen)
        pygame.display.update(things)
        pygame.display.flip()

    def levelInit(self):
        print 'Level Init'
        self.background = load_image('brawler-arena-mockup.jpg') #pygame.image.load(os.path.join('images', 'map01.png')).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.screen.blit(self.background, [0,0])

        # This is kind of ugly
        self.backWall = pygame.Rect(0, 0, self.width, self.height-250)
        return True

    def mainLoop(self):
        self.levelInit()
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

            self.update()
            self.draw()
            #if pygame.sprite.spritecollideany(self.exitSprite, self.actorsprites):
            #    i+=1
            #    break;
            #elif self.playerSprite.vel[1] > 250:
            #    if self.recording: self.stopRecording()
            #    self.resetLevel()
            #    break;
            self.timer.tick(60)




    def pause(self):
        print 'Paused';
        self.sprites.add(self.overlay)
        while True:
        # game paused
            self.draw()
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        print 'Exiting';
                        sys.exit()
                    elif e.key == K_RETURN:
                        print 'Resume';
                        self.sprites.remove(self.overlay)
                        #self.draw()
                        return True



if __name__ == '__main__':
    redo = BrawlerGame()
    redo.mainLoop()
