#-*-coding:utf-8-*-
# -*- coding: utf-8 -*-
import pygame
from sys import exit
from pygame.locals import *
import random

# 设置游戏屏幕大小
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/image/fire.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 5

    def move(self):
        self.rect.top -= self.speed

"""class EnemyBullet(pygame.sprite.Sprite):
	def __init__(self, bullet2_img, init_pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('resources/image/bullet.png')
		self.rect = self.image.get_rect()
		self.rect.midtop = init_pos
		self.speed = 2.5

	def move(self):
		self.rect.bottom += self.speed"""
		

# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 用来存储玩家飞机图片的列表
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
            #self.image.append(plane_img1.subsurface(player_down_imgs[i]).convert_alpha())
        self.rect = player_rect[0]                      # 初始化图片所在的矩形
        self.rect.topleft = init_pos                    # 初始化矩形的左上角坐标
        self.speed = 8                                  # 初始化玩家飞机速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group()            # 玩家飞机所发射的子弹的集合
        self.img_index = 0                              # 玩家飞机图片索引
        self.is_hit = False                             # 玩家是否被击中

    # 发射子弹
    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)
 

    # 向上移动，需要判断边界
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    # 向下移动，需要判断边界
    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    # 向左移动，需要判断边界
    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    # 向右移动，需要判断边界        
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 2
       self.down_index = 0 
 
    # 敌机移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed

    """def shoot(self, bullet2_img):
        bullet2 = EnemyBullet(bullet2_img, self.rect.midbottom)
        self.bullets.add(bullet2)"""

# 初始化 pygame
pygame.init()

# 设置游戏界面大小、背景图片及标题
# 游戏界面像素大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), RESIZABLE, 32)

# 游戏界面标题
pygame.display.set_caption('飞机大战')
pygame.mouse.set_visible(True)

pygame.mixer.music.load('resources/music/Tobu - Morning Energy.mp3')
pygame.mixer.music.play()

# 背景图
background = pygame.image.load('resources/image/space.png')
# Game Over 的背景图
game_over = pygame.image.load('resources/image/gameover2.png')

# 飞机及子弹图片集合
plane_img = pygame.image.load('resources/image/shoot.png')
#plane_img1 = pygame.image.load('resources/image/plane01.png')
# 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家飞机图片
#player_rect = pygame.Rect(0, 0, 152, 117)
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸图片
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
"""player_down_imgs = []
player_down_imgs.append(plane_img.subsurface(pygame.Rect(165, 234, 102, 126)))
player_down_imgs.append(plane_img.subsurface(pygame.Rect(330, 624, 102, 126)))
player_down_imgs.append(plane_img.subsurface(pygame.Rect(330, 498, 102, 126)))
player_down_imgs.append(plane_img.subsurface(pygame.Rect(432, 624, 102, 126)))"""
#player = Player(plane_img1, player_down_imgs, player_pos)
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 敌机不同状态的图片列表，多张图片展示为动画效果
#enemy1_rect = pygame.Rect(534, 612, 57, 43)
#enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_img = pygame.image.load('resources/image/enemy.png')
enemy1_rect = pygame.Rect(0, 0, 51, 50)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

# 敌机子弹图片
bullet2_rect = pygame.Rect(1004, 987, 9, 21)
bullet2_img = plane_img.subsurface(bullet2_rect)

#存储敌机，管理多个对象
enemies1 = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁动画
enemies_down = pygame.sprite.Group()

# 初始化射击及敌机移动频率
shoot_frequency = 0
enemy_frequency = 0

# 玩家飞机被击中后的效果处理
player_down_index = 16

# 初始化分数
score = 0

bomb = 1
rank = 'SSS+'

# 游戏循环帧率设置
clock = pygame.time.Clock()


# 判断游戏循环退出的参数
running = True

