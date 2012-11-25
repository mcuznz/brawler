###################
import pygame
import sys, os
from myplayer import myPlayer
import mapobject
from pygame.locals import *
import level
from sprites import SpriteStripAnim
import enemy

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
    debug = True
    #debug = False

    def __init__(self):
        # some initialization, creates the window, loads the background
        pygame.init()
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('ULTRA HOBO SPACE FIGHT')

        self.overlay = overlay(self.width,self.height)
        self.reload()

    def update(self):
        self.actorsprites.update(self.level.mapObjects)
        
        layers = len(self.actorsprites)
        yValues = []
        
        for actor in self.actorsprites:
            yValues.append(actor.footprint.bottom)
        
        yValues = sorted(yValues)
        
        for i in range(len(yValues)):
            for actor in self.actorsprites:
                if actor.footprint.bottom == yValues[i]:
                    self.sprites.change_layer(actor, i)
        

    def draw(self):
        #print 'Draw'
        self.sprites.clear(self.screen, self.level.background)
        things = self.sprites.draw(self.screen)
        
        if self.debug:
            #Player aspects
            pygame.draw.rect(self.screen, pygame.color.Color("green"), self.playerSprite.rect, 1)
            pygame.draw.rect(self.screen, pygame.color.Color("blue"), self.playerSprite.hitbox, 1)
            pygame.draw.rect(self.screen, pygame.color.Color("white"), self.playerSprite.footprint, 1)
            pygame.draw.rect(self.screen, pygame.color.Color("red"), self.playerSprite.shadow.rect, 1)
            if self.playerSprite.attacking:
                pygame.draw.rect(self.screen, pygame.color.Color("red"), self.playerSprite.punchbox, 1)
            
            for mappart in self.level.mapObjects:
                pygame.draw.rect(self.screen, pygame.color.Color("yellow"), mappart.rect, 2)
                
            for baddie in self.enemies:
                pygame.draw.rect(self.screen, pygame.color.Color("green"), baddie.rect, 1)
                pygame.draw.rect(self.screen, pygame.color.Color("blue"), baddie.hitbox, 1)
                pygame.draw.rect(self.screen, pygame.color.Color("white"), baddie.footprint, 1)
                pygame.draw.rect(self.screen, pygame.color.Color("red"), baddie.shadow.rect, 1)
        
        pygame.display.update(things)
        pygame.display.flip()

    def levelInit(self):
        print 'Level Init'
        # should have some sort of parameter
        self.level = level.level(1, self.width, self.height)

        self.screen.blit(self.level.background, [0,0])
        self.playerSprite.setLocation(self.level.playerStart)

        self.playerSprite.speedMultiplier = 1.0
        self.playerSprite.gravMultiplier = 1.0

        for baddie in self.level.enemies:
            self.enemies.add(baddie)
            self.actorsprites.add(baddie)

        for actor in self.actorsprites:
            actor.velDamp = self.level.velDamp
            actor.accDamp = self.level.accDamp
            actor.grav = self.level.grav



    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        self.pause()
                    if event.key == K_w or event.key == K_UP:
                        self.playerSprite.up = True
                    if event.key == K_s or event.key == K_DOWN:
                        self.playerSprite.down = True
                    if event.key == K_a or event.key == K_LEFT:
                        self.playerSprite.left = True
                    if event.key == K_d or event.key == K_RIGHT:
                        self.playerSprite.right = True
                    if event.key == K_SPACE:
                        self.playerSprite.jump()
                    if event.key == K_f:
                        self.playerSprite.attack()
                        
                elif event.type == pygame.KEYUP:
                    if event.key == K_a or event.key == K_LEFT:
                        self.playerSprite.left = False
                    if event.key == K_d or event.key == K_RIGHT:
                        self.playerSprite.right = False
                    if event.key == K_w or event.key == K_UP:
                        self.playerSprite.up = False
                    if event.key == K_s or event.key == K_DOWN:
                        self.playerSprite.down = False

            self.update()
            self.draw()
            self.timer.tick(60)

    def pause(self):
        print 'Paused';
        self.sprites.add(self.overlay)
        self.sprites.move_to_front(self.overlay)
        while True:
        # game paused
            self.draw()
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE or e.key == K_q:
                        print 'Exiting';
                        sys.exit()
                    if e.key == K_r:
                        print 'Reloading';
                        self.reload()
                        self.sprites.remove(self.overlay)
                        return True
                    elif e.key == K_RETURN:
                        print 'Resume';
                        self.sprites.remove(self.overlay)
                        return True

    def reload(self):
        self.sprites = pygame.sprite.LayeredUpdates()
        
        self.actorsprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemyProjectiles = pygame.sprite.Group()
        
        self.playerSprite = myPlayer((200,450))
        self.actorsprites.add(self.playerSprite)
        
        self.sprites.add(self.playerSprite.shadow)
        self.sprites.add(self.playerSprite)
        
        self.levelInit()
        
        for baddie in self.enemies:
            self.sprites.add(baddie.shadow)
            self.sprites.add(baddie)
            self.sprites.change_layer(baddie.shadow, -1)

        self.sprites.change_layer(self.playerSprite.shadow, -1)


if __name__ == '__main__':
    brawler = BrawlerGame()
    brawler.mainLoop()
