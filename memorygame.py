import pygame
import random
import sys
import time


pygame.init()


WINDOW_SIZE = (800, 600)
CARD_SIZE = (100, 100)
GRID_SIZE = (4, 4)
CARD_COUNT = GRID_SIZE[0] * GRID_SIZE[1]
FPS = 30
BACKGROUND_COLOR = (245, 245, 220)  # Light beige background
CARD_COLOR = (156, 124, 56)         # Brownish color for cards
TEXT_COLOR = (37, 53, 41)           # Dark green text color

# Load card images
def load_images():
    images = []
    try:
        for i in range(CARD_COUNT // 2):
            image = pygame.image.load(f"images/card_{i}.png")
            image = pygame.transform.scale(image, CARD_SIZE)
            images.append(image)
            images.append(image)  # Add the pair of the image
        random.shuffle(images)  # Shuffle images
        return images
    except Exception as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        sys.exit()

# Create the display surface
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Memory Game")

# Initialize font
font = pygame.font.Font(None, 36)

# Function to draw the grid of cards and stats
def draw_grid(cards, flipped, matches, moves, elapsed_time):
    window.fill(BACKGROUND_COLOR)
    
    for i in range(GRID_SIZE[0]):
        for j in range(GRID_SIZE[1]):
            x = (WINDOW_SIZE[0] - GRID_SIZE[0] * CARD_SIZE[0]) // 2 + i * CARD_SIZE[0]
            y = (WINDOW_SIZE[1] - GRID_SIZE[1] * CARD_SIZE[1]) // 2 + j * CARD_SIZE[1]
            rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
            
            if (i, j) in matches:
                window.blit(cards[i][j], rect.topleft)
            elif (i, j) in flipped:
                window.blit(cards[i][j], rect.topleft)
            else:
                pygame.draw.rect(window, CARD_COLOR, rect)
                pygame.draw.rect(window, TEXT_COLOR, rect, 3)
    
    # Draw stats
    moves_text = font.render(f"Moves: {moves}", True, TEXT_COLOR)
    time_text = font.render(f"Time: {int(elapsed_time)}s", True, TEXT_COLOR)
    window.blit(moves_text, (10, WINDOW_SIZE[1] - 60))
    window.blit(time_text, (10, WINDOW_SIZE[1] - 30))
    
    pygame.display.flip()

# Function to generate a list of card images in a 2D grid
def generate_cards(images):
    return [[images.pop() for _ in range(GRID_SIZE[1])] for _ in range(GRID_SIZE[0])]

# Main game loop
def main():
    clock = pygame.time.Clock()
    images = load_images()
    cards = generate_cards(images)
    flipped = set()
    matches = set()
    first_card = None
    second_card = None
    waiting = False
    moves = 0
    start_time = time.time()
    
    while True:
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not waiting:
                x, y = event.pos
                grid_x = (x - (WINDOW_SIZE[0] - GRID_SIZE[0] * CARD_SIZE[0]) // 2) // CARD_SIZE[0]
                grid_y = (y - (WINDOW_SIZE[1] - GRID_SIZE[1] * CARD_SIZE[1]) // 2) // CARD_SIZE[1]
                
                if 0 <= grid_x < GRID_SIZE[0] and 0 <= grid_y < GRID_SIZE[1]:
                    if (grid_x, grid_y) not in flipped and (grid_x, grid_y) not in matches:
                        if not first_card:
                            first_card = (grid_x, grid_y)
                            flipped.add(first_card)
                        elif not second_card:
                            second_card = (grid_x, grid_y)
                            flipped.add(second_card)
                            moves += 1
                            waiting = True
        
        if first_card and second_card:
            if cards[first_card[0]][first_card[1]] == cards[second_card[0]][second_card[1]]:
                matches.add(first_card)
                matches.add(second_card)
            else:
                pygame.time.wait(1000)  # Wait for 1 second before flipping back
                flipped.discard(first_card)
                flipped.discard(second_card)
                
            first_card = None
            second_card = None
            waiting = False
        
        if len(matches) == CARD_COUNT:
            window.fill(BACKGROUND_COLOR)
            end_text = font.render(f"Finished in {int(elapsed_time)}s with {moves} moves", True, TEXT_COLOR)
            window.blit(end_text, (10, WINDOW_SIZE[1] // 2 - 20))
            pygame.display.flip()
            pygame.time.wait(3000)  # Show the final message for 3 seconds
            pygame.quit()
            sys.exit()
        
        draw_grid(cards, flipped, matches, moves, elapsed_time)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
