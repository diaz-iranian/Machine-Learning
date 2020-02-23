import pygame
import random
import sys
pygame.init()

width = 400
height = 380

WHITE = (255, 255, 255)
RED = (180, 0, 0)
BLACK = (0, 0, 0)
SNAKE_COLOR = (0, 168, 7)

food_h = [i for i in range(20, height - 16) if i % 10 == 0]
food_w = [i for i in range(20, width - 16) if i % 10 == 0]

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((SNAKE_COLOR))
        self.rect = self.image.get_rect()
        self.rect.center = (120, 120)
        self.speedx = 0
        self.speedy = 0
        self.score = 0
        self.tail = []
        self.ispaused = False

    def update(self):
        if self.ispaused == False:
            if self.score == len(self.tail):
                self.tail.append((self.rect.x, self.rect.y))
            else:
                self.tail.append((self.rect.x, self.rect.y))
                self.tail.pop(0)
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.speedx >= 0:
                self.speedx = 10
                self.speedy = 0
            if keys[pygame.K_LEFT] and self.speedx <= 0:
                self.speedx = -10
                self.speedy = 0
            if keys[pygame.K_UP] and self.speedy <= 0:
                self.speedy = -10
                self.speedx = 0
            if keys[pygame.K_DOWN] and self.speedy >= 0:
                self.speedy = 10
                self.speedx = 0
            if self.rect.left >= width:
                self.rect.left = 5
            if self.rect.top >= height:
                self.rect.bottom = 5
            if self.rect.bottom <= 0:
                self.rect.top = height - 5
            if self.rect.left <= 0:
                self.rect.left = width - 5

    def _exit(self):
        if self.ispaused == False:
            for i in range(1, len(self.tail)):
                if dist(self.rect.x, self.rect.y, self.tail[i][0], self.tail[i][1]) < 1:
                    endgame()


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((8, 8))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


def dist(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**1 / 2


def draw_txt(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def refresh_vars():
    global all_sprites, food, player, tails
    all_sprites = pygame.sprite.Group()
    tails = pygame.sprite.Group()
    player = Snake()
    food = Food(random.choice(food_w), random.choice(food_h))
    all_sprites.add(player)
    all_sprites.add(food)


def endgame():
    end_run = True
    while end_run:
        keystate = pygame.key.get_pressed()
        for i in pygame.event.get():
            if i.type == pygame.QUIT or keystate[pygame.K_e]:
                sys.exit()
        if keystate[pygame.K_a]:
            end_run = False
        screen.fill(BLACK)
        draw_txt(screen, "Game Over !!", 55, width / 2, 100)
        draw_txt(screen, f"Score = {player.score}", 30, width / 2, 200)
        draw_txt(screen, "Press 'a' to Play Again and 'e' to exit ", 22, width / 2, 250)
        draw_txt(screen, "Press 'p' to Pause and 'r' to resume ", 22, width / 2, 280)
        pygame.display.flip()
    refresh_vars()


all_sprites = pygame.sprite.Group()
tails = pygame.sprite.Group()
player = Snake()
food = Food(random.choice(food_w), random.choice(food_h))
all_sprites.add(player)
all_sprites.add(food)
running = True

while running:
    clock.tick(25)
    keys_pressed = pygame.event.get()
    for i in keys_pressed:
        if i.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        player.ispaused = True
    if keys[pygame.K_r]:
        player.ispaused = False
    if pygame.sprite.collide_rect(player, food):
        food.kill()
        player.score += 1
        food = Food(random.choice(food_w), random.choice(food_h))
        all_sprites.add(food)
    all_sprites.update()
    screen.fill(BLACK)
    draw_txt(screen, str(player.score), 18, width / 2, 10)
    all_sprites.draw(screen)
    for i in range(1, len(player.tail)):
        pygame.draw.rect(screen, SNAKE_COLOR, (player.tail[i][0], player.tail[i][1], 10, 10))
    pygame.display.flip()
    player._exit()
pygame.quit()
