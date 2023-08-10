import pygame
import random

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


    def __del__(self):
        pass

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
            player2.score += 1
            return True

        if self.rect.colliderect(walls[3].rect):
            player1.score += 1
            return True

        if self.rect.colliderect(player1.rect):
            self.x_coor = player1.rect.right + self.radius
            self.x_vel = abs(self.x_vel)

        if self.rect.colliderect(player2.rect):
            self.x_coor = player2.rect.left - self.radius
            self.x_vel = -abs(self.x_vel)

        return False

# Outer Frame
class Frame(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos)



# Game setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

walls = []
player1 = Player("red", (40, screen.get_height()/2 - 60))
player2 = Player("blue", (screen.get_width() - 60, screen.get_height()/2 - 60))


def menu():

    background_color = (149, 225, 211)
    light_button_color = (234, 255, 208)
    dark_button_color = (252, 227, 138)
    light_text_color = (243, 129, 129)
    dark_text_color = (243, 189, 189)

    title_font = pygame.font.SysFont('Consolas', 80)
    button_font = pygame.font.SysFont('Consolas', 40)

    title_text = title_font.render('PONG GAME', True, light_text_color)

    light_button_text_0 = button_font.render('Player VS Player', True, light_text_color)
    dark_button_text_0 = button_font.render('Player VS Player', True, dark_text_color)

    light_button_text_1 = button_font.render('Player VS AI', True, light_text_color)
    dark_button_text_1 = button_font.render('Player VS AI', True, dark_text_color)

    light_button_text_2 = button_font.render('QUIT', True, light_text_color)
    dark_button_text_2 = button_font.render('QUIT', True, dark_text_color)


    running = True
    while running:

        for ev in pygame.event.get():
            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN and (screen.get_width()/2-210 <= mouse[0] <= screen.get_width()/2+120 and screen.get_height()/2-50<= mouse[1] <= screen.get_height()/2):
                playerVsPlayer()
            if ev.type == pygame.MOUSEBUTTONDOWN and (screen.get_width()/2-180 <= mouse[0] <= screen.get_width()/2+120 and screen.get_height()/2+200<= mouse[1] <= screen.get_height()/2+250):
                running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

        mouse = pygame.mouse.get_pos()

        # Button 0
        if screen.get_width()/2-210 <= mouse[0] <= screen.get_width()/2+120 and screen.get_height()/2-50<= mouse[1] <= screen.get_height()/2:
            pygame.draw.rect(screen, light_button_color, [screen.get_width()/2-210, screen.get_height()/2 - 50, 360, 50])
            screen.blit(light_button_text_0, (screen.get_width()/2-205, screen.get_height()/2 - 48))
        else:
            pygame.draw.rect(screen, dark_button_color, [screen.get_width()/2-210, screen.get_height()/2 - 50, 360, 50])
            screen.blit(dark_button_text_0, (screen.get_width()/2-205, screen.get_height()/2 - 48))

        # Button 1
        if screen.get_width()/2-180 <= mouse[0] <= screen.get_width()/2+120 and screen.get_height()/2+75<= mouse[1] <= screen.get_height()/2+125:
            pygame.draw.rect(screen, light_button_color, [screen.get_width()/2-180, screen.get_height()/2+75, 300, 50])
            screen.blit(light_button_text_1, (screen.get_width()/2-180, screen.get_height()/2+75))
        else:
            pygame.draw.rect(screen, dark_button_color, [screen.get_width()/2-180, screen.get_height()/2+75, 300, 50])
            screen.blit(dark_button_text_1, (screen.get_width()/2-180, screen.get_height()/2+75))

        # Button 2
        if screen.get_width()/2-180 <= mouse[0] <= screen.get_width()/2+120 and screen.get_height()/2+200<= mouse[1] <= screen.get_height()/2+250:
            pygame.draw.rect(screen, light_button_color, [screen.get_width()/2-180, screen.get_height()/2 +200, 300, 50])
            screen.blit(light_button_text_2, (screen.get_width()/2-180, screen.get_height()/2+200))
        else:
            pygame.draw.rect(screen, dark_button_color, [screen.get_width()/2-180, screen.get_height()/2+200, 300, 50])
            screen.blit(dark_button_text_2, (screen.get_width()/2-180, screen.get_height()/2+200))

        screen.blit(title_text, (screen.get_width()/2-240, 60))



        pygame.display.flip()


def playerVsPlayer():

    ball = Ball()
    frame = [[0, 0, screen.get_width(), 10], [0, screen.get_height()-9, screen.get_width(), 10],
                [0, 0, 10, screen.get_height()], [screen.get_width()-9, 0, 10, screen.get_height()]]

    for wall in frame:
        Frame(wall)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        for i, wall in enumerate(walls):
            if i < 2:
                wall_color = "purple"
            else:
                wall_color = "green"
            pygame.draw.rect(screen, wall_color, wall.rect)

        pygame.draw.rect(screen, player1.color, player1.rect)
        pygame.draw.rect(screen, player2.color, player2.rect)

        pygame.draw.circle(screen, "black", ball.centre, ball.radius)

        font = pygame.font.Font(None, 36)
        p1_score_text = font.render(f'{player1.score}', True, (0, 0, 0))
        p2_score_text = font.render(f'{player2.score}', True, (0, 0, 0))

        screen.blit(p1_score_text, (20, 20))
        screen.blit(p2_score_text, (screen.get_width()-270, 20))

        if ball.auto_move():
            del ball
            ball = Ball()

        # Display work on screen
        pygame.display.flip()
        dt = clock.tick(60) / 1000

menu()
pygame.quit()
