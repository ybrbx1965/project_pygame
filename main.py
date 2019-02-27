import pygame
import random

pygame.init()
screen = pygame.display.set_mode((500, 500))

pygame.display.set_caption('Space Invaders')

pygame.font.init()
# myfont = pygame.font.SysFont('Comic Sans MS', 30)
x, y = 300, 450
width = 30
height = 30
speed = 4
cur_speed = speed
score = 0
lives = 3
sposobnost = 300
running = True
enemy_dvizh = False
n = 1
recordable = True
ultimate = 0
ultimate_time_count = 200
ulting = False
end_mus = False
bullet_speed = 10

fps = 120
left = False
right = False

f = open('record.txt','r')
record = f.read()
f.close()

pygame.mixer.music.load(random.choice(['1.mp3', '4.mp3']))
pygame.mixer.music.play()
sound1 = pygame.mixer.Sound('2.wav')
sound2 = pygame.mixer.Sound('3.wav')

clock = pygame.time.Clock()
player = pygame.image.load('images/nlo.png')

bg = pygame.image.load("images/bg.jpg")
image = pygame.image.load("images/go.jpg")
x_im,y_im = -500,500

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemy_speed = 1
anim_count = -1
animations = [pygame.image.load('images/enemy.png'), pygame.image.load('images/enemy2.png'),
              pygame.image.load('images/enemy3.png')]


# font = pygame.font.Font(None, 25)
def start():
    font = pygame.font.Font('freesansbold.ttf', 80)
    text = font.render(str("SPACE"), 1, (100, 255, 100))
    text10 = font.render(str("INVADERS"), 1, (100, 255, 100))
    font = pygame.font.Font('freesansbold.ttf', 70)
    text_aboutstart = font.render(str("Press f to start"), 1, (100, 255, 100))
    screen.blit(text, (100,0))
    screen.blit(text10, (40,80))
    screen.blit(text_aboutstart, (0,160))

start()
class snar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = bullet_speed
        bullets.add(self)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global anim_count
        anim_count += 1
        if anim_count + 1 >= 4:
            anim_count = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = animations[anim_count]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = enemy_speed
        enemies.add(self)


def draw_window():
    screen.blit(bg, (0, 0))
    screen.blit(player, (x, y))
    bullets.draw(screen)
    enemies.draw(screen)

def draw():
    font = pygame.font.Font('freesansbold.ttf', 20)
    text1 = font.render(str("Score:"+ str(score)), 1, (100, 255, 100))
    text2 = font.render(str("Lives:" + str(lives)), 1, (100, 255, 100))
    text3 = font.render(str("Record:" + str(record)), 1, (100, 255, 100))
    text7 = font.render(str("Sposobnost: " + str(sposobnost)), 1, (100, 255, 100))
    text8 = font.render(str("Ultimate " + str(int(ultimate))), 1, (100, 255, 100))
    text1_x = 0
    text1_y = 0
    text2_x = 0
    text2_y = 20
    text3_x = 0
    text3_y = 40
    text7_x = 0
    text7_y = 60
    text8_x = 0
    text8_y = 80
    screen.blit(text1, (text1_x, text1_y))
    screen.blit(text2, (text2_x, text2_y))
    screen.blit(text3, (text3_x, text3_y))
    screen.blit(text7, (text7_x, text7_y))
    screen.blit(text8, (text8_x, text8_y))

while running:
    clock.tick(fps)
    if ultimate < 100:
        ultimate += 0.01
    # text = font.render(('Score:', score), 1, (100, 255, 100))
    # screen.blit(text, (0, 0))
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, bullets, True):
            sound2.play()
            enemy.kill()
            score += 1
            if ultimate+3 <= 100:
                ultimate += 3

    for bullet in bullets:
        if bullet.rect.y < 500 and bullet.rect.y > 0:
            bullet.rect.y -= bullet.speed
        else:
            bullet.kill()

    for enemy in enemies:
        if enemy_dvizh:
            if enemy.rect.y < 500:
                enemy.rect.y += enemy.speed
            else:
                if enemy in enemies:
                    enemy.kill()
                    lives -= 1

    keys = pygame.key.get_pressed()
    if len(enemies) < 1:
        enemies.add(Enemy(random.randint(50, 450), -50))
        enemy_speed += 0.1

    if keys[pygame.K_g]:
        if keys[pygame.K_a]:
            if keys[pygame.K_m]:
                if keys[pygame.K_e]:
                    lives = 10000
                    recordable = False
                    sposobnost = 10000000000
                    ultimate = 100

    if keys[pygame.K_f]:
        score = 0
        lives = 3
        running = True
        recordable = True
        enemy_dvizh = True
        ultimate = 0
        ultimate_time_count = 200
        ulting = False
        end_mus = False
        bullets = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        enemy_speed = 1
        anim_count = -1
        sposobnost = 600
        f = open('record.txt', 'r')
        record = f.read()
        f.close()
        pygame.mixer.music.load(random.choice(['1.mp3', '4.mp3']))
        pygame.mixer.music.play()

    if keys[pygame.K_ESCAPE]:
        start()
    if keys[pygame.K_x] and int(ultimate) == 100:
        ulting = True
        ultimate = 0
    else:
        pass

    if ulting and ultimate_time_count >0:
        ultimate_time_count -= 1
        cur_speed = 10
        n = 50
        bullet_speed = 20
    elif ulting and ultimate_time_count == 0:
        ulting = False
        ultimate_time_count = 200
        bullet_speed = 10
        cur_speed = 4
        n = 1


    if keys[pygame.K_z] and sposobnost > 0:
        fps = 60
        if n == 1:
            n += 1
        sposobnost -= 1
    else:
        if n ==2:
            n -= 1
        fps = 120

    if keys[pygame.K_SPACE] or ulting:
        if len(bullets) < n:
            sound1.play()
            bullets.add(snar(x, y))

    if keys[pygame.K_LEFT] and x >= 0:
        x -= cur_speed
        left = True
    if keys[pygame.K_RIGHT] and x <= 450:
        x += cur_speed
        right = True
    else:
        left = False
        right = False

    if lives == 0:
        enemy_dvizh = False
        screen.fill((0, 0, 0))
        screen.blit(image, (x_im, y_im))
        if x_im < 0 and y > 0:
            x_im += 2
            y_im -= 2
        if (x_im, y_im) == (0,0):
            font = pygame.font.Font('freesansbold.ttf', 50)
            text1 = font.render(str("Score:" + str(score)), 1, (255, 255, 255))
            text1_x = 152
            text1_y = 300
            screen.blit(text1, (text1_x, text1_y))
            text2 = font.render(('Press F to restart'), 1, (255, 255, 255))
            text2_x = 40
            text2_y = 350
            screen.blit(text2, (text2_x, text2_y))
            pygame.display.update()

        if not end_mus:
            pygame.mixer.music.load('6.mp3')
            pygame.mixer.music.play()
            end_mus = True

    if score > int(record) and recordable:
        c = open('record.txt', 'w')
        c.write(str(score))
        c.close()
    if enemy_dvizh:
        draw_window()
        draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



print(score)
pygame.quit()