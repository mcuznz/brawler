import pygame
import sys, os
from sprites import SpriteStripAnim
import math
#import mapobject

class enemyHopper(pygame.sprite.Sprite):

	grav = 1
	scale = 1.0

	scaler = math.floor(192*scale / 192)

	footprintOffset = [math.floor(12*scaler), math.floor(128*scaler)]
	footprintSize = [math.floor(168*scaler), math.floor(40*scaler)]
	hitboxOffset = [math.floor(12*scaler), math.floor(48*scaler)]
	hitboxSize = [math.floor(168*scaler), math.floor(120*scaler)]
	shadowOffset = [math.floor(-12*scaler), math.floor(-16*scaler)]
	shadowSize = [math.floor(192*scaler), math.floor(96*scaler)]

	jumpVelStart = 16
	jumpVel = 0.0
	jumpHeight = 0.0
	jumpDelta = 0.0

	accel = [10, 6]
	
	health = 100.0
	maxHealth = 100.0
	
	damageOnCollide = True
	damage = 15

	def setScale(self, newscale):
		print 'scaling to',newscale
		self.scale = newscale
		self.scaler = 192*self.scale / 192
		
		print self.scale, self.scaler
		
		oldWidth = self.rect.width
		oldHeight = self.rect.height
		
		self.rect.width = math.floor(192*self.scaler)
		self.rect.height = math.floor(192*self.scaler)
		
		print self.rect
		
		self.rect.left = self.rect.left + math.floor((oldWidth - self.rect.width) /2)
		self.rect.top = self.rect.top + math.floor((oldHeight - self.rect.height) /2)
		
		self.footprintOffset = [math.ceil(12*self.scaler), math.ceil(128*self.scaler)]
		self.footprintSize = [math.floor(168*self.scaler), math.floor(40*self.scaler)]

		self.footprint = pygame.Rect(self.rect.left + self.footprintOffset[0], self.rect.top + self.footprintOffset[1], self.footprintSize[0], self.footprintSize[1])

		self.hitboxOffset = [math.ceil(12*self.scaler), math.ceil(48*self.scaler)]
		self.hitboxSize = [math.floor(168*self.scaler), math.floor(120*self.scaler)]

		self.hitbox = pygame.Rect(self.rect.left + self.hitboxOffset[0], self.rect.top + self.hitboxOffset[1], self.hitboxSize[0], self.hitboxSize[1])

		self.shadowOffset = [math.ceil(-12*self.scaler), math.ceil(-16*self.scaler)]
		self.shadowSize = [math.floor(192*self.scaler), math.floor(96*self.scaler)]

		self.image = pygame.transform.smoothscale(self.sourceImage, (int(self.rect.width), int(self.rect.height)))
		self.shadow.image = pygame.transform.smoothscale(self.shadow.sourceImage, (int(self.shadowSize[0]), int(self.shadowSize[1])))
		self.shadow.rect = pygame.Rect(self.footprint.left + self.shadowOffset[0], self.footprint.top + self.shadowOffset[1], self.shadowSize[0], self.shadowSize[1])

		self.footprintCheck.left = self.footprint.left - 1024
		self.footprintCheck.top = self.footprint.top
		self.footprintCheck.height = self.footprint.height
		
		# should probably modify jump height and accel as well

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

	def __init__(self, acc, scale = 1.0):
		pygame.sprite.Sprite.__init__(self)
		x, y = acc
		self.pos = [x,y]
		
		self.sourceImage = self.load_image(os.path.join("player_frames", "cube-192.png"));
		self.image = self.sourceImage
		
		self.rect = self.image.get_rect()
		self.initialpos = self.rect.center = self.pos
		
		self.footprint = pygame.Rect(self.rect.left + self.footprintOffset[0], self.rect.top + self.footprintOffset[1], self.footprintSize[0], self.footprintSize[1])
		self.hitbox = pygame.Rect(self.rect.left + self.hitboxOffset[0], self.rect.top + self.hitboxOffset[1], self.hitboxSize[0], self.hitboxSize[1])

		self.footprintCheck = pygame.Rect(self.footprint.left - 1024, self.rect.top + self.footprintOffset[1], 2048 + self.footprint.width, self.footprintSize[1])

		self.shadow = pygame.sprite.Sprite()
		self.shadow.sourceImage = self.load_image(os.path.join("player_frames", "shadow-large.png"))
		self.shadow.image = self.shadow.sourceImage
		self.shadow.image = pygame.transform.smoothscale(self.shadow.image, (int(self.shadowSize[0]), int(self.shadowSize[1])))
		self.shadow.rect = self.shadow.image.get_rect()
		self.shadow.rect.left = self.footprint.left + self.shadowOffset[0]
		self.shadow.rect.top = self.footprint.top + self.shadowOffset[1]
		
		self.setScale(scale)

	def takeHit(self, damage):
		self.health = self.health - damage
		if self.health <= 0:
			print "It's dead!"
			self.shadow.kill()
			self.kill()
		else:
			self.setScale(self.health / self.maxHealth)

	def update(self, mapData):
		pass
