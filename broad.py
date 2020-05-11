import pygame

class Broad(pygame.sprite.Sprite):
	def __init__(self, size):
		super().__init__()
		self.image = pygame.image.load('image/broad.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.size = size
		self.rect.left, self.rect.top = (self.size[0] - self.rect.width) // 2, self.size[1] - self.rect.height - 5
		self.mask = pygame.mask.from_surface(self.image)
		self.speed = 10
		self.active = True

	def moveLeft(self):
		if self.rect.left > 0:
			self.rect.left -= self.speed
			return True
		else:
			self.rect.left = 0
			return False

	def moveRight(self):
		if self.rect.right < self.size[0]:
			self.rect.left += self.speed
			return True
		else:
			self.rect.right = self.size[0]
			return False

	def reset(self):
		self.rect.left, self.rect.top = (self.size[0] - self.rect.width) // 2, self.size[1] - self.rect.height - 5
		self.active = True