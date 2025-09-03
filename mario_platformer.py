import pygame
import sys
import random

# Initialize pygame - this sets up all the pygame modules we need
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800  # Width of our game window in pixels
WINDOW_HEIGHT = 600  # Height of our game window in pixels
WINDOW_TITLE = "Super Mario Style Platformer"  # Title that appears at the top of the window

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Set up colors (RGB format - Red, Green, Blue, each from 0-255)
WHITE = (255, 255, 255)  # White background
RED = (255, 0, 0)       # Red color for our player
BLACK = (0, 0, 0)       # Black color for text
GREEN = (0, 255, 0)     # Green color for platforms
BLUE = (0, 0, 255)      # Blue color for enemies
BROWN = (139, 69, 19)   # Brown color for ground

# Player properties
player_width = 40   # Width of our player square
player_height = 40  # Height of our player square
player_x = 50       # Starting X position (distance from left edge)
player_y = WINDOW_HEIGHT - player_height - 10  # Starting Y position (near bottom)
player_speed = 6    # How fast the player moves (pixels per frame) - increased from 5
player_velocity_y = 0  # Vertical velocity for jumping
player_on_ground = False  # Whether player is touching the ground
GRAVITY = 0.7       # How fast the player falls - reduced from 0.8
JUMP_STRENGTH = -18 # How high the player jumps - increased from -15

# Platform properties
platforms = [
    pygame.Rect(100, 450, 200, 20),   # Platform 1
    pygame.Rect(400, 350, 200, 20),   # Platform 2
    pygame.Rect(600, 250, 150, 20),   # Platform 3
    pygame.Rect(50, 200, 150, 20),    # Platform 4
    pygame.Rect(300, 150, 150, 20),   # Platform 5 - new platform for better jumping
]

# Enemy properties - slower and better positioned
enemies = [
    {"rect": pygame.Rect(200, WINDOW_HEIGHT - 50, 30, 30), "direction": 1, "speed": 1},  # Slower speed
    {"rect": pygame.Rect(500, 320, 30, 30), "direction": 1, "speed": 0.8},  # Even slower
    {"rect": pygame.Rect(700, 220, 30, 30), "direction": -1, "speed": 1},   # New enemy on higher platform
    {"rect": pygame.Rect(150, 420, 30, 30), "direction": -1, "speed": 1.2}, # Additional enemy
    {"rect": pygame.Rect(600, 320, 30, 30), "direction": 1, "speed": 0.9},  # Another enemy
]

# Game state
score = 0
lives = 3
game_over = False
game_won = False

# Game loop variables
clock = pygame.time.Clock()  # This helps control the game's frame rate
FPS = 60  # Frames per second - how many times we update the game per second

# Font for displaying text
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    """Helper function to draw text on the screen"""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def reset_player():
    """Reset player position and state"""
    global player_x, player_y, player_velocity_y, player_on_ground
    player_x = 50
    player_y = WINDOW_HEIGHT - player_height - 10
    player_velocity_y = 0
    player_on_ground = False

