import pygame
import sys
#test
pygame.init()

screen_width = 800
screen_height = 600

circle_radius = 25
circle_x = screen_width // 2
circle_y = screen_height // 2

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

while True:
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), circle_radius)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                circle_y -= 20
            elif event.key == pygame.K_DOWN:
                circle_y += 20
            elif event.key == pygame.K_LEFT:
                circle_x -= 20
            elif event.key == pygame.K_RIGHT:
                circle_x += 20

    circle_x = max(circle_radius, min(circle_x, screen_width - circle_radius))
    circle_y = max(circle_radius, min(circle_y, screen_height - circle_radius))

    clock.tick(30)