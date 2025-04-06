import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Directional Movement")

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Circle properties
circle_x = 100  # Initial x position
circle_y = HEIGHT // 2  # Initial y position
radius = 10

# Velocity
speed = 1  # Constant speed
angle = 0  # Initial angle in radians

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)  # Clear screen
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control direction with UP & DOWN arrows
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:  
        angle -= 0.05  # Turn upward (rotate counterclockwise)
    if keys[pygame.K_DOWN]:  
        angle += 0.05  # Turn downward (rotate clockwise)

    # Convert angle to velocity components
    vx = speed * math.cos(angle)  # x velocity
    vy = speed * math.sin(angle)  # y velocity

    # Update position
    circle_x += vx
    circle_y += vy

    # Draw circle
    pygame.draw.circle(screen, BLUE, (int(circle_x), int(circle_y)), radius)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.quit()
