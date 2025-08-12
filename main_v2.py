import pygame
import collision_detection as cd
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.set_num_channels(100)  # Allow up to 8 simultaneous sounds

clock = pygame.time.Clock()
fps = 60

font = pygame.font.SysFont('calibri', 30, True)

win_res = [1280, 720]
display = pygame.display.set_mode(win_res)
pygame.display.set_caption("Space Invaders V2")

pygame.mouse.set_visible(False)

# images
space_ship = pygame.image.load("data/images/spaceship.png").convert_alpha()
bg = pygame.image.load("data/images/bg.png").convert_alpha()
bullet_img = pygame.image.load("data/images/bullet.png").convert_alpha()
alien_bullet_img = pygame.image.load("data/images/alien_bullet.png").convert_alpha()
enemy_1 = pygame.image.load("data/images/alien1.png").convert_alpha()
enemy_2 = pygame.image.load("data/images/alien2.png").convert_alpha()
enemy_3 = pygame.image.load("data/images/alien3.png").convert_alpha()
enemy_4 = pygame.image.load("data/images/alien4.png").convert_alpha()
enemy_5 = pygame.image.load("data/images/alien5.png").convert_alpha()
power_up = pygame.image.load("data/images/power_up.png").convert_alpha()
power_down = pygame.image.load("data/images/power_down.png").convert_alpha()
title_page = pygame.image.load("data/images/title.png").convert_alpha()
title_page.set_colorkey((255, 255, 255))

# sounds
shooting_sound = pygame.mixer.Sound("data/audio/laser.wav")
shooting_sound.set_volume(0.05)
enemy_shooting_sound = pygame.mixer.Sound("data/audio/laser.wav")
explosion_sound = pygame.mixer.Sound("data/audio/explosion2.wav")
explosion_sound.set_volume(1.5)
game_over_sound = pygame.mixer.Sound("data/audio/gameover.wav")
game_over_sound.set_volume(2)
power_up_sound = pygame.mixer.Sound("data/audio/powerup.wav")
power_up_sound.set_volume(2)
power_down_sound = pygame.mixer.Sound("data/audio/powerdown.wav")
power_down_sound.set_volume(2)
levelup_sound = pygame.mixer.Sound("data/audio/levelup.wav")
levelup_sound.set_volume(2)
health_down_sound = pygame.mixer.Sound("data/audio/healthdown.wav")
health_down_sound.set_volume(2)

exp_animation = []
for x in range(1, 6):
    exp_animation.append(pygame.image.load("data/images/exp" + str(x) + ".png"))


class Spaceship:
    def __init__(self, x, y, health, img):
        self.x = x
        self.y = y
        self.health = health
        self.img = img
        self.bullet_count = 1

    def draw(self, win):
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y))

    def update(self):
        mx = pygame.mouse.get_pos()[0]
        self.x = mx


class Bullet:
    def __init__(self, x, y, vel, img):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self):
        self.y += self.vel


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.health = None

        # Assign image based on enemy type
        match self.enemy_type:
            case 1:
                self.health = 1
                self.img = enemy_1
            case 2:
                self.health = 3
                self.img = enemy_2
            case 3:
                self.health = 5
                self.img = enemy_3
            case 4:
                self.health = 9
                self.img = enemy_4
            case 5:
                self.health = 15
                self.img = enemy_5

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Drop:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.vel = 2
        self.type = type
        if self.type == 1:
            self.img = power_up
        elif self.type == 2:
            self.img = power_down

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def update(self):
        self.y += self.vel


def load_level(path, cell_width, cell_height):
    enemies = []
    with open(path, "r") as file:
        level_data = [list(map(int, line.strip().split(','))) for line in file]

    num_columns = len(level_data[0])
    grid_width = num_columns * cell_width
    start_x = (win_res[0] - grid_width) // 2

    for row_idx, row in enumerate(level_data):
        for col_idx, cell in enumerate(row):
            if cell > 0:
                x = start_x + col_idx * cell_width
                y = row_idx * cell_height + 50
                enemy = Enemy(x, y, cell)
                enemies.append(enemy)
    return enemies


def render_text(text, text_color, x, y, win, size):
    font = pygame.font.SysFont("comic sans", size, bold=True)

    # Create a text surface
    text_surface = font.render(text, True, text_color)

    text_width = text_surface.get_width() // 2

    x -= text_width

    # Blit the text surface onto the window
    win.blit(text_surface, (x, y))


def update():
    pygame.display.update()
    clock.tick(fps)


