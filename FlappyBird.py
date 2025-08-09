import pygame
from pygame.locals import *
import random
import sys

# Initialize pygame
pygame.init()

# Game configuration
clock = pygame.time.Clock()
fps = 90
screen_width = 850
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Fonts and colors
font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

# Game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
player_name = ''

# Load images
try:
    bg = pygame.image.load(r"C:\Users\Tab & Tech\Documents\python\practice\FlappyBirdGame-Python\img\bg.png")
    ground_img = pygame.image.load(r"C:\Users\Tab & Tech\Documents\python\practice\FlappyBirdGame-Python\img\ground.png")
    button_img = pygame.image.load(r"C:\Users\Tab & Tech\Documents\python\practice\FlappyBirdGame-Python\img\restart.png")
except Exception as e:
    print("Error loading images:", e)
    pygame.quit()
    sys.exit()

# Groups
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

# Functions
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    global last_pipe, ground_scroll
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    ground_scroll = 0
    return 0

def save_score(name, final_score):
    try:
        with open("flappy_scores.txt", "a") as file:
            file.write(f"{name}: {final_score}\n")
    except Exception as e:
        print("Error saving score:", e)

def get_player_name():
    input_active = True
    name = ""
    input_box = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 40, 400, 80)
    font_input = pygame.font.SysFont('Bauhaus 93', 50)

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "":
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 20:
                        name += event.unicode

        screen.fill((0, 0, 0))
        draw_text("Enter Your Name:", font, white, screen_width // 2 - 200, screen_height // 2 - 150)
        txt_surface = font_input.render(name, True, white)
        input_box.w = max(400, txt_surface.get_width() + 10)
        pygame.draw.rect(screen, pygame.Color('lightskyblue3'), input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 20))
        pygame.display.flip()
        clock.tick(30)

# Classes
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        try:
            for _ in range(3):
                img = pygame.image.load(r"C:\Users\Tab & Tech\Documents\python\practice\FlappyBirdGame-Python\img\bird1.png")
                self.images.append(img)
        except Exception as e:
            print("Error loading bird image:", e)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying:
            self.vel += 0.5
            self.vel = min(self.vel, 8)
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load(r"C:\Users\Tab & Tech\Documents\python\practice\FlappyBirdGame-Python\img\pipe.png")
        except Exception as e:
            print("Error loading pipe image:", e)
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Main game execution
try:
    player_name = get_player_name()

    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy)
    button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

    run = True
    while run:
        clock.tick(fps)
        screen.blit(bg, (0, 0))
        pipe_group.draw(screen)
        bird_group.draw(screen)
        bird_group.update()
        screen.blit(ground_img, (ground_scroll, 768))

        for pipe in pipe_group:
            if flappy.rect.left > pipe.rect.right and not pass_pipe:
                score += 1
                pass_pipe = True

        if pass_pipe and pipe_group and flappy.rect.left > pipe_group.sprites()[0].rect.right:
            pass_pipe = False

        draw_text(str(score), font, white, int(screen_width / 2), 20)

        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
        if flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        if flying and not game_over:
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            pipe_group.update()

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

        if game_over:
            if button.draw():
                save_score(player_name, score)
                game_over = False
                score = reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(player_name, score)
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
                flying = True

        pygame.display.update()

finally:
    pygame.quit()
    print(f"Game ended. Score for {player_name}: {score}")
