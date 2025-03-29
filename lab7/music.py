import pygame

pygame.init()

HEIGHT = 300
WIDTH = 300
SIZE = (HEIGHT, WIDTH)

SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)
songs = ['/Users/nurislambekbolat/Desktop/pp2/lab7/s_1.mp3',
         '/Users/nurislambekbolat/Desktop/pp2/lab7/s_2.mp3']
next_song = 0
clock = pygame.time.Clock()
pause = False
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Music Player")

# Загружаем и воспроизводим первую песню
pygame.mixer.music.load(songs[next_song])
pygame.mixer.music.play()

while True:
    screen.fill((0, 0, 0))  # Фон черный (можно поменять цвет)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                next_song -= 1
                if next_song < 0:
                    next_song = len(songs) - 1
                pygame.mixer.music.load(songs[next_song])
                pygame.mixer.music.play()

            elif event.key == pygame.K_RIGHT:
                next_song += 1
                if next_song >= len(songs):
                    next_song = 0
                pygame.mixer.music.load(songs[next_song])
                pygame.mixer.music.play()

            elif event.key == pygame.K_SPACE:
                if pause:
                    pause = False
                    pygame.mixer.music.unpause()
                else:
                    pause = True
                    pygame.mixer.music.pause()

    pygame.display.flip()
    clock.tick(60)
