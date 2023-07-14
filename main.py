import pygame
from sys import exit
from random import randint, choice
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(player_walk_1_path).convert_alpha()
        player_walk_2 = pygame.image.load(player_walk_2_path).convert_alpha()
        self.player_jump = pygame.image.load(jump_path).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound(jump_sound_path)
        self.jump_sound.set_volume(0.05)

        self.is_jumping = False  # Track if player is currently jumping
        self.jump_count = 0  # Track the number of jumps performed
        self.max_jumps = 2  # Maximum number of jumps allowed
        self.jump_cooldown = 250  # Cooldown period in milliseconds (adjust as needed)
        self.last_jump_time = 0  # Timestamp of the last jump

    def player_input(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.is_jumping:
                if current_time - self.last_jump_time >= self.jump_cooldown:
                    # Jump is allowed
                    self.gravity = -20
                    self.jump_sound.play()
                    self.is_jumping = True
                    self.jump_count += 1
                    self.last_jump_time = current_time
            else:
                # Allow a second jump if still within the max jumps limit
                if self.jump_count < self.max_jumps:
                    if current_time - self.last_jump_time >= self.jump_cooldown:
                        # Jump is allowed
                        self.gravity = -20
                        self.jump_sound.play()
                        self.jump_count += 1
                        self.last_jump_time = current_time

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.jump_count = 0
            self.is_jumping = False

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= int(len(self.player_walk)):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()  # we need this or error!

        if type == 'fly':
            fly_1 = pygame.image.load(Fly1_path).convert_alpha()
            fly_2 = pygame.image.load(Fly2_path).convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load(snail1_path).convert_alpha()
            snail_2 = pygame.image.load(snail2_path).convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        global score

        self.animation_state()
        if 40 <= score // 1000 < 50:
            self.rect.x -= 20
        elif 50 <= score // 1000 < 65:
            self.rect.x -= 25
        elif  score // 1000 >= 65:
            self.rect.x -= 50
        else:
            self.rect.x -= 6

        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = (pygame.time.get_ticks() - start_time)
    if 40 <= score // 1000 < 50:
        score_surf = test_font.render(f"HARD MODE : {current_time // 1000}", False, "ORANGE")
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)
    elif score // 1000 >= 50:
        score_surf = test_font.render(f"EVEN HARDER : {current_time // 1000}", False, "RED")
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)
    else:
        score_surf = test_font.render(f"Score : {current_time // 1000}", False, "Black")
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)
    return current_time


def display_welcome():
    welcome_surf = test_font.render(f"Welcome  to  Boom's  game  na ja", False, "Black")
    welcome_rect = welcome_surf.get_rect(center=((GAME_WIDTH / 2), GAME_HEIGHT / 6))
    screen.blit(welcome_surf, welcome_rect)


def collision_sprite():
    global  score
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):  # (sprite, group, boolean(True is "Delete obstacle_group when collided)
        if score >= 60000:
            score_check(3)

        obstacle_group.empty()
        return False
    else:
        return True


def score_check(num):
    global bg_music
    a = num
    match a:
        case 1:
            bg_music.stop()
            bg_music = pygame.mixer.Sound(song1_path)
            bg_music.play()  # -1 = forever
            bg_music.set_volume(0.03)

        case 2:
            bg_music.stop()
            bg_music = pygame.mixer.Sound(song2_path)
            bg_music.play()  # -1 = forever
            bg_music.set_volume(0.03)

        case 3:
            bg_music.stop()
            bg_music = pygame.mixer.Sound(tt_path)
            bg_music.play()  # -1 = forever
            bg_music.set_volume(0.4)

GAME_HEIGHT = 400
GAME_WIDTH = 800

pygame.init()

double_jump_check = 0

