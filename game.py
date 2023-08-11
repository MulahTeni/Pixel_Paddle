import pygame
import random

pygame.init()

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_render = text_font.render(self.text, True, "white")
        text_rect = text_render.get_rect(center=self.rect.center)
        surface.blit(text_render, text_rect)


WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20

player1_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
player_score = 0
opponent_score = 0

start_ball_speed = [5, 5]
ball_speed = list(start_ball_speed)

text_font = pygame.font.Font(None, 36)
paused_font = pygame.font.Font(None, 72)
paused_text = paused_font.render("Game Paused", True, "blue")

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60

menu_active = True
player_vs_player = False
game_over = False
game_paused = False


clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif not menu_active and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_paused = not game_paused

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if return_to_menu_button.rect.collidepoint(event.pos):
                    player_score = 0
                    opponent_score = 0
                    game_over = False
                    player1_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                    player2_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    ball_speed = list(start_ball_speed)
                    menu_active = True
            elif game_paused:
                if return_to_menu_button.rect.collidepoint(event.pos):
                    game_paused = not game_paused
                    player_score = 0
                    opponent_score = 0
                    game_over = False
                    player1_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                    player2_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    ball_speed = list(start_ball_speed)
                    menu_active = True

                if paused_button.rect.collidepoint(event.pos):
                    game_paused = not game_paused
            else:
                if play_button.rect.collidepoint(event.pos):
                    menu_active = False
                elif pvp_button.rect.collidepoint(event.pos):
                    menu_active = False
                    player_vs_player = True
                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()


    if menu_active:
        player_vs_player = False
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Pixel Paddle", True, "red")
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        win.fill((0,0,0))
        win.blit(title_text, title_rect)
        play_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 60, BUTTON_WIDTH, BUTTON_HEIGHT, "Play", "blue")
        pvp_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 10, BUTTON_WIDTH, BUTTON_HEIGHT, "Player vs. Player", "blue")
        exit_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 80, BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", "blue")
        play_button.draw(win)
        pvp_button.draw(win)
        exit_button.draw(win)

    else:
        if game_over:
            win.fill("white")

            winner_font = pygame.font.Font(None, 48)
            if player_score >= 5:
                winner_text = winner_font.render("Player Wins!", True, "blue")
            else:
                winner_text = winner_font.render("Bot Wins!", True, "blue")
            winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            win.blit(winner_text, winner_rect)

            return_to_menu_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, "Return to Menu", "blue")
            return_to_menu_button.draw(win)

        else:
            if not game_paused:
                keys = pygame.key.get_pressed()
                if player_vs_player:
                    if keys[pygame.K_UP] and player2_paddle.top > 0:
                        player2_paddle.y -= 5
                    if keys[pygame.K_DOWN] and player2_paddle.bottom < HEIGHT:
                        player2_paddle.y += 5
                    if keys[pygame.K_w] and player1_paddle.top > 0:
                        player1_paddle.y -= 5
                    if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
                        player1_paddle.y += 5
                else:
                    if keys[pygame.K_w] and player1_paddle.top > 0:
                        player1_paddle.y -= 5
                    if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
                        player1_paddle.y += 5

                    if ball_speed[0] > 0:
                        predicted_y = ball.y + (player2_paddle.centerx - ball.centerx) * ball_speed[1] / ball_speed[0]

                        time_to_reach_predicted = abs(predicted_y - player2_paddle.centery) / 5

                        predicted_ball_x = ball.centerx + ball_speed[0] * time_to_reach_predicted
                        predicted_ball_y = ball.centery + ball_speed[1] * time_to_reach_predicted

                        while predicted_ball_y < 0 or predicted_ball_y > HEIGHT:
                            if predicted_ball_y < 0:
                                predicted_ball_y = -predicted_ball_y
                            else:
                                predicted_ball_y = 2 * HEIGHT - predicted_ball_y

                        if predicted_ball_y < player2_paddle.centery and player2_paddle.top>0:
                            player2_paddle.y -= 5
                        elif predicted_ball_y > player2_paddle.centery and player2_paddle.bottom<HEIGHT:
                            player2_paddle.y += 5
                    else:
                        vel = 5
                        if abs(player2_paddle.centery - HEIGHT/2) < 5:
                            vel = player2_paddle.centery - HEIGHT/2
                        if player2_paddle.centery < HEIGHT/2:
                            player2_paddle.y += vel
                        else:
                            player2_paddle.y -= vel

                ball.x += ball_speed[0]
                ball.y += ball_speed[1]

                if abs(ball_speed[0]) < 15:
                    ball_speed[0] *= 1.001
                if abs(ball_speed[1]) < 15:
                    ball_speed[1] *= 1.001

                if ball.top <= 0 or ball.bottom >= HEIGHT:
                    ball_speed[1] = -ball_speed[1]

                if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
                    ball_speed[0] = -ball_speed[0]
                    if ball.colliderect(player1_paddle):
                        ball.left = player1_paddle.right
                    elif ball.colliderect(player2_paddle):
                        ball.right = player2_paddle.left



                if ball.left <= 0:
                    opponent_score += 1
                    ball_speed = list((random.randint(2,5), random.randint(1,4)))
                    num = 1 if random.random() > 0.5 else -1
                    ball_speed[0] *= num
                    num = 1 if random.random() > 0.5 else -1
                    ball_speed[1] *= num
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                if ball.right >= WIDTH:
                    player_score += 1
                    ball_speed = list((random.randint(2,5), random.randint(1,4)))
                    num = 1 if random.random() > 0.5 else -1
                    ball_speed[0] *= num
                    num = 1 if random.random() > 0.5 else -1
                    ball_speed[1] *= num
                    ball.center = (WIDTH // 2, HEIGHT // 2)



            win.fill("white")
            pygame.draw.rect(win, "red", player1_paddle)
            pygame.draw.rect(win, "red", player2_paddle)
            pygame.draw.ellipse(win, "red", ball)
            pygame.draw.aaline(win, "red", (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

            if game_paused:
                win.blit(paused_text, paused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))
                paused_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 60, BUTTON_WIDTH, BUTTON_HEIGHT, "Resume", "blue")
                paused_button.draw(win)
                return_to_menu_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 10, BUTTON_WIDTH, BUTTON_HEIGHT, "Return to Menu", "blue")
                return_to_menu_button.draw(win)



            player_text = text_font.render(f"Player: {player_score}", True, "red")
            opponent_text = text_font.render(f"Opponent: {opponent_score}", True, "red")
            win.blit(player_text, (20, 20))
            win.blit(opponent_text, (WIDTH - opponent_text.get_width() - 20, 20))

            if player_score >= 5 or opponent_score >= 5:
                game_over = True


    pygame.display.update()
    clock.tick(60)


pygame.quit()
