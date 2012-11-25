import pygame
import sys, os

class mapobject(pygame.sprite.Sprite):
    def __init__(self, startPos, affect = False, bounce = 0):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(startPos)
        self.onlyAffectPlayer = affect
        self.bounceFactor = max(bounce, 0)
