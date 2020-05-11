import pygame

class Ball(pygame.sprite.Sprite):
	def __init__(self, size):
		super().__init__()
		self.image = pygame.image.load('image/ball.jpg').convert_alpha()
		self.size = size
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = (self.size[0] - self.rect.width) // 2, self.size[1] - 5 - self.rect.height - 19
		self.mask = pygame.mask.from_surface(self.image)
		self.speed = 10
		self.x_speed = 7
		self.y_speed = -7

	def reset(self):
		self.rect.left, self.rect.top = (self.size[0] - self.rect.width) // 2, self.size[1] - 5 - self.rect.height - 19
		self.y_speed = -7
		self.x_speed = 7

	def autoMove(self):
		if self.rect.left <= 0:
			self.x_speed *= -1
		elif self.rect.right >= self.size[0]:
			self.x_speed *= -1
		
		if self.rect.top <= 0:
			self.y_speed *= -1

		self.rect.left += self.x_speed
		self.rect.top += self.y_speed

	def moveLeft(self, flag):
		if flag:
			self.rect.left -= self.speed

	def moveRight(self, flag):
		if flag:
			self.rect.left += self.speed