import pygame
import datetime

COLOR_BACK = (250, 255, 255)

pygame.display.set_caption("Mickey Clock")
screen = pygame.display.set_mode((800, 800))

main_clock = pygame.image.load("/Users/nurislambekbolat/Desktop/pp2/lab7/clock.png")
left_hand = pygame.image.load("/Users/nurislambekbolat/Desktop/pp2/lab7/leftarm.png")
right_hand = pygame.image.load("/Users/nurislambekbolat/Desktop/pp2/lab7/rightarm.png")

left_hand = pygame.transform.rotate(left_hand, 90)
right_hand = pygame.transform.rotate(right_hand, 90)

screen.fill(COLOR_BACK)


def blitRotateCenter(surf, image, center, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center)
    surf.blit(rotated_image, new_rect)


clock = pygame.time.Clock()

clock_center = (screen.get_width() // 2, screen.get_height() // 2)

l_center = (400, 400)
r_center = (400, 400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill(COLOR_BACK)

    clock_x = clock_center[0] - main_clock.get_width() // 2
    clock_y = clock_center[1] - main_clock.get_height() // 2
    screen.blit(main_clock, (clock_x, clock_y))

    time = datetime.datetime.now()
    minute_angle = (time.minute % 60) * 6
    second_angle = (time.second % 60) * 6

    blitRotateCenter(screen, left_hand, l_center, 180 - second_angle)
    blitRotateCenter(screen, right_hand, r_center, minute_angle)
    pygame.display.flip()
    clock.tick(60)