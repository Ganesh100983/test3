import pygame, sys, random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simple Pinball')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [random.choice([-4, 4]), -5]

# Flipper (paddle) properties
flipper_width, flipper_height = 100, 20
flipper_speed = 7
flipper_rect = pygame.Rect((WIDTH // 2 - flipper_width // 2, HEIGHT - 50), (flipper_width, flipper_height))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and flipper_rect.left > 0:
        flipper_rect.x -= flipper_speed
    if keys[pygame.K_RIGHT] and flipper_rect.right < WIDTH:
        flipper_rect.x += flipper_speed

    # Move ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Wall collision
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= WIDTH:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] - ball_radius <= 0:
        ball_vel[1] = -ball_vel[1]

    # Flipper collision
    if flipper_rect.collidepoint(ball_pos[0], ball_pos[1] + ball_radius):
        ball_vel[1] = -abs(ball_vel[1])
        # Add a little horizontal change based on where it hits
        offset = (ball_pos[0] - flipper_rect.centerx) / (flipper_width / 2)
        ball_vel[0] += offset * 2
        score += 1

    # Bottom collision (lose)
    if ball_pos[1] - ball_radius > HEIGHT:
        # Reset ball
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_vel = [random.choice([-4, 4]), -5]
        score = 0

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.draw.rect(screen, WHITE, flipper_rect)
    score_surf = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surf, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
