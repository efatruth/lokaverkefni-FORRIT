#livinus felix bassey
#lokaverkefni_space-invaders
#20.04.2019

import pygame
import random
import os

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

##CONSTANTS##

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# DISPLAY
display_width = 960
display_height = 960
DISPLAYSURFACE = pygame.display.set_mode((display_width, display_height))

# CLOCK
clock = pygame.time.Clock()
FPS = 60

# FONT
path = os.path.abspath('fonts/emulogic.ttf')
smallfont = pygame.font.Font(path, 23)
bigfont = pygame.font.Font(path, 29)

# SOUNDS
pew_sound = pygame.mixer.Sound('sounds/pew.ogg')
boom_sound = pygame.mixer.Sound('sounds/boom.ogg')
impact_sound = pygame.mixer.Sound('sounds/impact.ogg')
pause_in = pygame.mixer.Sound('sounds/pause_in.ogg')
pause_out = pygame.mixer.Sound('sounds/pause_out.ogg')
youwin_jingle = pygame.mixer.Sound('sounds/youwin.ogg')
gameover_sound = pygame.mixer.Sound('sounds/gameover.ogg')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        self.image = pygame.image.load("images/spaceship.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.score = 0
        self.rect.x = display_width / 2
        self.rect.y = display_height - 75
        self.rect.center = (self.rect.x, self.rect.y)
        self.dx = 15
        self.dy = 15
        self.lives = 3
        self.last = pygame.time.get_ticks()
        self.gun = Gun()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.dx
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.dx
        if keys[pygame.K_UP]:
            self.rect.y -= self.dy
        if keys[pygame.K_DOWN]:
            self.rect.y += self.dy
        if self.rect.x + 150 >= display_width:
            self.rect.x = display_width - 150
        elif self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y + 120 >= display_height:
            self.rect.y = display_height - 120
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last >= 225:
                self.last = now
                self.gun.shoot(58, 34)  # left gun
                self.gun.shoot(91, 34)  # right gun
                if self.score > 0:
                    self.score = self.score - 20
                pygame.mixer.Sound.play(pew_sound)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load("images/asteroid.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = -160
        self.rect.x = random.randint(1, display_width - 160)
        self.dx = 50
        self.dy = random.randint(6,10)

    def update(self):
        self.rect.y += self.dy
        if self.rect.y >= display_height:
            self.kill()


class AsteroidSpawner:
    def __init__(self):
        self.delay = 1000
        self.time = 0
        self.speed_increment = 0

    def spawn_asteroid(self):
        new_time = pygame.time.get_ticks()
        time_delay = self.time + self.delay
        if time_delay <= new_time and self.delay > 500:
            amount = random.randint(1,3)
            for x in range(amount):
                asteroid = Asteroid()
                asteroid_list.add(asteroid)
                all_sprites_list.add(asteroid)
            self.speed_increment += 0.1
            asteroid.dy += self.speed_increment
            self.delay -= 10
            self.time = new_time


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/laser.png")
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.dx = 25  # speed on x
        self.dy = 25  # speed on y

    def update(self):
        self.rect.y -= self.dy
        if self.rect.y + 19 < 0:
            self.kill()


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shot_start_x = 4
        self.shot_start_y = 13

    def shoot(self, x_pos_on_sprite, y_pos_on_sprite):
        self.bullet = Bullet()
        self.bullet.rect.x = player.rect.x + x_pos_on_sprite - self.shot_start_x
        self.bullet.rect.y = player.rect.y + y_pos_on_sprite - self.shot_start_y
        all_sprites_list.add(self.bullet)
        bullet_list.add(self.bullet)


def msg_to_screen(font, msg, color, x_pos, y_pos, fromright=False):
    text = font.render(msg, True, color)
    if not fromright:
        DISPLAYSURFACE.blit(text, (x_pos, y_pos))
    else:
        DISPLAYSURFACE.blit(text, (display_width - text.get_width() - x_pos, y_pos))


def center_msg_to_screen(font, msg, color, x=None, y=None):
    text = font.render(msg, True, color)
    if not x:
        x = display_width/2 - text.get_width()/2
    if not y:
        y = display_height/2 - text.get_height()/2
    DISPLAYSURFACE.blit(text, [x, y])




running = True
reset = True
while running:
    if reset:
        all_sprites_list = pygame.sprite.Group()
        asteroid_list = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        BackGround = Background('images/spacepic.jpg', [0, 0])
        player = Player()
        asteroidspawner = AsteroidSpawner()
        all_sprites_list.add(player)
        game = True
        gamepause = False
        gamewin = False
        gameover = False
        reset = False

    while gamepause:
        DISPLAYSURFACE.fill(BLACK)
        center_msg_to_screen(smallfont, "Do you want to quit the game? (y/n)", WHITE)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    gamepause = False
                    game = False
                    running = False

                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    gamepause = False
                    game = True
                    pygame.mixer.Sound.play(pause_out)
        pygame.display.update()
        clock.tick(FPS)

    while gameover:
        DISPLAYSURFACE.fill(BLACK)
        center_msg_to_screen(bigfont, "GAME OVER.", WHITE, y = display_height/2 - 65)
        center_msg_to_screen(bigfont, "SCORE: " + str(player.score), WHITE, y = display_height/2 + 0)
        center_msg_to_screen(bigfont, "Do you want to play again? (y/n)", WHITE, y = display_height/2 + 65)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    gameover = False
                    game = False
                    running = True
                    reset = True

                elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    game = False
                    gameover = False
                    running = False
        pygame.display.update()
        clock.tick(FPS)

    while gamewin:
        DISPLAYSURFACE.fill(BLACK)
        center_msg_to_screen(bigfont, "YOU WIN!", WHITE, y = display_height/2 - 65)
        center_msg_to_screen(bigfont, "SCORE: " + str(player.score), WHITE, y = display_height/2 + 0)
        center_msg_to_screen(bigfont, "Do you want to play again? (y/n)", WHITE, y = display_height/2 + 65)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    gamewin = False
                    reset = True

                if event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                    gamewin = False
                    gameover = False
                    game = False
                    running = False
                    reset = False

        pygame.display.update()
        clock.tick(FPS)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                running = False
                gamewin = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamepause = True
                    game = False
                    pygame.mixer.Sound.play(pause_in)
                if event.key == pygame.K_w:
                    gamewin = True
                    game = False

        if player.lives <= 0:
            gameover = True
            game = False
            pygame.mixer.Sound.play(gameover_sound)


        elif asteroidspawner.delay <= 500:
            gamewin = True
            game = False
            pygame.mixer.Sound.play(youwin_jingle)
        asteroidspawner.spawn_asteroid()
        collided = pygame.sprite.groupcollide(bullet_list, asteroid_list, True, True)
        if collided:
            for hits in collided:
                player.score += 100
            pygame.mixer.Sound.play(boom_sound)
        collided = pygame.sprite.spritecollide(player, asteroid_list, True)
        if collided:
            for hits in collided:
                player.lives -= 1
            pygame.mixer.Sound.play(impact_sound)
        all_sprites_list.update()
        DISPLAYSURFACE.fill(WHITE)
        DISPLAYSURFACE.blit(BackGround.image, BackGround.rect)
        bullet_list.draw(DISPLAYSURFACE)
        player.draw(DISPLAYSURFACE)
        asteroid_list.draw(DISPLAYSURFACE)
        msg_to_screen(smallfont, "score: " + str(player.score), WHITE, 20, 20)
        msg_to_screen(smallfont, "lives: " + str(player.lives), WHITE, 20, 20, fromright=True)
        pygame.display.update()
        clock.tick(FPS)
pygame.quit()
quit()
