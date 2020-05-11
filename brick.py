import pygame

class Brick(pygame.sprite.Sprite):
	def __init__(self, size):
		super().__init__()
		# 定义砖块图片组
		# self.image1 = pygame.image.load('image/Brick1.png').convert_alpha()
		# self.image2 = pygame.image.load('image/Brick2.png').convert_alpha()
		# self.image3 = pygame.image.load('image/Brick3.png').convert_alpha()
		self.images = [
				pygame.image.load('image/Brick1.png').convert_alpha(),
				pygame.image.load('image/Brick2.png').convert_alpha(),
				pygame.image.load('image/Brick3.png').convert_alpha()
		]
		self.life = 1
		# 当前砖块图片
		self.image = self.images[self.life - 1]
		# 碰撞检测
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.score = 0


	def position(self, left, top):
		self.rect.left = left
		self.rect.top = top
