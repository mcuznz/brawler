import pygame
import sys, os

class mapobject(pygame.sprite.Sprite):
    def __init__(self, startPos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(startPos)

