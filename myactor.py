import pygame
import sys, os

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


class myActor(pygame.sprite.Sprite):
    grav = 6#2.9
    maxVelX = 70
    maxVelY = 35
    velDamp = .1
    accDamp = .35
    accDefault = 3
    groundAcc = 8.4
    airAcc = 5
    left, right, up, down, onGround = False, False, False, False, True
    def __init__(self, acc):
        pygame.sprite.Sprite.__init__(self)
        x, y = acc
        self.pos = [x,y]
        self.vel = [0.0,0.0]
        self.acc = [0.0, 0.0]
        self.jumpAcc = [0.0, 0.0]
        self.theta = 0.0
        self.dtheta = 0.0

        self.image = load_image(os.path.join("player_frames", "hobo-still.png"))
        self.rect = self.image.get_rect()
        self.initialpos = self.rect.center = self.pos

        self.jumpHeight = 0

        self.facingRight = True
        #Rects - left top width height
        self.exterior = pygame.Rect(0, 0, 128, 128)
        self.footprint = pygame.Rect(48, 96, 32, 16)
        self.hitbox = pygame.Rect(48, 48, 32, 64)

    def setLocation(self, pos):
        print 'setLoc'
        x,y = pos
        self.pos = [x,y]
        self.vel = [0,0]
        self.rect.center = self.pos

    def leftPress(self):
        print 'Left'
        if self.onGround: self.acc[0] = -myActor.groundAcc
        else: self.acc[0] = -myActor.airAcc

        if False == self.right:
            self.facingRight = False

    def rightPress(self):
        print 'Right'
        if self.onGround: self.acc[0] = myActor.groundAcc
        else: self.acc[0] = myActor.airAcc

        if False == self.left:
            self.facingRight = True

    def upPress(self):
        print 'Up'
        if self.onGround: self.acc[1] = myActor.groundAcc
        else: self.acc[1] = myActor.airAcc

    def downPress(self):
        print 'Down'
        if self.onGround: self.acc[1] = myActor.groundAcc
        else: self.acc[1] = myActor.airAcc

    def reset(self):
        self.pos = self.initialpos
        self.rect.center = self.pos

    def update(self, offset=[0.0, 0.0]):
        #self.pos = [a+b+myActor.velDamp*c for a,b,c in zip(self.pos, offset, self.vel)]
        self.pos = [a+b for a,b in zip(self.pos, offset)]
        #On above line: self.pos = [a +b + Actor.velDamp*c for a, b, c in zip(stuff)]
        #if abs(self.vel[0]) > myActor.maxVel and self.acc[0]*self.vel[0] > 0:
        #    self.acc[0] = 0

        #self.vel = [a[0]+myActor.accDamp*a[1] for a in zip(self.vel, self.acc)]

        #if not (self.left or self.right):
        #    if (self.onGround):
        #        self.acc[0] = -.2*self.vel[0]
        #    else:
        #        self.acc[0] = -.12*self.vel[0]

        #if not (self.up or self.down):
        #    if (self.onGround):
        #        self.acc[1] = -.2*self.vel[1]
        #    else:
        #        self.acc[1] = -.12*self.vel[1]

        self.rect.center = self.pos
        if self.left:
            self.leftPress()
        elif self.right:
            self.rightPress()
        elif self.up:
            self.upPress()
        elif self.down:
            self.downPress()
