import pygame
import os
import random
import datetime
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Jumppie Cat")

LOGO = pygame.image.load("Assets/catwallpaper.png")

pygame.display.set_icon(LOGO)

RUNNING = [pygame.image.load(os.path.join("Assets/cat", "CatRun1.png")),
           pygame.image.load(os.path.join("Assets/cat", "CatRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/cat", "CatJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/cat", "CatDuck1.png")),
           pygame.image.load(os.path.join("Assets/cat", "CatDuck2.png"))]

TREE = [pygame.image.load(os.path.join("Assets/obstruction", "tree1.png")),
        pygame.image.load(os.path.join("Assets/obstruction", "tree2.png")),
        pygame.image.load(os.path.join("Assets/obstruction", "tree3.png"))]

BEE = [pygame.image.load(os.path.join("Assets/obstruction", "bee1.png")),
       pygame.image.load(os.path.join("Assets/obstruction", "bee2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "cloud.png"))

STONE = [pygame.image.load(os.path.join("Assets/obstruction", "stone2.png")),
        pygame.image.load(os.path.join("Assets/obstruction", "stone3.png"))]


BG = pygame.image.load(os.path.join("Assets/Other", "map.png"))
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255 , 255)
GRAY = (128, 128, 128)
BLUE = (226, 247, 252)
GREEN = (108, 196, 161)
CARAMEL = (247, 233, 215)

class Cat:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 350
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.cat_duck = False
        self.cat_run = True
        self.cat_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X_POS
        self.cat_rect.y = self.Y_POS

    def update(self, userinput):
        if self.cat_duck:
            self.duck()
        if self.cat_run:
            self.run()
        if self.cat_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userinput[pygame.K_UP] or userinput[pygame.K_SPACE] or userinput[pygame.K_w]) and not self.cat_jump:
            self.cat_duck = False
            self.cat_run = False
            self.cat_jump = True
        elif (userinput[pygame.K_DOWN] or userinput[pygame.K_s]) and not self.cat_jump:
            self.cat_duck = True
            self.cat_run = False
            self.cat_jump = False
        elif not (self.cat_jump or userinput[pygame.K_DOWN]):
            self.cat_duck = False
            self.cat_run = True
            self.cat_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X_POS
        self.cat_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.cat_rect = self.image.get_rect()
        self.cat_rect.x = self.X_POS
        self.cat_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.cat_jump:
            self.cat_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.cat_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.cat_rect.x, self.cat_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Tree(obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class Stone(obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 370

class Bee(obstacle):
    BEE_HEIGHTS = [250, 290, 350]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BEE_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Cat()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 400
    points = 0
    font = pygame.font.Font(os.path.join("Assets/FreeSansBold.ttf"), 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed, current_time
        points += 1
        if points % 200 == 0:
            game_speed += 0.5
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]
            highscore = max(score_ints)
            if points > highscore:
                highscore = points
            text = font.render("High Score: " + str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textrect = text.get_rect()
        textrect.center = (900, 40)
        SCREEN.blit(text, textrect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            SCREEN.fill(WHITE)
        else:
            SCREEN.fill(BLUE)
        userinput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userinput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Tree(TREE))
            elif random.randint(0, 2) == 1:
                obstacles.append(Bee(BEE))
            elif random.randint(0, 2) == 2:
                obstacles.append(Stone(STONE))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.cat_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(FPS)
        pygame.display.update()

def menu(death_count):
    global points, FONT_COLOR
    run = True
    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
           FONT_COLOR = BLACK
           SCREEN.fill(WHITE)
        else:
            FONT_COLOR = BLACK
            SCREEN.fill(GREEN)
        font = pygame.font.Font(os.path.join("Assets/FreeSansBold.ttf"), 30)

        if death_count == 0:
            text = font.render("Press any Key to Strat", True, FONT_COLOR)
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, FONT_COLOR)
            score = font.render("Your Score: " + str(points), True, FONT_COLOR)
            scorerect = score.get_rect()
            scorerect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scorerect)
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            with open("score.txt", "r") as f:
                score = (f.read())
                score_ints = [int(x) for x in score.split()]
            highscore = max(score_ints)
            hs_score_text = font.render("High Score : " + str(highscore), True, FONT_COLOR)
            hs_score_rect = hs_score_text.get_rect()
            hs_score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(hs_score_text, hs_score_rect)
        textrect = text.get_rect()
        textrect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textrect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count = 0)
