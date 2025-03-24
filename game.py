import pygame
import random
import time
import math

# Initialize pygame
# pygame.init()
# import pygame
import asyncio

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)
text = font.render("Click to Start", True, (255, 255, 255))

async def main():
    screen.fill((0, 0, 0))
    screen.blit(text, (250, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False  # Start game on click

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0) # Required for Pygbag

asyncio.run(main())

# Screen settings
WIDTH, HEIGHT = 900, 642
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Collecting Game")

# Load images
bg_img = pygame.image.load("table.jpg")  # Background table image
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

stick_img = pygame.image.load("stick.jpg")  # Stick image
stick_img = pygame.transform.scale(stick_img, (15, 125))  # Resize stick

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 0)
BLACK = (0, 0, 0)

# Stick settings
stick_x, stick_y = WIDTH // 2, HEIGHT - 120
stick_speed = 9
stick_thrown = False
stick_y_movement = 0

# Ball settings
balls = []
ball_spawn_delay = 1000  # New ball every 1 second
last_ball_spawn_time = pygame.time.get_ticks()

# Timer
start_time = time.time()
game_duration = 60  # 1-minute game

# Score
score = 0

# Frame rate control
clock = pygame.time.Clock()

# Function to create a new ball
def create_ball():
    angle = random.uniform(0, 2 * math.pi)  # Random movement direction
    speed = random.uniform(2, 4)  # Random speed
    return {
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, HEIGHT // 2),
        "radius": 15,
        "dx": speed * math.cos(angle),
        "dy": speed * math.sin(angle),
        "value": random.randint(1, 10),
        "rotation": 0,  # Spin effect
        "rotation_speed": random.choice([-5, 5]),  # Direction of spin
    }

# Main game loop
running = True
while running:
    screen.blit(bg_img, (0, 0))  # Draw wooden table background

    # Timer
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_duration - int(elapsed_time))
    
    if remaining_time == 0:
        running = False
    
    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move stick
    if keys[pygame.K_LEFT] and stick_x > 0:
        stick_x -= stick_speed
    if keys[pygame.K_RIGHT] and stick_x < WIDTH - 50:
        stick_x += stick_speed
    if keys[pygame.K_SPACE] and not stick_thrown:
        stick_thrown = True
        stick_y_movement = -10

    # Move stick upwards
    if stick_thrown:
        stick_y += stick_y_movement
        if stick_y <= 0:
            stick_thrown = False
            stick_y = HEIGHT - 120

    # Spawn new balls
    current_time = pygame.time.get_ticks()
    if current_time - last_ball_spawn_time > ball_spawn_delay:
        balls.append(create_ball())
        last_ball_spawn_time = current_time

    # Move and bounce balls
    for ball in balls[:]:
        ball["x"] += ball["dx"]
        ball["y"] += ball["dy"]
        ball["rotation"] += ball["rotation_speed"]  # Spin effect

        # Bounce off walls
        if ball["x"] <= 0 or ball["x"] >= WIDTH:
            ball["dx"] *= -1
        if ball["y"] <= 0 or ball["y"] >= HEIGHT // 2:
            ball["dy"] *= -1

        # Speed increase over time
        ball["dx"] *= 1.001
        ball["dy"] *= 1.001

        # Check collision with stick
        if stick_thrown and abs(stick_x - ball["x"]) < 20 and abs(stick_y - ball["y"]) < 20:
            score += ball["value"]
            balls.remove(ball)
            stick_thrown = False
            stick_y = HEIGHT - 120

    # Draw balls with rotation effect
    for ball in balls:
        pygame.draw.circle(screen, BLUE, (int(ball["x"]), int(ball["y"])), ball["radius"])
        font = pygame.font.Font(None, 25)
        text = font.render(str(ball["value"]), True, WHITE)
        rotated_text = pygame.transform.rotate(text, ball["rotation"])  # Rotate text for spin effect
        screen.blit(rotated_text, (ball["x"] - 8, ball["y"] - 8))

    # Draw stick image
    screen.blit(stick_img, (stick_x, stick_y))
    
    # Display timer and score
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (10, 50))
    
    pygame.display.flip()
    clock.tick(60)  # Limit frame rate to 60 FPS

# End screen
screen.fill(WHITE)
font = pygame.font.Font(None, 50)
end_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
screen.blit(end_text, (WIDTH // 4, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(3000)
pygame.quit()
