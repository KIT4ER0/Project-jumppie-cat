import pygame
import os
import random

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

CLOUD = pygame.image.load(os.path.join("Assets/Other", "cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "map.png"))

FPS = 60
GRAY = (169, 169, 169)
WHITE = (255, 255 , 255)

class Cat:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
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
            
        if (userinput[pygame.K_UP] or userinput[pygame.K_SPACE]) and not self.cat_jump:
            self.cat_duck = False
            self.cat_run = False
            self.cat_jump = True
        elif userinput[pygame.K_DOWN] and not self.cat_jump:
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

def main():
    global game_speed, x_pos_bg, y_pos_bg, points
    run = True
    clock = pygame.time.Clock()
    player = Cat()
    cloud = Cloud()
    game_speed = 5
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        
        text = font.render("Points: " + str(points), True, WHITE)
        textrect = text.get_rect()
        textrect.center = (1000, 40)
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
        
        SCREEN.fill(GRAY)
        userinput = pygame.key.get_pressed()
        
        player.draw(SCREEN)
        player.update(userinput)
        
        background()
        
        cloud.draw(SCREEN)
        cloud.update()
        
        score()
        
        clock.tick(FPS)
        pygame.display.update()

main()
