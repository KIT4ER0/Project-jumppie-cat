import pygame
import os

pygame.init()

fps = 60
width, height = 900, 500
screen = pygame.display.set_mode((width, height))
    
pygame.display.set_caption("Jumpie Cat")

logo = pygame.image.load("pic juppiecat/cat run up right.png")
pygame.display.set_icon(logo)

# เพื่มรูปภาพที่ใช้ในgame

font_color = (0, 0, 0)

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == '__main__':
    main()