# Main game loop - this runs continuously while the game is running
running = True
while running:
    # Handle events (like key presses, mouse clicks, window close)
    for event in pygame.event.get():
        # Check if the user clicked the X button to close the window
        if event.type == pygame.QUIT:
            running = False
        
        # Handle single key press for jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_on_ground:
                player_velocity_y = JUMP_STRENGTH
                player_on_ground = False
    
    if not game_over:
        # Handle continuous key presses for smooth movement
        keys = pygame.key.get_pressed()  # Get the state of all keys
        
        # Move player left when left arrow key is pressed
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        
        # Move player right when right arrow key is pressed
        if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_width:
            player_x += player_speed
        
        # Apply gravity to player
        player_velocity_y += GRAVITY
        player_y += player_velocity_y
        
        # Create player rectangle for collision detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        # Check collision with ground
        if player_y >= WINDOW_HEIGHT - player_height - 10:
            player_y = WINDOW_HEIGHT - player_height - 10
            player_velocity_y = 0
            player_on_ground = True
        
        # Check collision with platforms
        for platform in platforms:
            if player_rect.colliderect(platform):
                # Landing on top of platform
                if player_velocity_y > 0 and player_y < platform.y:
                    player_y = platform.y - player_height
                    player_velocity_y = 0
                    player_on_ground = True
                # Hitting platform from below
                elif player_velocity_y < 0 and player_y > platform.y:
                    player_y = platform.y + platform.height
                    player_velocity_y = 0
        
        # If player is not on any platform or ground, they're in the air
        if player_velocity_y != 0:
            player_on_ground = False
        
        # Update enemies
        for enemy in enemies:
            # Move enemy
            enemy["rect"].x += enemy["speed"] * enemy["direction"]
            
            # Change direction when hitting edges
            if enemy["rect"].x <= 0 or enemy["rect"].x >= WINDOW_WIDTH - enemy["rect"].width:
                enemy["direction"] *= -1
            
            # Check collision with player
            if player_rect.colliderect(enemy["rect"]):
                # Check if player is jumping on enemy (from above)
                if player_velocity_y > 0 and player_y < enemy["rect"].y:
                    # Player jumped on enemy - get points and remove enemy
                    score += 100
                    # Remove this enemy from the list
                    enemies.remove(enemy)
                    # Give player a small bounce
                    player_velocity_y = -8
                    break  # Exit the loop since we modified the list
                else:
                    # Player hit enemy from side or below - lose life
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    else:
                        reset_player()
        
        # Check if player fell off the screen
        if player_y > WINDOW_HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                reset_player()
        
        # Check win condition - all enemies defeated
        if len(enemies) == 0 and not game_won:
            game_won = True
    
    # Clear the screen by filling it with white color
    screen.fill(WHITE)
    
    # Draw ground
    ground_rect = pygame.Rect(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10)
    pygame.draw.rect(screen, BROWN, ground_rect)
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, BLUE, enemy["rect"])
    
    # Draw the player (red square) at the current position
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, RED, player_rect)
    
    # Draw UI
    draw_text(f"Score: {score}", BLACK, 10, 10)
    draw_text(f"Lives: {lives}", BLACK, 10, 50)
    
    # Debug info - show if player can jump
    if player_on_ground and not game_over and not game_won:
        draw_text("CAN JUMP - Press SPACEBAR", GREEN, 10, 90)
    elif not game_over and not game_won:
        draw_text("IN AIR - Cannot jump", RED, 10, 90)
    
    if game_over:
        draw_text("GAME OVER! Press R to restart", BLACK, WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            game_over = False
            game_won = False
            lives = 3
            score = 0
            reset_player()
            # Reset enemies
            enemies = [
                {"rect": pygame.Rect(200, WINDOW_HEIGHT - 50, 30, 30), "direction": 1, "speed": 1},
                {"rect": pygame.Rect(500, 320, 30, 30), "direction": 1, "speed": 0.8},
                {"rect": pygame.Rect(700, 220, 30, 30), "direction": -1, "speed": 1},
                {"rect": pygame.Rect(150, 420, 30, 30), "direction": -1, "speed": 1.2},
                {"rect": pygame.Rect(600, 320, 30, 30), "direction": 1, "speed": 0.9},
            ]
    
    if game_won:
        draw_text("YOU WIN! All enemies defeated!", GREEN, WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2)
        draw_text(f"Final Score: {score}", BLACK, WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 40)
        draw_text("Press R to play again", BLACK, WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 + 80)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            game_over = False
            game_won = False
            lives = 3
            score = 0
            reset_player()
            # Reset enemies
            enemies = [
                {"rect": pygame.Rect(200, WINDOW_HEIGHT - 50, 30, 30), "direction": 1, "speed": 1},
                {"rect": pygame.Rect(500, 320, 30, 30), "direction": 1, "speed": 0.8},
                {"rect": pygame.Rect(700, 220, 30, 30), "direction": -1, "speed": 1},
                {"rect": pygame.Rect(150, 420, 30, 30), "direction": -1, "speed": 1.2},
                {"rect": pygame.Rect(600, 320, 30, 30), "direction": 1, "speed": 0.9},
            ]
    
    # Update the display - this shows everything we've drawn on the screen
    pygame.display.flip()
    
    # Control the frame rate - this ensures the game runs at 60 FPS
    clock.tick(FPS)

# Clean up pygame when the game ends
pygame.quit()
sys.exit() 