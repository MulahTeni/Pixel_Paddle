# Example file showing a circle moving on screen
import pygame
import random


# Player class
class Player(object):
    def __init__(self, color, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 120)
        self.color = color

    def move(self, d):
        self.rect.y += d

# Ball class
class Ball(object):
    def __init__(self):
        self.cir = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.radius = 15

# Outer Frame
class Frame(object):
    def __init__(self):
        self.upper = pygame.Rect(0, 0, screen.get_width(), 10)
        self.lower = pygame.Rect(0, screen.get_height()-9, screen.get_width(), 10)

        self.left = pygame.Rect(0, 0, 10, screen.get_height())
        self.right = pygame.Rect(screen.get_width()-9, 0, 10, screen.get_height())


# Game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player1 = Player("red", (40, screen.get_height()/2 - 60))
player2 = Player("blue", (screen.get_width() - 60, screen.get_height()/2 - 60))

ball = Ball()

frame = Frame()



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")



    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_w]:
        player1.move(-300 * dt)
    if keys[pygame.K_s]:
        player1.move(300 * dt)

    if keys[pygame.K_UP]:
        player2.move(-300 * dt)
    if keys[pygame.K_DOWN]:
        player2.move(300 * dt)


    pygame.draw.rect(screen, "purple", frame.upper)
    pygame.draw.rect(screen, "purple", frame.lower)
    pygame.draw.rect(screen, "green", frame.left)
    pygame.draw.rect(screen, "green", frame.right)

    pygame.draw.rect(screen, player1.color, player1.rect)
    pygame.draw.rect(screen, player2.color, player2.rect)

    pygame.draw.circle(screen, "black", ball.cir, ball.radius)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
