import pygame
import os

pygame.init()

width, height = 900, 500
screen = pygame.display.set_mode((width, height))
    
pygame.display.set_caption("Jumpie Cat")

logo = pygame.image.load("pic juppiecat/catwallpaper.png")
pygame.display.set_icon(logo)

# เพื่มรูปภาพที่ใช้ในgame

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == '__main__':
    main()
