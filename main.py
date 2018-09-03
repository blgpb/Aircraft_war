import pygame
import time
import random
from pygame.locals import *
class Base(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
class BasePlane(Base):
    def __init__(self, screen_temp, x, y, image_name):
        Base.__init__(self, screen_temp, x, y, image_name)
        self.bullet_list = []  # 存储发射出去的子弹对象的引用
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():#判断子弹是否越界
                self.bullet_list.remove(bullet)#删除越界的子弹对象
class HeroAircraft(BasePlane):
    '''飞机的类'''
    def __init__(self, screen_temp):
       BasePlane.__init__(self, screen_temp, 190, 585, './feiji/hero1.png')
    def move_left(self):
        self.x -= 5
    def move_right(self):
        self.x += 5
    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))
class EnemyPlane(BasePlane):
    '''敌机的类'''
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, './feiji/enemy0.png')
        self.direction = 'right'#用来指示敌机的移动方向
    def move(self):
        if self.direction == 'right':
            self.x += 5
        elif self.direction == 'left':
            self.x -= 5
        if self.x > 480-50:
            self.direction = 'left'
        elif self.x < 0:
            self.direction = 'right'
    def fire(self):
        self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))
class BaseBullet(Base):
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+40, y-20, './feiji/bullet.png')
    def move(self):
        self.y -= 5
    def judge(self):
        if self.y < 0:
            return True
        else:
            return False
class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+25, y+40, './feiji/bullet1.png')
    def move(self):
        self.y += 5
    def judge(self):
        if self.y > 685:
            return True
        else:
            return False
def key_scan(hero_temp):
    # 获取事件,比如按下键盘
    for event in pygame.event.get():
        # 判断是否点击了退出按钮
        if event.type == QUIT:
            print('exit')
            exit()
        # 判断是否按下按键
        elif event.type == KEYDOWN:
            # 检测按键是否是left
            if event.key == K_LEFT:
                #print('left')
                hero_temp.move_left()
            # 检测按键是否是right
            elif event.key == K_RIGHT:
                #print('right')
                hero_temp.move_right()
            # 检测按键是否是空格键
            elif event.key == K_SPACE:
                #print('space')
                hero_temp.fire()
def main():
    #1.创建游戏界面的窗口
    screen = pygame.display.set_mode((480,852), 0, 32)

    #2.创建一个背景图片
    background = pygame.image.load('./feiji/background.png')

    #3. 创建一个飞机对象
    hero = HeroAircraft(screen)
    #4. 创建一个敌机
    enemyplane = EnemyPlane(screen)

    while True:
        screen.blit(background, (0, 0))
        hero.display()
        enemyplane.display()
        enemyplane.move()#调用敌机的移动方法
        pygame.display.update()
        key_scan(hero)
        random_num = random.randint(1,100)
        if random_num == 15 or random_num == 99:
            enemyplane.fire()#敌机发射子弹
        time.sleep(0.01)

if __name__ == '__main__':
    main()
