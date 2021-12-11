from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        randint(80, win_width - 80)
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()

win_width = 900 #Game scene
win_height = 700
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
window = display.set_mode((win_width, win_height))
display.set_caption("paixnidi")

ship=Player("rocket.png", 400, 600, 100, 100, 8)
monsters = sprite.Group()
lost = 0
score = 0
img_enemy = "ufo.png"
img_bullet = "bullet.png"

for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()

font.init()
font2 = font.SysFont("Arial", 36)

lose = font2.render("you lost", 1, (255,255,255))
win = font2.render("you won", 1, (255,255,255))
finish=False
game = True
clock = time.Clock()
FPS = 120

max_lost=3
goal=10
num_fire = 0
rel_time = False


while game:  #game loop
    for e in event.get():
        if e.type == QUIT:
           game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire+=1
                    ship.fire()
                    mixer.init()
                    fire_sound=mixer.Sound('fire.ogg')
                    fire_sound.play()
                if num_fire >= 10 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
    if finish!=True:
        window.blit(background,(0, 0))
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text2 = font2.render("missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text2, (10, 50))
        ship.update()
        ship.reset()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload_txt = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload_txt, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
           #this loop will repeat as many times as the number of monsters hit
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
        if sprite.spritecollide(ship,monsters,True) or lost >= max_lost:
            finish=True
            window.blit(lose,(200,200))
        if score >= goal:
            finish=True
            window.blit(win,(200,200))
        display.update()
    else:
        time.delay(3000)
        finish=False
        score=0
        lost=0
        num_fire=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
            
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        clock.tick(FPS)