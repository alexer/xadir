import os, sys, time
import pygame
from pygame.locals import *
from helpers import *

if not pygame.font: print "Warning: Fonts not enabled"
if not pygame.mixer: print "Warning: Audio not enabled"

SIZE = int(sys.argv[1])

class PyManMain:
	# Main class for initialization and mechanics of the game

	def __init__(self, width=1200, height=720):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))

	def MainLoop(self):
		self.LoadSprites();
		while 1:
			self.map_sprites.draw(self.screen)
			self.player_sprites.draw(self.screen)
                	pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			time.sleep(0.05)

	def LoadSprites(self):
    		"""Load the sprites that we need"""
		w = 'w'
		l = 'l'
		self.map = Map([
				[w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w],
				[w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w,w],
                                [w,w,w,w,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l],
                                [w,w,w,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l],
                                [w,w,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l],
                                [w,w,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l],
                                [w,w,l,l,l,l,l,l,l,l,l,w,w,w,w,w,w,w,l,l],
                                [w,w,l,l,l,l,l,l,l,l,w,w,w,w,w,w,w,w,w,l],
                                [w,w,l,l,l,l,l,l,l,w,w,w,l,l,l,l,l,w,w,w],
                                [w,w,l,l,l,l,l,l,l,w,w,w,l,l,l,l,l,w,w,w],
                                [w,w,l,l,l,l,l,l,l,l,w,w,w,l,l,l,w,w,w,w],
                                [w,w,l,l,l,l,l,l,l,l,l,w,w,w,w,w,w,w,w,w],
                                [w,w,l,l,l,l,l,l,l,l,l,l,l,l,w,w,w,w,w,l],
                                [w,w,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l],
                                [w,w,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l,l],
				], 20, 15)
		self.player1 = Player([
					['b', 4, 3]
				])
		self.map_sprites = self.map.getSprites()
		self.player_sprites = self.player1.getSprites()

class Map:
	# Map class to create the background layer, holds any static and dynamical elements in the field.
	
	def __init__(self, map, height, width):
		self.sprite = [] 
                self.width = width
                self.height = height
		self.map = map
		self.map_sprites = pygame.sprite.Group()
		for x in range(self.width):
			for y in range(self.height):
				if map[x][y] == 'w':
					print "Water at: (" + str(x) + "," + str(y) + ")"
					self.map_sprites.add(Water(pygame.Rect(y*SIZE, x*SIZE, SIZE, SIZE)))
				elif map[x][y] == 'l':
					print "Land at: (" + str(x) + "," + str(y) + ")"
					self.map_sprites.add(Land(pygame.Rect(y*SIZE, x*SIZE, SIZE, SIZE)))
	def getSprites(self):
		return self.map_sprites

class Player:
	# Class to create player or team in the game. One player may have many characters.

	def __init__(self, coords):
		self.sprite = [] 
		self.coords = coords
		self.player_sprites = pygame.sprite.Group()
		self.player_characters = []
		for i in range(len(coords)):
			if coords[i][0] == 'b':
				x = coords[i][1]
				y = coords[i][2]
				print "Player1, ball sprite at: (" + str(x) + "," + str(y) + ")"
				self.player_sprites.add(Water(pygame.Rect(y*SIZE, x*SIZE, SIZE, SIZE)))
				self.player_characters.append([Character(2, [x, y], 90)])
	def getSprites(self):
		return self.map_sprites

class Character:
	# Universal class for any character in the game

	def __init__(self, movement, coords, heading):
		self.movement = movement	# Movement points left
		self.coords = coords 		# Array of x and y
		self.heading = heading		# Angle from north in degrees, possible values are: 0, 45, 90, 135, 180, 225, 270 and 315
	
	def getCoords():			# Returns coordinates of the character, return is array [x, y]
		return self.coords
	
	def setCoords(coords):			# Sets coordinates of characte, input is array of [x, y]
		self.coords = coords

	def getHeading():			# Returns heading of character in degrees
		return self.heading

	def setHeading(angle):			# Sets the absolute heading of character
		self.heading = angle

	def turn(angle):			# Turns character given amount, relative to previous heading. For now only turns 90-degrees at a time
		angle = angle % 360
		if angle <= 45:
			self.heading = (self.heading + angle) % 360
		elif angle <= 90:
			self.heading = (self.heading + angle) % 360
		elif angle <= 135:
			self.heading = (self.heading + angle) % 360

	def moveForward(steps):		# Moves to headed direction given amount of steps
		if self.movement <= steps:
			if self.heading == 0:
				self.coords[1] -= steps
			elif self.heading == 90:
				self.coords[0] += steps
			elif self.heading == 180:
				self.coords[1] += steps
			elif self.heading == 270:
				self.coords[0] -= steps
	
	def getMovementGrid():			# Return grid of available cells to move to
		 

# Following classes define the graphical elements, or Sprites.

class Land(pygame.sprite.Sprite):
        
    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image('land24.jpg', None, SIZE/24)
        if rect != None:
            self.rect = rect

class Water(pygame.sprite.Sprite):

    def __init__(self, rect=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('water24.jpg', None, SIZE/24)
        if rect != None:
            self.rect = rect

class Ball(pygame.sprite.Sprite):

   def __init__(self, rect=None):
	pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('player.png', None, SIZE/24)
        if rect != None:
            self.rect = rect

# Main starts here

if __name__ == "__main__":
	MainWindow = PyManMain()
	MainWindow.MainLoop()
