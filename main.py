import pygame, sys, os
import numpy as np
from pygame.locals import *

import brick
import broad
import ball

# 设置窗口打开位置
os.environ['SDL_VIDEO_WINDOW_POS'] = "300, 100"

# 初始化
pygame.init()
pygame.mixer.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("打砖块 (AD/←→:控制;  Q:音乐;  E:更换背景;  R:重新开始;)")
font = pygame.font.Font('font/font.ttf', 24)
FPS = 30
brick_pos = [100, 50]

# 加载音乐
pygame.mixer.music.load('sound/bg.ogg')
pygame.mixer.music.set_volume(0.5)

# 背景加载
bg_image = [
	pygame.image.load('image/stage1.jpg').convert_alpha(),
	pygame.image.load('image/stage2.jpg').convert_alpha(),
	pygame.image.load('image/stage3.jpg').convert_alpha()
]

# 创建精灵组
brick_group = pygame.sprite.Group()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BULE = (0, 0, 125)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def add_brick(content):
	for line in content:
		for each in line:
			bricks = brick.Brick(size)
			bricks.position(brick_pos[0], brick_pos[1])
			if each == 1:
				bricks.life = 1
				bricks.image = bricks.images[bricks.life - 1]
				bricks.score = 10
				brick_group.add(bricks)
			elif each == 2:
				bricks.life = 2
				bricks.image = bricks.images[bricks.life - 1]
				bricks.score = 30
				brick_group.add(bricks)
			elif each == 3:
				bricks.life = 3
				bricks.image = bricks.images[bricks.life - 1]
				bricks.score = 50
				brick_group.add(bricks)
			brick_pos[0] += 50
		brick_pos[0] = 100
		brick_pos[1] += 25
	brick_pos[1] = 50

def print_text(font, x, y, text, color = WHITE):
	ti = font.render(text, True, color)
	screen.blit(ti, (x, y))

# 碰撞检测
def change_ball_speed(rect1, rect2):
	flag = [1, 1]
	if (rect2.left > rect1.right) or (rect2.right < rect1.left):
		flag[0] = -1
	else :
		flag[1] = -1
	return flag

def main():
	# pygame.mixer.music.play(-1)
	clock = pygame.time.Clock()
	# 创建玩家和球
	player = broad.Broad(size)
	myball = ball.Ball(size)
	# 随机创建砖块组并添加到精灵组, (行,列)
	content = np.random.randint(0, 4, (14, 12))
	add_brick(content)
	# 背景索引
	Bg_index = 0
	# 分数
	score = 0
	score_flag = 0
	# 音乐播放暂停
	sound = True
	# 小球自动移动控制
	running = False
	
	while True:
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				elif event.key == K_q:
					sound = not sound
				elif event.key == K_e:
					Bg_index = (Bg_index + 1) % 3
				elif event.key == K_r:
					brick_group.empty()
					main()
				elif event.key == K_SPACE:
					running = True
					myball.active = False
		
		keys = pygame.key.get_pressed()
		if keys[K_LEFT] or keys[K_a]:
			flag = player.moveLeft()
			if not running:
				myball.moveLeft(flag)
		elif keys[K_RIGHT] or keys[K_d]:
			flag = player.moveRight()
			if not running:
				myball.moveRight(flag)

		if score - score_flag > 300:
			score_flag = score
			myball.x_speed += (1 if myball.x_speed > 0 else -1)
			myball.y_speed += (1 if myball.y_speed > 0 else -1)
		
		if running:
			myball.autoMove()
			# 玩家小球碰撞检测, 精灵和精灵碰撞检测
			if pygame.sprite.collide_mask(myball, player):
				# print(pygame.sprite.collide_mask(myball, player))
				# print(pygame.sprite.collide_mask(player, myball))
				myball.y_speed *= -1
			elif myball.rect.bottom > h:
				myball.reset()
				player.reset()
				running = False
			# 小球和砖块碰撞检测, 精灵与精灵组碰撞检测
			hit = pygame.sprite.spritecollideany(myball, brick_group)
			# pygame.image.save(screen,'11.jpg')
			if hit:
				hit.life -= 1
				if hit.life == 0:
					score += hit.score
					brick_group.remove(hit)
				else:
					hit.image = hit.images[hit.life - 1]
					speed_flag = change_ball_speed(hit.rect, myball.rect)
					myball.x_speed *= speed_flag[0]
					myball.y_speed *= speed_flag[1]
					
		if not brick_group:
			content = np.random.randint(0, 4, (14, 12))
			add_brick(content)

		# 背景绘制
		screen.blit(pygame.transform.scale(bg_image[Bg_index], (1066, 600)), (-133, 0))
		# 声音控制及绘制
		if sound:
			pygame.mixer.music.unpause()
			print_text(font, 610, 0, "Sound: On")
		else:
			pygame.mixer.music.pause()
			print_text(font, 610, 0, "Sound: Off")
		# 分数绘制
		print_text(font, 50, 0, "Score: " + str(score))
		# 砖块组,小球,玩家绘制
		brick_group.draw(screen)
		screen.blit(player.image, player.rect)
		screen.blit(myball.image, myball.rect)
		
		pygame.display.update()
		clock.tick(FPS)

if __name__ == '__main__':
	main()