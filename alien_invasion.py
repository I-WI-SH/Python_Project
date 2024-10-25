import pygame
import pygame.display
import sys
import os

from bullet import Bullet

os.chdir("./alien_invasion")

# 游戏的相关设置
class Settings:
    def __init__(self):

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # 子弹设置
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3



class AlineInvasion:
    def __init__(self):
        # initial the game
        pygame.init()

        # 通过时钟来控制帧率
        self.clock = pygame.time.Clock()
        
        self.settings = Settings()
        
        # 初始化游戏屏幕
        self.screen = pygame.display.set_mode(size=(self.settings.screen_height,
                                                    self.settings.screen_height))
        
        # 初始化全屏游戏屏幕
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Aline Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


    
    def run_game(self):
        # game start!
        while True:
            self.__check__events()
            
            self.ship.update()
            self.__update_bullet()
            
            self.__update_screen()

            # 限制游戏只能用60帧进行
            self.clock.tick(60)
        
    def __check__events(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.__check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.__check_keyup_events(event)
                
    def __check_keydown_events(self, event):
        """响应按下键盘"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True   
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def __check_keyup_events(self, event):
        """响应释放键盘"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建子弹，并加入编组"""
        
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def __update_screen(self):
        """更新屏幕上的图像，并切换到新的屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitem()
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        pygame.display.flip()
    
    def __update_bullet(self):
        """更新子弹的位置，并且删除超出边界的子弹"""
        
        self.bullets.update()
        
        # 删除超出屏幕边缘的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        



class Ship:
    """飞船"""
    def __init__(self, game:AlineInvasion):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.ship_speed = 1.5

        

        # 加载飞船图像
        self.image = pygame.image.load("./image/ship.bmp")
        # 接收图像外接框架
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # 控制飞船右移
        self.moving_right = False

        # 控制飞船左移
        self.moving_left = False


    # 绘制飞船
    def blitem(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """控制飞船移动"""

        # 控制飞船不移动出屏幕
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ship_speed
        
        self.rect.x = self.x




if __name__ == '__main__':
    # 创建游戏实例
    ai = AlineInvasion()
    ai.run_game()