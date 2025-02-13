import os
import sys
import random
import pygame


pygame.init()
size = width, height = 800, 1000
screen = pygame.display.set_mode(size)

ship_speed = 50
ship_size = 75

alien_speed = 1.35
alien_size = 50

bullet_speed = 40
bullet_size = 20

player_bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
ship_p = pygame.sprite.GroupSingle()

score = 0
lose_flag = False

count_of_aliens = 5
level = 0

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('You have lost', False, 'white')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


background = load_image('cosmos.png')
background = pygame.transform.scale(background, (800, 1000))
start_screen = load_image('start_screen.png')
start_screen = pygame.transform.scale(start_screen, (800, 1000))


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites, ship_p)
        self.x = pos[0]
        self.y = pos[1]

        self.image = load_image('ship.png', 'white')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.ship_speed = ship_speed

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.ship_speed

    def move_right(self):
        if self.rect.x < 725:
            self.rect.x += self.ship_speed

    def shoot(self):
        bul_pos = (self.rect.centerx - (bullet_size // 2), self.rect.y)
        player_bullets.add(Bullet(bul_pos, bullet_size))

    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(all_sprites)
        self.x = pos[0]
        self.y = pos[1]

        self.image = load_image('bullet.png', 'black')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.move_speed = -bullet_speed

    def update(self):
        self.rect.y += self.move_speed
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

        if self.rect.bottom <= 0 or self.rect.top >= height:
            self.kill()


class Alien(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__(aliens, all_sprites)
        self.x = pos[0]
        self.y = pos[1]

        self.image = load_image('alien.png', 'black')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.move_speed = alien_speed
        self.side_speed = 5

    def move_left(self):
        self.rect.x -= self.side_speed

    def move_right(self):
        self.rect.x += self.side_speed

    def update(self):
        global lose_flag
        self.rect.y += self.move_speed

        if random.randint(0, 1) == 0 and self.rect.x > 0:
            self.move_left()
        else:
            if self.rect.x < 725:
                self.move_right()

        if self.rect.y >= 850:
            lose_flag = True

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


player = Ship((0, 850), ship_size)


if __name__ == '__main__':
    end_it = False
    running = False
    while end_it is False:
        screen.fill('black')
        screen.blit(start_screen, (0, 0))
        text = pygame.font.SysFont("Britannic Bold", 60)
        nlabel = text.render("Welcome to Space Pirates", 1, 'Black')
        nlabel2 = text.render("Press to start", 1, 'Black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ent_it = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_it = True
                running = True
        screen.blit(nlabel, (150, 400))
        screen.blit(nlabel2, (250, 500))
        pygame.display.flip()
    clock = pygame.time.Clock()
    while running:
        try:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.move_left()
                    if event.key == pygame.K_d:
                        player.move_right()

                    if event.key == pygame.K_SPACE:
                        player.shoot()

            screen.fill("black")

            screen.blit(background, (0, 0))

            if pygame.sprite.groupcollide(ship_p, aliens, True, True) or lose_flag:
                all_sprites.empty()
                if player:
                    with open('records.txt', 'a+') as file:
                        f = file.readlines()
                        f = sorted([int(x) for x in f])

                        for i in f:
                            print(i, file=file)
                        print(score, file=file)

                    with open('records.txt', 'r') as file:
                        f = file.readlines()
                        f = sorted([int(x) for x in f])
                        record = f[-1]
                    ur_scores = my_font.render('Your record: ' + str(record), False, 'white')
                player = None

            if pygame.sprite.groupcollide(aliens, player_bullets, True, True):
                score += 10

            score_count = my_font.render('SCORE: ' + str(score), False, 'white')
            level_count = my_font.render('level: ' + str(level), False, 'white')

            if not all_sprites:
                screen.blit(text_surface, (300, 500))
                screen.blit(ur_scores, (300, 600))

            screen.blit(score_count, (575, 0))
            screen.blit(level_count, (575, 50))

            if not aliens and all_sprites:
                for i in range(count_of_aliens):
                    Alien((random.randint(0, 725), random.randint(0, 200)), alien_size)
                count_of_aliens += 5
                level += 1

            all_sprites.draw(screen)
            all_sprites.update()

            pygame.display.flip()
            clock.tick(60)

        except AttributeError:
            pass

    pygame.quit()
