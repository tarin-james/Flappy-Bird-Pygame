import pygame
from sys import exit
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()
clock = pygame.time.Clock()

# Window settings
win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

# Images
bird_image = pygame.image.load("images/bird_mid.png")
skyline_image = pygame.image.load("images/background.png")
ground_image = pygame.image.load("images/ground.png")
top_pipe_image = pygame.image.load("images/pipe_top.png")
bottom_pipe_image = pygame.image.load("images/pipe_bottom.png")
game_over_image = pygame.image.load("images/game_over.png")
start_image = pygame.image.load("images/start.png")

# Sounds
score_sound = pygame.mixer.Sound('sound/score.mp3')
flap_sound = pygame.mixer.Sound('sound/flap.mp3')

# Game Settings
scroll_speed = 1
bird_start_position = (100, 250)
score = 0
font = pygame.font.SysFont('Segoe', 26)
game_stopped = True

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect(center=bird_start_position)
        self.vel = 0
        self.flap = False
        self.alive = True

    # Update bird position and handle user input
    def update(self, user_input):
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7
            flap_sound.play()
        if self.vel == 0:
            self.flap = False

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pipe_type = pipe_type
        self.passed = False

    # Move pipes and handle scoring
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()
        global score
        if self.pipe_type == 'bottom':
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.passed = True
                score_sound.play()
                score += 1

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ground_image
        self.rect = self.image.get_rect(topleft=(x, y))

    # Move ground to create scrolling effect
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

# Handle quitting the game
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Main game loop
def main():
    global score

    bird = pygame.sprite.GroupSingle(Bird())
    pipes = pygame.sprite.Group()
    ground = pygame.sprite.Group(Ground(0, 520))

    pipe_timer = 0
    run = True
    while run:
        quit_game()

        window.fill((0, 0, 0))
        user_input = pygame.key.get_pressed()

        window.blit(skyline_image, (0, 0))

        if len(ground) <= 2:
            ground.add(Ground(win_width, 520))

        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        window.blit(score_text, (20, 20))

        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        if pygame.sprite.spritecollideany(bird.sprite, pipes) or pygame.sprite.spritecollideany(bird.sprite, ground):
            bird.sprite.alive = False
            if pygame.sprite.spritecollideany(bird.sprite, ground):
                window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2, win_height // 2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    score = 0
                    break

        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, 'bottom'))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()

# Display the menu
def menu():
    global game_stopped

    while game_stopped:
        quit_game()

        window.fill((0, 0, 0))
        window.blit(skyline_image, (0, 0))
        window.blit(ground_image, (0, 520))
        window.blit(bird_image, (100, 250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2, win_height // 2 - start_image.get_height() // 2))

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()

menu()
