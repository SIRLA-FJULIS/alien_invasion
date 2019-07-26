import pygame
import time

aliens = []
bullets = []

magazine = [4] #彈匣
score = [0] #分數
last_shoot = [pygame.time.get_ticks()] #擊發的時間

BLACK = (0,0,0)
WHITE = (225,225,225)

class Settings():
    #初始設定
    def __init__(self):
        self.screen_width=900
        self.screen_height=600
        self.bg_color = (1,42,111)

        self.BLACK = (0,0,0)
        self.WHITE = (225,225,225)

class Ship():
    def __init__(self, ai_settings, screen):
        #設置飛船的初始位置
        self.screen = screen
        self.ai_settings = ai_settings
        
        self.image = pygame.image.load('ship.png')#載入飛船圖像
        self.rect = self.image.get_rect()#取得他的矩形
        self.screen_rect = screen.get_rect()#取得畫面的矩形

        self.rect.centerx = self.screen_rect.centerx #飛船的中間值x = 畫面的中間值x
        self.rect.bottom = self.screen_rect.bottom #飛船的y值 = 螢幕的底部y值
 
        #将飛船的属性center中存成小數
        self.center=float(self.rect.centerx)
 
        #移動標誌
        self.moving_right = False
        self.moving_left = False
    def update(self) :
        #根據移動調整飛船的位置
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.center += 1.5
        if self.moving_left and self.rect.left > self.screen_rect.left :
            self.center -= 1.5 
        self.rect.centerx = self.center
    def blitme(self): 
        self.screen.blit(self.image, self.rect)

class Alien():
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('alien.png')#載入圖片
        self.rect = self.image.get_rect()#取得外星人的矩形
        self.rect.centerx = 0#設定中間值x
        self.rect.bottom = 64 #設定底部y
        self.speed_x = 1
        self.speed_y = 64 #設定速度

        self.x= self.rect.centerx
        self.y= self.rect.bottom
    def update(self):
        self.x =  self.x + self.speed_x  #使外星人向右跑
        if self.x + 91 > 900:#如果超出邊界，則往下一行出現
            self.x = 0
            self.y =  self.y + self.speed_y
        #更新外星人的rect位置
        self.rect.centerx = self.x
        self.rect.bottom = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Bullet():
    def __init__(self, ai_settings, screen, ship):
        self.screen = screen
        self.ai_settings = ai_settings

        #在（0,0）處創建一個表示子彈的矩形，再設置正确的位置
        self.rect = pygame.Rect(0,0,10,15)
        self.rect.centerx=ship.rect.centerx
        self.rect.top = ship.rect.top

        #用小數來標示子彈的位置
        self.y= self.rect.y
        self.color = WHITE
        self.speed_factor = 1
    def update(self):
        #子彈向上移動，更新小數
        self.y -= self.speed_factor
        #更新表示子彈的rect的位置
        self.rect.y = self.y 

    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect)

def draw_text(text, size, color, x, y,screen): #文字輸出
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def update_screen(ai_settings, screen, ship, bullets, alien, aliens) :
    #每次循環時更新畫面
    screen.fill(ai_settings.bg_color)

    #在飛船和外星人后面重新繪製所有子彈
    for bullet in bullets: 
        bullet.draw()
    ship.blitme()

    for alien in aliens:
        alien.draw()

    for bullet in bullets:
        for alien in aliens:
            if collision_check(bullet, alien): #如果碰撞的話
                aliens.remove(alien)
                bullets.remove(bullet)
                score[0] = score[0] + 10

    draw_text("magazine*" + str(magazine[0]), 40, WHITE, 100, 20,screen) #子彈剩餘數目

    # 讓最近繪製的屏幕可見
    pygame.display.flip()

def collision_check(object_A, object_B):
    #碰撞檢查
    return(object_A.rect.colliderect(object_B.rect)) #判斷兩個rect是否有碰撞

def check_keydown_events(event, ai_settings, screen, ship, bullets, last_shoot) :
    #按鍵按下
    if event.key == pygame.K_RIGHT :
        ship.moving_right =True
    elif event.key == pygame.K_LEFT :
         ship.moving_left =True
    elif event.key == pygame.K_SPACE :
        if magazine[0] > 0: #如果有子彈的話
            new_bullet = Bullet(ai_settings,screen,ship)
            bullets.append(new_bullet)
            magazine[0] = magazine[0] - 1
 
def check_keyup_events(event,ship) :
    #按鍵放開
    if event.key == pygame.K_RIGHT:
         ship.moving_right = False
    elif event.key == pygame.K_LEFT :
         ship.moving_left =False
 
def check_events(ai_settings,screen,ship,bullets):
    #按鍵相關
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            quitgame()
        elif event.type == pygame.KEYDOWN :
            check_keydown_events(event, ai_settings, screen, ship,bullets, last_shoot)
        elif event.type == pygame.KEYUP :
            check_keyup_events(event, ship)


def game_intro(): #開始畫面
    pygame.init()
    ai_settings=Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    image = pygame.image.load('game_intro.png')
    screen.blit(image, (0,0))
    aliens.clear()
    bullets.clear()
    magazine[0] = 4 #彈匣
    score[0] = 0 #分數
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                quitgame()
            elif event.type == pygame.KEYDOWN : #如果按下空白鍵即可開始遊戲
                if event.key == pygame.K_SPACE :
                    run_game()
        draw_text("Press space to start game", 40, BLACK, 450, 400, screen)
        pygame.display.flip()

def run_game():#遊戲進行
    pygame.init()
    ai_settings=Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings,screen)
    alien = Alien(ai_settings,screen)
    game_time = pygame.time.get_ticks()

    #開始遊戲
    while True:
        # 查看事件
        check_events(ai_settings, screen, ship, bullets) #確定按鍵是否有被使用
        ship.update() #載入飛船

        if pygame.time.get_ticks() % 500 == 0: #每500毫秒產生一個新的外星人
            aliens.append(Alien(ai_settings, screen))

        for alien in aliens:
            alien.update() #載入外星人
            if alien.rect.bottom >= 600:  #如果外星人到達底線，則消失
                aliens.remove(alien)  #移除外星人
                score[0] = score[0] - 5

        for bullet in bullets:
            bullet.update() #載入子彈
        
        shoot = pygame.time.get_ticks()
        if shoot - last_shoot[0] > 2000 and magazine[0] < 4: #每過2秒補充一子彈
            magazine[0] = magazine[0] + 1
            last_shoot[0] = shoot

        update_screen(ai_settings, screen, ship, bullets, alien, aliens) #更新畫面
        if pygame.time.get_ticks() - game_time > 10000: #100秒後遊戲結束
            time_up(screen)
            break

def time_up(screen): #遊戲時間到
    image = pygame.image.load('time_up.png')
    screen.blit(image, (0,0))
    draw_text("score:" + str(score[0]), 100, BLACK, 450, 330, screen)
    pygame.display.flip()
    time.sleep(3)
    game_intro()

def quitgame(): #離開遊戲
    pygame.quit()
    quit()

game_intro()