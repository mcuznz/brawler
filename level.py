import pygame
from pygame.locals import *
import sys, os
import mapobject as m

class level():
	
	# x, y values
	# Lower Values dampen velocity more harshly
	velDamp = [0.8, 0.8]
	accDamp = [0.8, 0.6]
	grav = 1.1

	mapObjects = ()
	playerStart = (100, 400)
	
	width = 1024
	height = 576
	
	background = ''

	def __init__(self, whichLevel, width, height):
		self.mapObjects = pygame.sprite.Group()

		print 'Load Level',whichLevel
		
		self.width = width
		self.height = height
		
		# this should all be loaded from an XML file.  This is a cludge
		self.background = self.load_image('brawler-arena-mockup.jpg')
		self.background = pygame.transform.scale(self.background, (self.width, self.height))

		# Back Wall
		#self.mapObjects.add(m.mapobject((0, 0, self.width, self.height-230), False, 0.1))
		# Left Side
		#self.mapObjects.add(m.mapobject((-200, 0, 190, self.height), False, 0.1))
		# Right Side
		#self.mapObjects.add(m.mapobject((self.width + 10, 0, 190, self.height), False, 0.1))
		# Bottom
		#self.mapObjects.add(m.mapobject((-100, self.height, self.width+100, 190), False, 0.1))
		# Ship Ramp
		#self.mapObjects.add(m.mapobject((self.width - 250, self.height - 230, 260, 160), True, 0.4))

		self.mapObjects.add(m.mapobject((600, 300, 150, 150), True, 0.5))
		
		self.playerStart = (125,375)

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
