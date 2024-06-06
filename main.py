import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 400
GROUND_LEVEL = 300

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Project")
font = pygame.font.Font("font/Pixeltype.ttf", 32)
bg_music = pygame.mixer.Sound("audio/music.wav")

collision_sound = pygame.mixer.Sound("audio/collision.mp3")
collision_sound.set_volume(0.5)

class Player(pygame.sprite.Sprite): # Pelaaja-luokka, joka perii pygame.sprite.Sprite-luokan ominaisuudet
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk1, player_walk2]  # list of player walking animation images
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = GROUND_LEVEL - self.rect.height
        self.gravity = 0
        self.on_ground = True
        self.damage_cooldown = 0
        self.animation_speed = 0.1  # speed of the walking animation

    def player_input(self):
        keys = pygame.key.get_pressed()  # get all keys currently pressed
        if keys[pygame.K_LEFT]:
            if self.rect.x > 0: 
                self.rect.x -= 5
            else:
                self.rect.x = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.gravity = -20
            self.on_ground = False        

    def apply_gravity(self):
        self.gravity += 1  # gravity
        self.rect.y += self.gravity  # update y position

    def update(self):
        self.player_input()
        self.apply_gravity()

        if self.rect.y >= GROUND_LEVEL - self.rect.height:
            self.rect.y = GROUND_LEVEL - self.rect.height
            self.gravity = 0
            self.on_ground = True

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        self.player_index += self.animation_speed
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
        if not self.on_ground:
            self.image = self.player_jump

    def take_damage(self):
        if self.damage_cooldown <= 0:
            self.damage_cooldown = 60  # can only take damage every 60 frames / 1 sec
            return True
        return False

