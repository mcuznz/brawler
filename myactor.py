import pygame
import sys, os
from sprites import SpriteStripAnim

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
    maxVelX = 70
    maxVelY = 35
    velDamp = .1
    accDamp = .35
    groundAcc = 8.4
    airAcc = 5

    footprintOffset = [48, 96]
    footprintSize = [32, 16]
    hitboxOffset = [48, 48]
    hitboxSize = [32, 64]
    # two different punchbox Offsets because he could be facing right or left
    punchboxOffsets = [[64,64],[0,64]]
    punchboxSize = [64,48]

    left, right, up, down = False, False, False, False
    onGround, walking, facingRight = True, False, True

    attacking = False
    attackFrames = 12
    currentAttackFrame = 0
    
    # these control how fast the hobo goes up.. and how fast he comes down
    jumpVelStart = 20
    grav = 1.1

    jumpVel = 0.0
    jumpHeight = 0.0
    jumpDelta = 0.0

    minWalkVel = 3

    def __init__(self, acc):
        pygame.sprite.Sprite.__init__(self)
        x, y = acc
        self.pos = [x,y]
        self.vel = [0.0,0.0]
        self.acc = [0.0, 0.0]
        self.theta = 0.0
        self.dtheta = 0.0

        self.frameHold = 4

        self.strips = [
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-still.png"), (0,0,128,128), 1, None, True, self.frameHold, False),
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-still.png"), (0,0,128,128), 1, None, True, self.frameHold, True),
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-run-sprite03.png"), (0,0,128,128), 3, None, True, self.frameHold, False),
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-run-sprite03.png"), (0,0,128,128), 3, None, True, self.frameHold, True)
        ]
        self.whichStrip = 0
        self.strips[self.whichStrip].iter()
        self.image = self.strips[self.whichStrip].next()

        self.rect = self.image.get_rect()
        self.initialpos = self.rect.center = self.pos

        #Rects - left top width height
        #self.exterior = pygame.Rect(0, 0, 128, 128)
        self.footprint = pygame.Rect(self.rect.left + self.footprintOffset[0], self.rect.top + self.footprintOffset[1], self.footprintSize[0], self.footprintSize[1])
        self.hitbox = pygame.Rect(self.rect.left + self.hitboxOffset[0], self.rect.top + self.hitboxOffset[1], self.hitboxSize[0], self.hitboxSize[1])
        self.punchbox = pygame.Rect(self.rect.left + self.punchboxOffsets[0][0], self.rect.top + self.punchboxOffsets[0][1], self.punchboxSize[0], self.punchboxSize[1])

    def jump(self):
        if self.onGround is True:
            self.jumpVel = self.jumpVelStart
            self.onGround = False

    def attack(self):
        print 'Attack!'
        self.attacking = True
        self.currentAttackFrame = 0

    def updateRects(self):
        self.rect.center = self.pos
        self.footprint.left = self.rect.left + self.footprintOffset[0]
        self.footprint.top = self.rect.top + self.footprintOffset[1] + self.jumpHeight
        self.hitbox.left = self.rect.left + self.hitboxOffset[0]
        self.hitbox.top = self.rect.top + self.hitboxOffset[1]
        if self.facingRight:
            self.punchbox.left = self.rect.left + self.punchboxOffsets[0][0]
            self.punchbox.top = self.rect.top + self.punchboxOffsets[0][1]
        else:
            self.punchbox.left = self.rect.left + self.punchboxOffsets[1][0]
            self.punchbox.top = self.rect.top + self.punchboxOffsets[1][1]

    def setLocation(self, pos):
        print 'setLoc'
        x,y = pos
        self.pos = [x,y]
        self.vel = [0,0]
        #self.rect.center = self.pos
        self.updateRects()

    def leftPress(self):
        if self.onGround: self.acc[0] = -myActor.groundAcc
        else: self.acc[0] = -myActor.airAcc

        if False == self.right:
            self.facingRight = False

    def rightPress(self):
        if self.onGround: self.acc[0] = myActor.groundAcc
        else: self.acc[0] = myActor.airAcc

        if False == self.left:
            self.facingRight = True

    def leftAndRightPress(self):
        if self.onGround:
            self.acc[0] = -.2*self.vel[0]
        else:
            self.acc[0] = -0.12*self.vel[0]

    def upPress(self):
        if self.onGround: self.acc[1] = -myActor.groundAcc
        else: self.acc[1] = -myActor.airAcc

    def downPress(self):
        if self.onGround: self.acc[1] = myActor.groundAcc
        else: self.acc[1] = myActor.airAcc

    def upAndDownPress(self):
        if self.onGround:
            self.acc[1] = -.2*self.vel[1]
        else:
            self.acc[1] = -0.12*self.vel[1]

    def offset(self, x, y):
        self.pos = [a[0] + a[1] for a in zip(self.pos, [x,y])]
        self.updateRects()

    def reset(self):
        self.pos = self.initialpos
        self.updateRects()

    def update(self, offset=[0.0, 0.0]):
        tempJumpHeight = self.jumpHeight
        self.jumpHeight = max(self.jumpHeight + self.jumpVel, 0)
        self.jumpDelta = self.jumpHeight - tempJumpHeight
        
        self.pos[0] = self.pos[0] + offset[0] + myActor.velDamp * self.vel[0]
        self.pos[1] = self.pos[1] + offset[1] + myActor.velDamp * self.vel[1] - self.jumpDelta

        if abs(self.vel[0]) > myActor.maxVelX and self.acc[0]*self.vel[0] > 0:
            self.acc[0] = 0

        if abs(self.vel[1]) > myActor.maxVelY and self.acc[1]*self.vel[1] > 0:
            self.acc[1] = 0

        self.vel[0] = self.vel[0] + myActor.accDamp * self.acc[0]
        self.vel[1] = self.vel[1] + myActor.accDamp * self.acc[1]
        
        if self.jumpHeight == 0:
            self.jumpVel = 0
            self.onGround = True
        else:
            self.jumpVel = self.jumpVel - self.grav
        
        if (abs(self.vel[0]) > self.minWalkVel) or (abs(self.vel[1]) > self.minWalkVel*0.8) :
            self.walking = True
        else:
            self.walking = False

        if not (self.left or self.right):
            if self.onGround:
                self.acc[0] = -.2*self.vel[0]
            else:
                self.acc[0] = -.12*self.vel[0]

        if not (self.up or self.down):
            if self.onGround:
                self.acc[1] = -.2*self.vel[1]
            else:
                self.acc[1] = -.12*self.vel[1]

        self.updateRects()

        if self.attacking:
            self.currentAttackFrame = self.currentAttackFrame + 1
            if self.currentAttackFrame > self.attackFrames:
                self.currentAttackFrame = 0
                self.attacking = False

        if self.walking:
            if not self.facingRight:
                if self.whichStrip != 3:
                    self.whichStrip = 3
                    self.strips[self.whichStrip].iter()
            else:
                if self.whichStrip != 2:
                    self.whichStrip = 2
                    self.strips[self.whichStrip].iter()
        else:
            if not self.facingRight:
                if self.whichStrip != 1:
                    self.whichStrip = 1
                    self.strips[self.whichStrip].iter()
            else:
                if self.whichStrip != 0:
                    self.whichStrip = 0
                    self.strips[self.whichStrip].iter()
        
        self.image = self.strips[self.whichStrip].next()

        if self.left and self.right:
            self.leftAndRightPress()
        elif self.left:
            self.leftPress()
        elif self.right:
            self.rightPress()

        if self.up and self.down:
            self.upAndDownPress()
        elif self.up:
            self.upPress()
        elif self.down:
            self.downPress()
