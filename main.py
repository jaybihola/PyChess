import pygame
import sys
from game import Game
from colors import Colors

# Initialize Pygame
pygame.init()

# Set up the display
square_size = 80
board_size = 8
border_size = 40
window_size = (board_size * square_size + 2 * border_size,
               board_size * square_size + 2 * border_size)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("PyChess")

game = Game()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = (pos[0] - border_size) // square_size, (pos[1] - border_size) // square_size
            if 0 <= x < board_size and 0 <= y < board_size:
                game.handle_clicks((x, y))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.clear_clicks()

    # Clear the screen to white
    screen.fill(Colors.WHITE)

    game.play()

    game.draw_all(screen)

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()