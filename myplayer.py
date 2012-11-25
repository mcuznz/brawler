import pygame
import sys, os
from sprites import SpriteStripAnim
import math
#import mapobject

class myPlayer(pygame.sprite.Sprite):
    
    # these are sensible defaults that are overriden by the level
    maxVel = [10, 8]
    velDamp = [0.2, 0.2]
    accDamp = [0.2, 0.2]
    groundAcc = [1, 0.8]
    airAcc = [0.6, 0.5]
    grav = 1
    
    speedMultiplier = 1.0
    gravMultiplier = 1.0

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
    canAttack = True
    attackFrames = 12
    attackCooldownFrames = 12
    attackMinCooldown = 12
    attackCooldownRate = 0.01
    attackCooldownInc = 1
    currentAttackFrame = 0
    
    jumpVelStart = 16
    jumpVel = 0.0
    jumpHeight = 0.0
    jumpDelta = 0.0

    minWalkVel = 2
    
    damage = 15

    def __init__(self, acc):
        pygame.sprite.Sprite.__init__(self)
        x, y = acc
        self.pos = [x,y]
        self.vel = [0.0,0.0]
        self.acc = [0.0, 0.0]

        self.frameHold = 4

        self.strips = [
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-still.png"), (0,0,128,128),
                            1, None, True, self.frameHold, False),
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-still.png"), (0,0,128,128),
                            1, None, True, self.frameHold, True),
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-run-sprite03.png"), (0,0,128,128),
                            3, None, True, self.frameHold, False),
            SpriteStripAnim(os.path.join("images", "player_frames", "hobo-run-sprite03.png"), (0,0,128,128),
                            3, None, True, self.frameHold, True)
        ]
        self.whichStrip = 0
        self.strips[self.whichStrip].iter()
        self.image = self.strips[self.whichStrip].next()
        
        self.rect = self.image.get_rect()
        self.initialpos = self.rect.center = self.pos

        #Rects - left top width height
        #self.exterior = pygame.Rect(0, 0, 128, 128)
        self.footprint = pygame.Rect(self.rect.left + self.footprintOffset[0], self.rect.top + self.footprintOffset[1],
                                     self.footprintSize[0], self.footprintSize[1])
        self.hitbox = pygame.Rect(self.rect.left + self.hitboxOffset[0], self.rect.top + self.hitboxOffset[1],
                                  self.hitboxSize[0], self.hitboxSize[1])
        self.punchbox = pygame.Rect(self.rect.left + self.punchboxOffsets[0][0], self.rect.top + self.punchboxOffsets[0][1],
                                    self.punchboxSize[0], self.punchboxSize[1])
        self.footprintCheck = pygame.Rect(self.footprint.left - 1024, self.rect.top + self.footprintOffset[1],
                                          2048 + self.footprint.width, self.footprintSize[1])

        self.shadow = pygame.sprite.Sprite()
        #self.shadow.image = self.load_image(os.path.join("player_frames", "shadow.png"))
        self.shadow.image = self.load_image(os.path.join("player_frames", "shadow-large.png"))
        self.shadow.image = pygame.transform.smoothscale(self.shadow.image, (64, 32))
        self.shadow.rect = self.shadow.image.get_rect()
        self.shadow.rect.left = self.footprint.left - 16
        self.shadow.rect.top = self.footprint.top - 5

    def load_image(self, file_name, colorkey=False, image_directory='images'):
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

    def jump(self):
        if self.onGround is True:
            self.jumpVel = self.jumpVelStart
            self.onGround = False

    def attack(self):
        if self.canAttack == True:
            self.attacking = True
            self.canAttack = False
            self.attackCooldownFrames = self.attackCooldownFrames + self.attackCooldownInc

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

        self.shadow.rect.left = self.footprint.left - 16
        self.shadow.rect.top = self.footprint.top - 5
        
        self.footprintCheck.left = self.footprint.left - 1024
        self.footprintCheck.top = self.footprint.top
        
    def setLocation(self, pos):
        x,y = pos
        self.pos = [x,y]
        self.vel = [0,0]
        #self.rect.center = self.pos
        self.updateRects()

    def leftPress(self):
        if self.onGround: self.acc[0] = -self.groundAcc[0] * self.speedMultiplier
        else: self.acc[0] = -self.airAcc[0] * self.speedMultiplier

        if False == self.right:
            self.facingRight = False

    def rightPress(self):
        if self.onGround: self.acc[0] = self.groundAcc[0] * self.speedMultiplier
        else: self.acc[0] = self.airAcc[0] * self.speedMultiplier

        if False == self.left:
            self.facingRight = True

    def leftAndRightPress(self):
        if self.onGround:
            self.acc[0] = -.2*self.vel[0]
        else:
            self.acc[0] = -0.12*self.vel[0]

    def upPress(self):
        if self.onGround: self.acc[1] = -self.groundAcc[1] * self.speedMultiplier
        else: self.acc[1] = -self.airAcc[1] * self.speedMultiplier
        
    def downPress(self):
        if self.onGround: self.acc[1] = self.groundAcc[1] * self.speedMultiplier
        else: self.acc[1] = self.airAcc[1] * self.speedMultiplier

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

    def update(self, mapData):
        
        tempJumpHeight = self.jumpHeight
        tempFootprint = self.footprint
        
        self.jumpHeight = math.floor(max(self.jumpHeight + self.jumpVel, 0))
        self.jumpDelta = self.jumpHeight - tempJumpHeight
        
        self.pos[0] = self.pos[0] + self.velDamp[0] * self.vel[0]
        self.pos[1] = self.pos[1] + self.velDamp[1] * self.vel[1] - self.jumpDelta

        if abs(self.vel[0]) > (self.maxVel[0] * self.speedMultiplier) and self.acc[0]*self.vel[0] > 0:
            self.acc[0] = 0

        if abs(self.vel[1]) > (self.maxVel[1] * self.speedMultiplier) and self.acc[1]*self.vel[1] > 0:
            self.acc[1] = 0

        self.vel[0] = self.vel[0] + self.accDamp[0] * self.acc[0]
        self.vel[1] = self.vel[1] + self.accDamp[1] * self.acc[1]
        
        if self.jumpHeight == 0:
            self.jumpVel = 0
            self.onGround = True
        else:
            self.jumpVel = self.jumpVel - (self.grav * self.gravMultiplier)
        
        if (abs(self.vel[0]) > self.minWalkVel) or (abs(self.vel[1]) > self.minWalkVel) :
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
        
        # With the Rectangles Updated, test mapData for Collissions
        for block in mapData:
            if self.footprint.colliderect(block.rect):
                print "Collide with",block.rect

                distLeft = self.footprint.right - block.rect.left
                distRight = block.rect.right - self.footprint.left
                distTop = self.footprint.bottom - block.rect.top
                distBottom = block.rect.bottom - self.footprint.top

                # I feel like this could be completely refactored... but for now, it works
                if distLeft < distRight:
                    if distTop < distBottom:
                        if distLeft == distTop:
                            self.offset(distLeft*-1, distTop*-1)
                            self.vel[0] = min(abs(self.vel[0])*-1*block.bounceFactor, self.vel[0], 0)
                            self.vel[1] = min(abs(self.vel[1])*-1*block.bounceFactor, self.vel[1], 0)
                        elif distLeft < distTop:
                            self.offset(distLeft*-1, 0)
                            self.vel[0] = min(abs(self.vel[0])*-1*block.bounceFactor, self.vel[0], 0)
                        else:
                            self.offset(0, distTop*-1)
                            self.vel[1] = min(abs(self.vel[1])*-1*block.bounceFactor, self.vel[1], 0)
                    else:
                        if distLeft == distBottom:
                            self.offset(distLeft*-1, distBottom)
                            self.vel[0] = min(abs(self.vel[0])*-1*block.bounceFactor, self.vel[0], 0)
                            self.vel[1] = max(abs(self.vel[1])*block.bounceFactor, self.vel[1], 0)
                        elif distLeft < distBottom:
                            self.offset(distLeft*-1, 0)
                            self.vel[0] = min(abs(self.vel[0])*-1*block.bounceFactor, self.vel[0], 0)
                        else:
                            self.offset(0, distBottom)
                            self.vel[1] = max(abs(self.vel[1])*block.bounceFactor, self.vel[1], 0)
                else:
                    if distTop < distBottom:
                        if distRight == distTop:
                            self.offset(distRight, distTop*-1)
                            self.vel[0] = max(abs(self.vel[0])*block.bounceFactor, self.vel[0], 0)
                            self.vel[1] = min(abs(self.vel[1])*-1*block.bounceFactor, self.vel[1], 0)
                        elif distRight < distTop:
                            self.offset(distRight, 0)
                            self.vel[0] = max(abs(self.vel[0])*block.bounceFactor, self.vel[0], 0)
                        else:
                            self.offset(0, distTop*-1)
                            self.vel[1] = min(abs(self.vel[1])*-1*block.bounceFactor, self.vel[1], 0)
                    else:
                        if distRight == distBottom:
                            self.offset(distRight, distBottom)
                            self.vel[0] = max(abs(self.vel[0])*block.bounceFactor, self.vel[0], 0)
                            self.vel[1] = max(abs(self.vel[1])*block.bounceFactor, self.vel[1], 0)
                        elif distRight < distBottom:
                            self.offset(distRight, 0)
                            self.vel[0] = max(abs(self.vel[0])*block.bounceFactor, self.vel[0], 0)
                        else:
                            self.offset(0, distBottom)
                            self.vel[1] = max(abs(self.vel[1])*block.bounceFactor, self.vel[1], 0)
                        

        if self.attacking == True or self.canAttack == False:
            self.currentAttackFrame = self.currentAttackFrame + 1
            if self.currentAttackFrame > self.attackFrames:
                self.attacking = False
                if self.currentAttackFrame > (self.attackFrames + self.attackCooldownFrames):
                    self.currentAttackFrame = 0
                    self.canAttack = True

        self.attackCooldownFrames = max(self.attackMinCooldown, self.attackCooldownFrames - self.attackCooldownRate)

        #if self.walking or self.left or self.right or self.up or self.down:
        if self.left or self.right or self.up or self.down:
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
