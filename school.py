import pygame
from pygame import mixer
import os
from random import randint, choice
pygame.mixer.init(44100)
pygame.init()

def draw_score(k):
    font = pygame.font.Font(None, 50)
    text = font.render(f"{k}", 2, (100, 255, 100))
    text_x = 20
    text_y = 15
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 5, text_y - 5,
                                           text_w + 9, text_h + 5), 2)

def draw_best_record(k):
    font = pygame.font.Font(None, 50)
    text = font.render(f"BEST: {k}", 2, (255, 100, 100))
    text_x = 90
    text_y = 15
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (255, 0, 0), (text_x - 5, text_y - 5,
                                           text_w + 9, text_h + 5), 2)

def random_wall(x):
    size = randint(50, 450)
    wall = Wall(False, x, size)
    wall_reverse = Wall(True, x, H - size - WALL_S)
    return(wall, wall_reverse)

def is_of_display(sprite):
    return sprite.rect.x < W

def is_of_display_wall(sprite):
    return sprite.rect.x + WALL_WIDTH  < 0

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image

def load_sample(name):
    fullname = os.path.join('data', name)
    sound = pygame.mixer.Sound(fullname)
    return sound

class Bird(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("bird.png")

        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image = pygame.transform.flip(self.image, True, False)
        pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = W / 2 - 50
        self.rect.y = H / 2 - 50

        self.mask = pygame.mask.from_surface(self.image)

        self.speed = SPEED

        self.sound = load_sample('jump.wav')
    
    def update(self):
        self.speed += GRAVITY
        self.rect.y += self.speed

    def jump(self):
        self.speed = -SPEED
        self.sound.play()
        


class Ground(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("ground.jpg")
        self.image = pygame.transform.scale(self.image, (W * 2, 75))
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect.y = H - 75
        self.rect.x = W + 100
    
    def update(self):
        self.rect.x -= GAME_SPEED

class Wall(pygame.sprite.Sprite):
    def __init__(self, invert, x_pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('wall.jpg')
        self.image = pygame.transform.scale(self.image, (WALL_WIDTH, WALL_WEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos

        if invert:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y = size - self.rect[3]
        else:
            self.rect.y = H - size
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED

boom = load_sample('boom.wav')
best_score = open(os.path.join('data/txt.txt')).read()
best_score_int = int(best_score)

FONTS = ['images.jpg',
         'images2.jpg',
         'images4.jpg',
         'images3.jpg',
         'images1.jpg']

FONT_MUSIC = ['skril.mp3',
              'skril1.mp3',
              'skril2.mp3',
              'music.mp3']

W = 450
H = 600
SPEED = 7
GRAVITY = 0.5
GAME_SPEED = 5

WALL_WIDTH = 90
WALL_WEIGHT = 400
WALL_S = 150
k = int(input())

if pygame.display.get_init():
    for i in range(k):
        pygame.mixer.music.load(str('data/' + choice(FONT_MUSIC)))
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((W, H))
        
        BACKGROUND = load_image(choice(FONTS))
        BACKGROUND = pygame.transform.scale(BACKGROUND, (W, H))

        ## привет птичке
        group_bird = pygame.sprite.Group()
        bird = Bird(group_bird)

        ## создание земли
        grounds = pygame.sprite.Group()
        ground = Ground(grounds)

        ## создание стен
        wall_group = pygame.sprite.Group()
        wall = random_wall(W)
        wall_group.add(wall[0])
        wall_group.add(wall[1])

        record = 0

        jumping = False
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        jumping = True
                        bird.jump()
            
            if pygame.display.get_init():
                if is_of_display(ground):
                    grounds.remove()   
                    new_groaund = ground = Ground(grounds)
                
                if is_of_display_wall(wall_group.sprites()[0]):
                    wall_group.remove(wall_group.sprites()[0])
                    wall_group.remove(wall_group.sprites()[0])

                    new_wall = wall = random_wall(W)

                    wall_group.add(wall[0])
                    wall_group.add(wall[1])

                    record += 1
                
                if pygame.sprite.spritecollideany(bird, grounds) or pygame.sprite.spritecollideany(bird, wall_group) or bird.rect.y < 0:
                    boom.play()
                    break

                screen.blit(BACKGROUND, (0, 0))
                grounds.update()
                if jumping:
                    group_bird.update()
                    wall_group.update()
                
                wall_group.draw(screen)
                group_bird.draw(screen)
                grounds.draw(screen)
                draw_score(record)
                draw_best_record(best_score_int)

                pygame.display.update()
            
            if best_score_int < record:
                best_score_int = record

best_score = open(os.path.join('data/txt.txt'), 'w')
print(best_score_int, file=best_score)
best_score.close()
pygame.quit()