current_dir = os.getcwd()
print(current_dir)
font_path = os.path.join(current_dir, "Bin", "Pixel-type.ttf")
Fly1_path = os.path.join(current_dir, "Bin", "Fly1.png")
Fly2_path = os.path.join(current_dir, "Bin", "Fly2.png")
ground_path = os.path.join(current_dir, "Bin", "ground.png")
jump_sound_path = os.path.join(current_dir, "Bin", "jump.mp3")
jump_path = os.path.join(current_dir, "Bin", "jump.png")
music_path = os.path.join(current_dir, "Bin", "music.wav")
player_stand_path = os.path.join(current_dir, "Bin", "player_stand.png")
player_walk_1_path = os.path.join(current_dir, "Bin", "player_walk_1.png")
player_walk_2_path = os.path.join(current_dir, "Bin", "player_walk_2.png")
Sky_path = os.path.join(current_dir, "Bin", "Sky.png")
snail1_path = os.path.join(current_dir, "Bin", "snail1.png")
snail2_path = os.path.join(current_dir, "Bin", "snail2.png")
song1_path = os.path.join(current_dir, "Bin", "song1.wav")
song2_path = os.path.join(current_dir, "Bin", "song2.wav")
tt_path = os.path.join(current_dir, "Bin", "tt.wav")
heart_path = os.path.join(current_dir, "Bin", "heart.png")








test_font = pygame.font.Font(font_path, 50)

screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("ระวังหัวร้อนเด้อ")
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound(music_path)
bg_music.play(loops=-1)  # -1 = forever
bg_music.set_volume(0.03)

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load(Sky_path).convert()
ground_surface = pygame.image.load(ground_path).convert()  # convert ทุกครั้งเด้อ

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)  # (event that wanna trigger, milli sec)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)






while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            pass

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    game_active = True
                    start_time = pygame.time.get_ticks()
                    bg_music.stop()
                    bg_music = pygame.mixer.Sound(music_path)
                    bg_music.play(loops=-1)  # -1 = forever
                    bg_music.set_volume(0.03)
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()

        if 40000 < score < 40020:
            score_check(1)
        elif 50000 < score < 50020:
            score_check(2)

    else:

        screen.fill((94, 129, 162))

        score_message = test_font.render(f'Your score:  {score // 1000}   Tryna  make  it  60  XD  press  "  b  "',
                                         False, "black")
        score_message_rect = score_message.get_rect(center=(GAME_WIDTH / 2, 5.5 * GAME_HEIGHT / 6))
        display_welcome()
        welcome2_surf = test_font.render(f"Press  '  Space Bar  '  to  Jump  ,  Press  '  b  '  to  start", False,
                                         "Black")
        welcome2_rect = welcome2_surf.get_rect(center=(GAME_WIDTH / 2, 5.5 * GAME_HEIGHT / 6))

        ImInLoveWithYou = test_font.render(f"Please  go  out  with  me !!  (Text  me  btw)", False, "RED")
        ImInLoveWithYou_rect = ImInLoveWithYou.get_rect(center=(GAME_WIDTH / 2, 5.5 * GAME_HEIGHT / 6))

        if score // 1000 == 0:
            player_stand_surf = pygame.image.load(player_stand_path)
            player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)  # (surface, angle, scale)
            player_stand_rect = player_stand_surf.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2))
            screen.blit(player_stand_surf, player_stand_rect)
            screen.blit(welcome2_surf, welcome2_rect)

        elif score // 1000 >= 60:
            heart = pygame.image.load(heart_path).convert_alpha()
            heart = pygame.transform.rotozoom(heart, 0, 0.25)
            heart_rect = heart.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2))

            screen.blit(heart, heart_rect)
            screen.blit(ImInLoveWithYou, ImInLoveWithYou_rect)


        else:
            player_stand_surf = pygame.image.load(player_stand_path)
            player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)  # (surface, angle, scale)
            player_stand_rect = player_stand_surf.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT / 2))
            screen.blit(score_message, score_message_rect)
            screen.blit(player_stand_surf, player_stand_rect)



    pygame.display.update()
    clock.tick(60)