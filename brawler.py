###################
import pygame
import sys, os
from myplayer import myPlayer
import mapobject
from pygame.locals import *
import level
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
        self.actorsprites.update()

    def draw(self):
        #print 'Draw'
        self.sprites.clear(self.screen, self.level.background)
        things = self.sprites.draw(self.screen)
        
        if self.debug:
            #Player aspects
            pygame.draw.rect(self.screen, pygame.color.Color("green"), self.playerSprite.rect, 1)
            pygame.draw.rect(self.screen, pygame.color.Color("blue"), self.playerSprite.hitbox, 1)
            pygame.draw.rect(self.screen, pygame.color.Color("white"), self.playerSprite.footprint, 1)
            if self.playerSprite.attacking:
                pygame.draw.rect(self.screen, pygame.color.Color("red"), self.playerSprite.punchbox, 1)
            
            for mappart in self.level.mapObjects:
                pygame.draw.rect(self.screen, pygame.color.Color("yellow"), mappart.rect, 2)
        
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

        for actor in self.actorsprites:
            actor.velDamp = self.level.velDamp
            actor.accDamp = self.level.accDamp
            actor.grav = self.level.grav

#    def mapCollision(self):
#        for mappart in self.level.mapObjects:
#            if self.playerSprite.footprint.colliderect(mappart.rect):
#                print 'Collide with',mappart.rect
                #while self.playerSprite.footprint.colliderect(mappart.rect):

                

                    #print 'Still Colliding...'
                    #if self.playerSprite.footprint.right > mappart.rect.left:# > self.playerSprite.footprint.left:
                    #    print 'Collide: Right'
                    #    self.playerSprite.offset(mappart.rect.left - self.playerSprite.footprint.right, 0)
                    #    self.playerSprite.vel[0] = self.playerSprite.vel[0] * mappart.bounceFactor * - 1 #min(0, self.playerSprite.vel[0])
                    #    continue
                    #elif self.playerSprite.footprint.left < mappart.rect.right:# < self.playerSprite.footprint.right:
                    #    print 'Collide: Left'
                    #    self.playerSprite.offset(self.playerSprite.footprint.left - mappart.rect.right, 0)
                    #    self.playerSprite.vel[0] = self.playerSprite.vel[0] * mappart.bounceFactor * - 1
                    #    continue
                    #if self.playerSprite.footprint.bottom > mappart.rect.top:# > self.playerSprite.footprint.top:
                    #    print 'Collide: Bottom'
                    #    self.playerSprite.offset(0, mappart.rect.top - self.playerSprite.footprint.bottom)
                    #    self.playerSprite.vel[1] = self.playerSprite.vel[1] * mappart.bounceFactor * - 1
                    #    continue
                    #elif self.playerSprite.footprint.top < mappart.rect.bottom:# < self.playerSprite.footprint.bottom:
                    #    print 'Collide: Top'
                    #    self.playerSprite.offset(0, self.playerSprite.footprint.top - mappart.rect.bottom)
                    #    self.playerSprite.vel[1] = self.playerSprite.vel[1] * mappart.bounceFactor * - 1
                    #    continue
                    #
                    #print '---Bad Collision:',self.playerSprite.footprint,mappart.rect
                    #break

    #def damageCollissions(self):
    


        #collides = pygame.sprite.groupcollide(self.actorsprites, self.mapObjects, False, False)
        #for actor in collides:
        #    for mappart in collides[actor]:
        #        while pygame.sprite.collide_rect(actor, mappart):
        #            if actor.rect.bottom > mappart.rect.top > actor.rect.top:
        #                actor.offset(0,-1)
        #                actor.vel[1] = 0
        #            if actor.rect.top < mappart.rect.bottom < actor.rect.bottom:
        #                actor.offset(0,1)
        #                actor.vel[1] = 0
        #            if actor.rect.right > mappart.rect.left > actor.rect.left:
        #                actor.offset(-1,0)
        #                actor.vel[0] = 0
        #            if actor.rect.left < mappart.rect.right < actor.rect.right:
        #                actor.offset(1,0)
        #                actor.vel[0] = 0

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

            #self.mapCollision()
            for actor in self.actorsprites:
                actor.mapCollide(self.level.mapObjects)
            
            self.update()
            self.draw()
            #if pygame.sprite.spritecollideany(self.playerSprite, self.mapObjects):
            #    print 'Collision'
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
        self.sprites = pygame.sprite.OrderedUpdates()
        self.actorsprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemyProjectiles = pygame.sprite.Group()
        self.playerSprite = myPlayer((200,450))
        self.actorsprites.add(self.playerSprite)
        self.sprites.add(self.playerSprite)

        self.levelInit()


if __name__ == '__main__':
    brawler = BrawlerGame()
    brawler.mainLoop()
