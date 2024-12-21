import pygame
import sounddevice as sd
import numpy as np
import random
import sys

# Pygame initialisieren
pygame.init()

# Bildschirm erstellen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scream like a monkey")

icon = pygame.image.load("image/monkey.png")
pygame.display.set_icon(icon)

display = pygame.image.load("image/display.png")

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Spieler-Variablen
player_x, player_y = WIDTH // 2, HEIGHT/2
player_size = 100
player_velocity = 0
gravity = 1
player = pygame.image.load("image/monkey.png")

point = 0

pipe_x = 800
pipe_y = random.randint(150,500)
pipe_speed = 10
pipe_1 = pygame.image.load("image/tree.png")

# Geräusch-Erkennung
def sound_callback(indata, frames, time, status):
    global player_velocity
    volume = np.linalg.norm(indata)  # Berechnet die Lautstärke
    if volume > 0.05:  # Schwellenwert für Geräusch
        player_velocity = -20  # Spieler springt


stream = sd.InputStream(callback=sound_callback, channels=1, samplerate=44100)
stream.start()

def text(surface, text, x, y, size):
    font = pygame.font.Font("image/font.ttf", size)
    rendered_text = font.render(text, True, (0,0,0))
    text_rect = rendered_text.get_rect(center=(x, y))
    surface.blit(rendered_text, text_rect)

main_run = True
while main_run:

    second_run = True
    while second_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    second_run = False
                    point = 0

        text(screen,"scream like a monkey",400,100,75)
        text(screen, "press a to play", 200, 250, 50)
        if point != 0:
            text(screen,str(point),150,400,100)

        screen.blit(display,(0,0))

        pygame.display.update()






# Hauptspiel-Schleife
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # Ereignisse prüfen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Physik
        player_velocity += gravity
        player_y += player_velocity


        pipe_x -= pipe_speed
        screen.blit(pipe_1,(pipe_x,pipe_y))
        if pipe_x < 0:
            pipe_x = 800
            pipe_y = random.randint(150,500)
        pipe_rect = pygame.Rect(pipe_x,pipe_y,100,700)




        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        screen.blit(player,(player_x, player_y))

        if (pipe_rect.colliderect(player_rect) or player_y < -100 or player_y > 550):
            pipe_x = 800
            player_y = HEIGHT/2
            player_velocity = -20
            running = False

        text(screen,str(point),400,50,60)

        # Bildschirm aktualisieren
        pygame.display.flip()
        clock.tick(30)
        point += 1

# Ressourcen freigeben
stream.stop()
stream.close()
pygame.quit()
