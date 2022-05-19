import pygame

class SpriteSheet:
	def __init__(self, filename):
		self.spritesheet = pygame.image.load(filename).convert_alpha()
	
	def get_image(self, x, y, width, height):
		image = pygame.Surface((width, height), pygame.SRCALPHA)
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pygame.transform.scale(image, (64, 64))
		return image

class Sprite(pygame.sprite.Sprite):
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)

		self.image = image

		self.rect = self.image.get_rect()