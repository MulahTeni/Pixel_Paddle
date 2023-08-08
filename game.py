# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

class Player(object):

    def __init__(self, color, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)#pygame.Rect(32, 32, 16, 16)
        self.color = color

    def move(self, d):

        # Move each axis separately. Note that this checks for collisions both times.
        self.rect.y += d


player1_pos = pygame.Vector2(41, screen.get_height()/2 - 50)
player2_pos = pygame.Vector2(screen.get_width() - 41, screen.get_height()/2 - 50)
target_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

player1 = Player("red", player1_pos)
player2 = Player("blue", player2_pos)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    #pygame.draw.rect(screen, "red", (player1_pos[0], player1_pos[1], 20, 100))
    #pygame.draw.rect(screen, "blue", (player2_pos[0], player2_pos[1], 20, 100))
    pygame.draw.circle(screen, "black", target_pos, 40)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_w]:
        player1.move(-2)
    if keys[pygame.K_s]:
        player1.move(2)

    if keys[pygame.K_UP]:
        player2.move(-2)
    if keys[pygame.K_DOWN]:
        player2.move(2)

    pygame.draw.rect(screen, player1.color, player1.rect)
    pygame.draw.rect(screen, player2.color, player2.rect)
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
