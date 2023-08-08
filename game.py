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
        # If you collide with a wall, move out based on velocity
        if self.rect.colliderect(walls[0].rect):
            # Moving up; Hit the bottom side of the wall
            self.rect.bottom = walls[1].rect.top + 1

        if self.rect.colliderect(walls[1].rect):
            # Moving down; Hit the top side of the wall
            self.rect.top = walls[0].rect.bottom + 1


# Ball class
class Ball(object):
    def __init__(self):
        self.cir = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.radius = 15

# Outer Frame
class Frame(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos)



# Game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = 0

player1 = Player("red", (40, screen.get_height()/2 - 60))
player2 = Player("blue", (screen.get_width() - 60, screen.get_height()/2 - 60))

ball = Ball()

frame = [[0, 0, screen.get_width(), 10], [0, screen.get_height()-9, screen.get_width(), 10],
            [0, 0, 10, screen.get_height()], [screen.get_width()-9, 0, 10, screen.get_height()]]

walls = []

for wall in frame:
    Frame(wall)



running = True

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

    i=0
    for wall in walls:
        if i<2:
            i += 1
            pygame.draw.rect(screen, "purple", wall.rect)
        else:
            pygame.draw.rect(screen, "green", wall.rect)

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