# 游戏主循环
while running:
    # 控制游戏最大帧率为 60
    clock.tick(60)
    # 生成子弹，需要控制发射频率
    """back = pygame.mixer.Sound('resources/music/hero_fire.wav')
    back.set_volume(0.08)
    back.play()"""

    # 首先判断玩家飞机没有被击中
    if not player.is_hit:
        if shoot_frequency % 15 == 0:
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    # 生成敌机，需要控制生成频率
    if enemy_frequency % 40  == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 4.9
    if enemy_frequency >= 100:
        enemy_frequency = 0

    
   
    	"""bullet2.move()
    	if bullet2.rect.top >0:
    		enemy.bullets.rwmove(bullet2)"""


    for bullet in player.bullets:
        # 以固定速度移动子弹
        bullet.move()
        # 移动出屏幕后删除子弹
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)   

    for enemy in enemies1:
        #2. 移动敌机
        enemy.move()
        #3. 敌机与玩家飞机碰撞效果处理
        
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            break
        #4. 移动出屏幕后删除飞机    
        if enemy.rect.top < 0:
            enemies1.remove(enemy)

    #敌机被子弹击中效果处理
    # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8
    else:
        # 玩家飞机被击中后的效果处理
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            # 击中效果处理完成后游戏结束
            running = False

    # 敌机被子弹击中效果显示
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            pass
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 100
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1
        b = pygame.mixer.Sound('resources/music/BOMB2.WAV')
        b.set_volume(2)
        b.play()
    # 显示子弹
    player.bullets.draw(screen)
    # 显示敌机
    enemies1.draw(screen)


    # 绘制得分
    score_font = pygame.font.SysFont("arial", 63)
    #print(pygame.font.get_fonts())
    score_text = score_font.render(str(score), True, (0, 255, 0))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    bomb_font = pygame.font.SysFont("arial", 40)
    score_text2 = bomb_font.render('Bomb:' + str(bomb), True, (5, 91, 186))
    #score_text3 = bomb_font.render(str(bomb), True, (80, 128, 128))
    text_rect2 = score_text.get_rect()
    #text_rect3 = score_text.get_rect()
    text_rect2.topleft = [350, 10]
    #text_rect3.topleft = [450, 10]
    screen.blit(score_text2, text_rect2)
    #screen.blit(score_text3, text_rect3)
    
    # 更新屏幕
    pygame.display.update()

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 获取键盘事件（上下左右按键）
    key_pressed = pygame.key.get_pressed()

    # 处理键盘事件（移动飞机的位置）

    if key_pressed[K_w] and key_pressed[K_a]:
        player.moveUp()
        player.moveLeft()
    if key_pressed[K_w] and key_pressed[K_d]:
        player.moveUp()
        player.moveRight()
    if key_pressed[K_s] and key_pressed[K_a]:
        player.moveDown()
        player.moveLeft()
    if key_pressed[K_s] and key_pressed[K_d]:
        player.moveDown()
        player.moveRight()
    if key_pressed[K_w] or key_pressed[K_UP]:
        player.moveUp()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        player.moveDown()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        player.moveLeft()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        player.moveRight()
    if key_pressed[K_o]:
        if bomb != 0:
            bomb = bomb-1
            score += 200
            for enemy in enemies1:
            #for a in range(0,30):
            	enemies1.remove(enemy)
            
    if key_pressed[K_j]:
    	player.moveLeft()
    	player.moveLeft()
    	player.moveLeft()
    	player.moveLeft()
    	player.moveLeft()
    if key_pressed[K_l]:
    	player.moveRight()
    	player.moveRight()
    	player.moveRight()
    	player.moveRight()
    	player.moveRight()
    if key_pressed[K_m]:
    	player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            # 击中效果处理完成后游戏结束
            running = False
    if key_pressed[K_ESCAPE]:
        exit()
#    if key_pressed[K_r]:
        #  	self.image = pygame.image.load('resources/image/bullet.png')

# 游戏 Game Over 后显示最终得分
font = pygame.font.SysFont("arial", 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
if score <= 500:
    rank = 'D'
elif score <= 1800:
	rank = 'C'
elif score <= 4000:
	rank = 'B'
elif score <= 7000:
	rank = 'A'
elif score <= 11000:
	rank = 'S'
elif score <= 17000:
	rank = 'SS'
elif score <= 22000:
	rank = 'SSS'
text2 = font.render('Rank: '+ str(rank), True, (255, 0, 0))
text3 = font.render('Wonderful !!', True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
#text2_rect = text2.get_rect
screen.blit(game_over, (0,0))
screen.blit(text, text_rect)
screen.blit(text2, (160,450))
if score >22000:
    screen.blit(text3, (140,550))

pygame.display.update()

# 显示得分并处理游戏退出
while 1:	
    for event in pygame.event.get():   	
    	key_pressed = pygame.key.get_pressed()
    	if key_pressed[K_ESCAPE]:
            exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
pygame.display.update()