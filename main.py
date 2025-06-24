import pygame
from env.grid import Grid
from env.ant import Ant

# initializing imported module
pygame.init()

# displaying a window of height
# 500 and width 400
screen = pygame.display.set_mode((500, 500))

# Setting name for window
pygame.display.set_caption('GeeksforGeeks')

# creating a bool value which checks 
# if game is running and starts clock
running = True
clock = pygame.time.Clock()
fps = 10

# setsup grid and ants
grid = Grid(rows=50, cols=50, cell_size=10)
ants = [Ant(2, 3), Ant(5, 7), Ant(0, 0)]


# Game loop
# keep game running till running is true
while running:

    # Clear screen
    screen.fill((0, 0, 0))

    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
      


        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False
    
    # Draw and update Grid and ants to buffer
    grid.draw(screen)
    for ant in ants:
        ant.move(grid.rows, grid.cols)
        ant.draw(screen, grid.cell_size)

    # Update entire screen
    pygame.display.flip()
    clock.tick(fps)