def game_loop():
    spaceship = Spaceship(363, 600, 100, space_ship)

    score = 0
    vel = 1
    level = 1
    enemies = load_level("data/levels/level" + str(level) + ".txt", 64, 64)

    score_txt = font.render("SCORE: " + str(score), True, (255, 255, 255))
    health_txt = font.render("HEALTH: " + str(spaceship.health), True, (255, 255, 255))

    bullets = []
    alien_bullets = []
    drops = []

    shooting_timer = 20

    shooting = False

    # Explosion animation variables
    animation_steps = 5  # Total frames in explosion animation
    last_update = pygame.time.get_ticks()  # Last time animation was updated
    animation_cooldown = 100  # Milliseconds between frames (adjust as needed)
    frame = 0  # Current animation frame
    animating_explosion = False  # Flag to control explosion animation

    start_button = pygame.Rect(win_res[0]/2 - 150, 370, 300, 140)
    quit_button = pygame.Rect(win_res[0]/2 - 150, 530, 300, 140)
    a = 30
    d = -1
    vel_2 = 0.5

    health_rect = pygame.Rect(10, 10, 400, 25)

    main_menu = True
    splash = False
    running = True
    while running:
        if main_menu:
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        # select_sound.play()
                        main_menu = False
                    if quit_button.collidepoint(event.pos):
                        # select_sound.play()
                        running = False

            if a == 20:
                d = -1
            elif a == 0:
                d = 1
            a += vel_2 * d

            spaceship.health = 100
            health_rect.width = 400
            level = 1
            score = 0
            enemies = load_level("data/levels/level" + str(level) + ".txt", 64, 64)

            display.blit(bg, (0, 0))
            display.blit(bg, (600, 0))
            display.blit(bg, (1000, 0))
            pygame.draw.rect(display, (255, 50, 50), start_button)
            pygame.draw.rect(display, (255, 50, 50), quit_button)
            display.blit(title_page, (640 - title_page.get_width() // 2, a))
            render_text("start", (255, 255, 255), 640, 353, display, 100)
            render_text("quit", (255, 255, 255), 640, 523, display, 100)

        elif splash:
            pass
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    shooting = True

            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

            shooting_timer -= 1
            if shooting and shooting_timer <= 0:
                match spaceship.bullet_count:
                    case 1:
                        bullet = Bullet(mouse_pos_x -8, 600, -5, bullet_img)
                        bullets.append(bullet)
                    case 2:
                        bullet = Bullet(mouse_pos_x - 15, 600, -5, bullet_img)
                        bullets.append(bullet)
                        bullet = Bullet(mouse_pos_x + 3, 600, -5, bullet_img)
                        bullets.append(bullet)
                    case 3:
                        bullet = Bullet(mouse_pos_x - 22, 600, -5, bullet_img)
                        bullets.append(bullet)
                        bullet = Bullet(mouse_pos_x - 7, 600, -5, bullet_img)
                        bullets.append(bullet)
                        bullet = Bullet(mouse_pos_x + 8, 600, -5, bullet_img)
                        bullets.append(bullet)

                shooting_timer = 20
                shooting = False

                shooting_sound.play()

            display.blit(bg, (0, 0))
            display.blit(bg, (600, 0))
            display.blit(bg, (1000, 0))
            spaceship.draw(display)

            for enemy in enemies:
                if random.randint(1, 1000) == 1:
                    enemy_bul = Bullet(enemy.x + enemy.img.get_width()/2 - 5, enemy.y + enemy.img.get_height(), 2, alien_bullet_img)
                    alien_bullets.append(enemy_bul)
                    shooting_sound.play()
                enemy.x += vel
                if enemy.x >= (win_res[0] - 164) or enemy.x <= 100:
                    vel = -vel

                enemy.draw(display)

            for bul in bullets.copy():
                bul.draw(display)
                bul.update()
                if bul.y < 10:
                    bullets.remove(bul)

            for bul in alien_bullets.copy():
                bul.draw(display)
                bul.update()
                if bul.y > win_res[1]:
                    alien_bullets.remove(bul)

            for drop in drops.copy():
                drop.draw(display)
                drop.update()
                if drop.y >= win_res[1]:
                    drops.remove(drop)

            old_health = spaceship.health
            old_bullet_count = spaceship.bullet_count

            cd.handle_obj_with_drop_collision(spaceship, drops, False)
            cd.handle_obj_with_drop_collision(spaceship, alien_bullets, True)

            new_health = spaceship.health
            new_bullet_count = spaceship.bullet_count
            if new_health != old_health and new_health != 0:
                health_down_sound.play()
                health_rect.width -= 80

            if new_bullet_count > old_bullet_count:
                power_up_sound.play()
            elif new_bullet_count < old_bullet_count:
                power_down_sound.play()


            collided, x, y, score = cd.handle_list_collision(enemies, bullets, score)
            score_txt = font.render("SCORE: " + str(score), True, (255, 255, 255))

            if collided and not animating_explosion:
                animating_explosion = True  # Start explosion animation
                frame = 0  # Reset frame count for new animation
                explosion_x, explosion_y = x - 30, y - 30  # Store explosion position

                if random.randint(1, 3) == 1:
                    type = random.randint(1, 2)
                    drop = Drop(x - 20, y + 20, type)
                    drops.append(drop)

                explosion_sound.play()

            if animating_explosion:
                # Draw the current explosion frame at the saved position
                display.blit(exp_animation[frame], (explosion_x, explosion_y))
                current_time = pygame.time.get_ticks()

                # Check if enough time has passed since last frame update
                if current_time - last_update >= animation_cooldown:
                    frame += 1
                    last_update = current_time  # Reset last update time

                    # Reset animation if it has reached the end
                    if frame >= animation_steps:
                        frame = 0
                        animating_explosion = False  # Stop animating explosion

            if not enemies and level != 11:
                level += 1

                enemies = load_level("data/levels/level" + str(level) + ".txt", 64, 64)
                if level != 11:
                    levelup_sound.play()
                else:
                    pass

            display.blit(score_txt, (win_res[0] - 180, 10))
            pygame.draw.rect(display, (80, 0, 0), [10, 10, 400, 25])
            pygame.draw.rect(display, (255, 0, 0), health_rect)

            if (spaceship.health <= 0):
                game_over_sound.play()
                main_menu = True

            spaceship.update()

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


game_loop()

#Mery boss ka level uper hai
#dil toota to bohot hai