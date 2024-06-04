import pygame
import random

# Define game variables
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 650
GRAVITY = 0.25
FLAP_HEIGHT = -8
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_IMAGE_PATH = "/Users/amberhaverly/Pictures/flappycat.png"
BACKGROUND_IMAGE_PATH = "/Users/amberhaverly/Pictures/desert.jpg"
APPLE_IMAGE_PATH = "/Users/amberhaverly/Pictures/bubbletea.png"
SECOND_CHARACTER_IMAGE_PATH = "/Users/amberhaverly/Pictures/duck.png"  # Path to second character image
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (255, 140, 0)  # Dark Orange
APPLE_SPEED = 5  # Adjust as needed
BACKGROUND_SCROLL_SPEED = 1
high_score = 180

def display_dialogue(dialogue_text):
    # Code to display the dialogue text on the screen
    pass  # Placeholder, you need to implement this function according to your game's requirements

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Cat")

# Load images
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH).convert_alpha()
background_rect = background_image.get_rect()
bird_image = pygame.image.load(BIRD_IMAGE_PATH).convert_alpha()
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
apple_image = pygame.image.load(APPLE_IMAGE_PATH).convert_alpha()

# Load music
pygame.mixer.music.load("/Users/amberhaverly/Music/rivermusic.mp3")
pygame.mixer.music.play(-1)  # Play music on loop

# Define Bird class
bird_image_original = pygame.image.load(BIRD_IMAGE_PATH).convert_alpha()
bird_image = pygame.transform.scale(bird_image_original, (100, 120))
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.alive = True
        # Create a collision rectangle for the bird
        self.rect = pygame.Rect(x, y, BIRD_WIDTH, BIRD_HEIGHT)

    def flap(self):
        self.velocity = FLAP_HEIGHT

    def move_right(self):
        self.x += 7  # Adjust speed as needed

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        # Update the position of the collision rectangle
        self.rect.y = self.y

        if self.y < 0 or self.y > SCREEN_HEIGHT - self.height:
            self.alive = False

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))

    def bounce(self, platform_rect):
        self.y = platform_rect.top - self.height
        self.velocity = FLAP_HEIGHT  # Adjust bounce strength as needed
        # Update the position of the collision rectangle
        self.rect.y = self.y

# Define Platform class
class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, PLATFORM_COLOR, self.rect)

# Define Hazard class
class Hazard:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

# Load the image for the second character and scale it if needed
second_character_image_original = pygame.image.load(SECOND_CHARACTER_IMAGE_PATH).convert_alpha()
second_character_image = pygame.transform.scale(second_character_image_original, (120, 140))

# Set the position of the second character on the third platform
# Define the positions of the platforms
platform_positions = [
    (100, SCREEN_HEIGHT - 150),
    (300, SCREEN_HEIGHT - 300),
    (500, SCREEN_HEIGHT - 450),
    (700, SCREEN_HEIGHT - 150),
    (900, SCREEN_HEIGHT - 300),
    (1100, SCREEN_HEIGHT - 450),
]

# Create the platforms
platforms = [Platform(x, y) for x, y in platform_positions]

second_character_position = (platforms[2].rect.x, platforms[2].rect.y - second_character_image.get_height())

# Set up game loop
clock = pygame.time.Clock()
running = True
score = 0
background_x = 0

# Create bird object
bird = Bird(50, SCREEN_HEIGHT // 2)

# Create hazards
hazards = [
    Hazard(150, SCREEN_HEIGHT - 50, 60, 20),
    Hazard(600, SCREEN_HEIGHT - 200, 80, 30),
    Hazard(1000, SCREEN_HEIGHT - 350, 80, 25),
]

# Game loop
# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()
            elif event.key == pygame.K_RIGHT:
                bird.move_right()

    # Update bird
    if bird.alive:
        bird.update()

    # Collision with platforms
    for platform in platforms:
        if bird.x < platform.rect.right and bird.x + bird.width > platform.rect.left \
                and bird.y + bird.height > platform.rect.top and bird.y < platform.rect.bottom:
            bird.bounce(platform.rect)
            if bird.y < platform.rect.bottom:
                score += 10
                # Check if Flappy lands on the third platform
                if platform == platforms[2]:
                    display_dialogue("Hello, I'm an ally")

    # Collision with hazards
    for hazard in hazards:
        if bird.rect.colliderect(hazard.rect):
            bird.alive = False

    # Move background
    background_x -= BACKGROUND_SCROLL_SPEED
    if background_x <= -background_rect.width:
        background_x = 0

    # Draw background
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + background_rect.width, 0))

    # Draw bird
    bird.draw(screen)

    # Draw platforms
    for platform in platforms:
        platform.draw(screen)

    # Draw hazards
    for hazard in hazards:
        hazard.draw(screen)

    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Check game over
    if not bird.alive:
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        running = False  # Stop the game loop

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