class Snail(pygame.sprite.Sprite): # Vihollis-luokka, joka perii pygame.sprite.Sprite-luokan ominaisuudet
    def __init__(self): 
        super().__init__() #Miksi super().__init__()? Koska haluamme käyttää pygame.sprite.Sprite-luokan ominaisuuksia
        snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
        snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
        self.snail_walk = [snail_1, snail_2]
        self.image_index = 0
        self.image = self.snail_walk[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_LEVEL - self.rect.height
        self.speed = random.randint(5, 10)
        self.animation_speed = 0.1
        self.collision_sound_played = False

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()

        self.image_index += self.animation_speed
        if self.image_index >= len(self.snail_walk):
            self.image_index = 0
        self.image = self.snail_walk[int(self.image_index)]

class Fly(pygame.sprite.Sprite): # Vihollis-luokka, joka perii pygame.sprite.Sprite-luokan ominaisuudet
    def __init__(self):
        super().__init__()
        fly_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
        fly_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
        self.fly_walk = [fly_1, fly_2]
        self.image_index = 0

        self.image = self.fly_walk[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, GROUND_LEVEL // 2)
        self.speed = random.randint(5, 10)
        self.animation_speed = 0.1
        self.collision_sound_played = False

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()

        self.image_index += self.animation_speed
        if self.image_index >= len(self.fly_walk):
            self.image_index = 0
        self.image = self.fly_walk[int(self.image_index)]

class Collectible(pygame.sprite.Sprite): # Kerättävä-luokka, joka perii pygame.sprite.Sprite-luokan ominaisuudet
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/collectible/collectible1.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(90, 290)
        self.speed = random.randint(5, 10)

    def update(self): # move the collectible to the left and kill it when it's off the screen
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.kill()

class Background:
    def __init__(self, sky_path, ground_path):
        self.sky = pygame.image.load(sky_path).convert_alpha()
        self.ground = pygame.image.load(ground_path).convert_alpha()
    def draw(self, screen):
        screen.blit(self.sky, (0, 0))
        screen.blit(self.ground, (0, 300))

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Project Jumper", font, BLACK, screen, SCREEN_WIDTH // 2, 40, center=True)
        draw_text("1. Single Run - until 50 Points", font, BLACK, screen, SCREEN_WIDTH // 2, 120, center=True)
        draw_text("2. Endless Mode - Until 0 Health", font, BLACK, screen, SCREEN_WIDTH // 2, 200, center=True)
        draw_text("3. Quit", font, BLACK, screen, SCREEN_WIDTH // 2, 280, center=True)
        draw_text(f"Left & Right Arrow-keys to move, Space to jump, [X] to stop session", font, BLACK, screen, SCREEN_WIDTH // 2, 340, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game(single_run=True)
                if event.key == pygame.K_2:
                    game(single_run=False)
                if event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()


def game(single_run):
    player = Player()
    all_sprites = pygame.sprite.Group() # Miksi käytämme Group-luokkaa? Koska haluamme hallita useita sprite-olioita samanaikaisesti
    enemies = pygame.sprite.Group() # Miksi enemies? Koska haluamme hallita vihollisia erikseen
    all_sprites.add(player) # Lisää pelaaja sprite-olioihin
    collectibles = pygame.sprite.Group() # Lisää kerättävät sprite-oliot
    bg_music.play(loops = -1)
    bg_music.set_volume(0.2)

    background = Background("graphics/sky.png", "graphics/ground.png")

    spawn_timer = 0
    collectible_timer = 0
    spawn_delay = 1500
    collectible_delay = 3000
    points = 0
    health = 3
    game_over = False

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    game_over = True
                    bg_music.stop()
                    return

        if pygame.time.get_ticks() - spawn_timer > spawn_delay: # Jos kulunut aika on suurempi kuin spawn_delay, luo uuden vihollisen
            if random.choice([True, False]):
                enemy = Snail()
            else:
                enemy = Fly()
            all_sprites.add(enemy)
            enemies.add(enemy)
            spawn_timer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - collectible_timer > collectible_delay:
            collectible = Collectible()
            all_sprites.add(collectible)
            collectibles.add(collectible)
            collectible_timer = pygame.time.get_ticks()    

        all_sprites.update()

        if pygame.sprite.spritecollideany(player, enemies): # Jos pelaaja osuu viholliseen, vähennä healthia. Itsestään selvää, mutta muistuttaa mitä -collideany tekee.
            for enemy in enemies:
                if pygame.sprite.collide_rect(player, enemy) and not enemy.collision_sound_played:
                    collision_sound.play()
                    enemy.collision_sound_played = True
                if player.take_damage():
                    health -= 1
                    if health <= 0:
                        game_over = True
                        bg_music.stop()

        collectible_collision = pygame.sprite.spritecollide(player, collectibles, True) # True poistaa collectiblen kun se osuu pelaajaan
        if collectible_collision: # Jos pelaaja osuu collectibleen, lisää pisteitä
            points += 1

        if single_run and points == 50:
            game_over = True
            bg_music.stop()

        screen.fill(WHITE)
        background.draw(screen)     # Piirtojärjestyksellä on väliä, taustan tulee olla ensin   
        all_sprites.draw(screen)    # Piirtää kaikki sprite-oliot/classit ruudulle


        draw_text(f"Points: {round(points)}", font, BLACK, screen, 20, 20)
        draw_text(f"Health: {health}", font, BLACK, screen, 20, 60)

        pygame.display.update()
        clock.tick(60) # Hallitsee pelin nopeutta, tässä tapauksessa 60fps
    
    show_end_screen(points, single_run)

def show_end_screen(points, single_run): # Näyttää pelin lopetusruudun, jonka teksi riippuu siitä onko kyseessä single run vai endless mode, sekä palauttaa takaisin päävalikkoon
    screen.fill(WHITE)
    if single_run:
        draw_text("Run Completed!", font, BLACK, screen, SCREEN_WIDTH // 2, 40, center=True)
    else:
        draw_text("Game Over!", font, BLACK, screen, SCREEN_WIDTH // 2, 40, center=True)
    draw_text(f"Points Collected: {points}", font, BLACK, screen, SCREEN_WIDTH // 2, 80, center=True)
    draw_text("Press any key to return to main menu", font, BLACK, screen, SCREEN_WIDTH // 2, 120, center=True)

    pygame.display.update()

    waiting = True # odottaa kunnes pelaaja painaa jotain näppäintä palatakseen päävalikkoon
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
    main_menu()

if __name__ == "__main__":
    main_menu()
