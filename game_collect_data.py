import pygame
import random
import pandas as pd


# Velocity of ball
def velocity_generate():

    number = random.randint(-100, 100)
    if number < 0:
        number -= random.randint(200, 300)
    else:
        number += random.randint(200, 300)

    return number


# Update velocity through time
def update_velocity(velocity):

    if velocity<0:
        velocity -= random.random()
    else:
        velocity += random.random()

    return velocity


# Player class
class Player(object):

    def __init__(self, color, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 120)
        self.color = color
        self.score = 0

    def move(self, d):
        self.rect.y += d
        if self.rect.colliderect(walls[0].rect):
            self.rect.bottom = walls[1].rect.top - 1

        if self.rect.colliderect(walls[1].rect):
            self.rect.top = walls[0].rect.bottom + 1


# Ball class
class Ball(object):

    def __init__(self):
        self.x_coor = screen.get_width() / 2
        self.y_coor = screen.get_height() / 2
        self.centre = pygame.Vector2(self.x_coor, self.y_coor)
        self.radius = 15

        self.x_vel = velocity_generate()
        self.y_vel = velocity_generate()

        self.rect = pygame.Rect(self.x_coor - self.radius, self.y_coor - self.radius, self.radius * 2, self.radius * 2)



    def auto_move(self):
        self.x_vel = update_velocity(self.x_vel)
        self.y_vel = update_velocity(self.y_vel) - 0.1

        self.x_coor += int(self.x_vel * dt)
        self.y_coor += int(self.y_vel * dt)
        self.centre = pygame.Vector2(self.x_coor, self.y_coor)

        self.rect.center = self.centre

        if self.rect.colliderect(walls[0].rect):
            self.y_coor = walls[0].rect.bottom + self.radius
            self.y_vel = abs(self.y_vel)

        if self.rect.colliderect(walls[1].rect):
            self.y_coor = walls[1].rect.top - self.radius
            self.y_vel = -abs(self.y_vel)

        if self.rect.colliderect(walls[2].rect):
            player_blue.score += 1
            return True

        if self.rect.colliderect(walls[3].rect):
            player_red.score += 1
            return True

        if self.rect.colliderect(player_red.rect):
            self.x_coor = player_red.rect.right + self.radius
            self.x_vel = abs(self.x_vel)

        if self.rect.colliderect(player_blue.rect):
            self.x_coor = player_blue.rect.left - self.radius
            self.x_vel = -abs(self.x_vel)

        return False


# Outer Frame
class Frame(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos)


pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

walls = []
player_red = Player("red", (40, screen.get_height()/2 - 60))
player_blue = Player("blue", (screen.get_width() - 60, screen.get_height()/2 - 60))

data = [("ball.x_coor", "ball.y_coor", "ball.x_vel", "ball.y_vel", "player_blue.rect.y", "player_action")]

ball = Ball()
frame = [[0, 0, screen.get_width(), 10], [0, screen.get_height()-9, screen.get_width(), 10],
            [0, 0, 10, screen.get_height()], [screen.get_width()-9, 0, 10, screen.get_height()]]

for wall in frame:
    Frame(wall)


running2 = True
while running2:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running2 = False

    keys = pygame.key.get_pressed()

    player_action = 0
    if keys[pygame.K_ESCAPE]:
        running2 = False
    if keys[pygame.K_w]:
        player_red.move(-300 * dt)
    if keys[pygame.K_s]:
        player_red.move(300 * dt)
        player_action = 1
    if keys[pygame.K_UP]:
        player_blue.move(-300 * dt)
        player_action = 2
    if keys[pygame.K_DOWN]:
        player_blue.move(300 * dt)

    data.append((ball.x_coor, ball.y_coor, ball.x_vel, ball.y_vel, player_blue.rect.y, player_action))

    screen.fill("white")

    for i, wall in enumerate(walls):
        if i < 2:
            wall_color = "purple"
        else:
            wall_color = "green"
        pygame.draw.rect(screen, wall_color, wall.rect)

    pygame.draw.rect(screen, player_red.color, player_red.rect)
    pygame.draw.rect(screen, player_blue.color, player_blue.rect)
    pygame.draw.circle(screen, "black", ball.centre, ball.radius)


    font = pygame.font.Font(None, 36)
    p1_score_text = font.render(f'{player_red.score}', True, (0, 0, 0))
    p2_score_text = font.render(f'{player_blue.score}', True, (0, 0, 0))

    screen.blit(p1_score_text, (20, 20))
    screen.blit(p2_score_text, (screen.get_width()-270, 20))

    if ball.auto_move():
        del ball
        ball = Ball()

    # Display work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)

pygame.quit()
