#sprite
import pygame
import random
import os

BLACK = (0,0,0)
GREEN = (0,255,0)
RED= (255,0,0)
YELLOW = (0,255,255)
FPS=60
WIDTH = 500
HEIGHT = 600
WHITE= (255,255,255)
# initialize the game and great the window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("my first game")
clock = pygame.time.Clock()

#add picture
background_img = pygame.image.load(os.path.join("img","background.png")).convert()
player_img = pygame.image.load(os.path.join("img","player.png")).convert()
bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

expl_anim = {}
expl_anim['lg'] =[]
expl_anim['sm'] =[]
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30,30)))
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)
power_imgs ={}
power_imgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert()

#add sound
shoot_sound = pygame.mixer.Sound (os.path.join("sound","shoot.wav"))
gun_sound = pygame.mixer.Sound (os.path.join("sound","pow0.wav"))
shield_sound = pygame.mixer.Sound (os.path.join("sound","pow1.wav"))
die_sound = pygame.mixer.Sound (os.path.join("sound","rumble.ogg"))
expl_sounds=[pygame.mixer.Sound (os.path.join("sound","expl0.wav")),
             pygame.mixer.Sound (os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load (os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.3)

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame. font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius =20 
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        #self.rect.x=WIDTH/2
        #self.rect.y=HEIGHT/2
        self.rect.bottom = HEIGHT 
        self.speedx = 8
        self.speedy = 5
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now =pygame.time.get_ticks()
        if self.gun >1 and now - self.gun_time >5000:
            self.gun =1
            self.gun_time = now

        if self.hidden and now - self.hide_time >1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2

            self.rect.bottom = HEIGHT 
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect. bottom >HEIGHT :
            self.rect.bottom = HEIGHT
        if self.rect.top <0:
            self.rect.top = 0

    def shoot(self):
        if self.gun ==1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        elif self.gun ==2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)   
            bullets.add(bullet1)
            bullets.add(bullet2)
            shoot_sound.play()
        elif self.gun >=3:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            bullet3 = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)      
            bullets.add(bullet1)  
            bullets.add(bullet2)
            bullets.add(bullet3)
            shoot_sound.play()
    
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center =(WIDTH/2, HEIGHT+500)
    
    def gunup(self):
        self.gun +=1
        self.gun_time = pygame.time.get_ticks()

def new_rock():
    r= Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp<0 :
        hp =0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGHT
    outline_rect = pygame.Rect(x,y,BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect( x,y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE, outline_rect, 2)

def draw_lives(surf,lives, img, x , y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i
        img_rect.y = y
        surf.blit(img,img_rect)
                   
def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen, ' Zero\'s first game', 64, WIDTH/2, HEIGHT /4)            
    draw_text(screen, '-> <- up down' , 22, WIDTH/2, HEIGHT /2)
    draw_text(screen, 'press any key to start' , 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                pygame.quit()
                return True
            if event.type ==pygame.KEYUP:
                waiting = False
                return False
                
                 


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice( rock_imgs)  
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.8 /2)  
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)    
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 5 ) 
        self.speedx = random.randrange(-3,  3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3) 
                               

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree%360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top>HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10


        

    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame =0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50


        

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame +=1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.speedy = 3


        

    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT:
            self.kill()


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score =0 
pygame.mixer.music.play(-1)


# game while
show_init = True

running = True


while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False



    clock.tick(FPS)
    # get the input
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
        elif event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #update the game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random() >0.95:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        new_rock()
        player.health -=hit.radius
        if player.health <= 0:
            die = Explosion(player.rect.center,'player')
            all_sprites.add(die)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()
            #running = False

    hits = pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type == 'shield':
            player.health +=20
            if player.health >100: 
                player.health = 100
            shield_sound.play()
        
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    if player.lives ==0:
        show_init = True
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score =0 

    #display
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen,player.health, 5,10)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100 , 15 )
    pygame.display.update()

running = False