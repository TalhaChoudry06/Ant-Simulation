import pygame
from env.Grid import Grid
from env.Ant import Ant
from env.PheromoneMap import PheromoneMap

# initializing imported module
pygame.init()

# displaying a window of height
# 500 and width 400
screen = pygame.display.set_mode((1000, 1000))
brown = (139, 69, 19)

# Setting name for window
pygame.display.set_caption('GeeksforGeeks')

# creating a bool value which checks 
# if game is running and starts clock
running = True
clock = pygame.time.Clock()
fps = 10

# set up pheromone map
pheromone_map = PheromoneMap(rows=100, cols=100, cell_size=10)

# set up grid
grid = Grid(rows=100, cols=100, cell_size=10)

# place nest
nest = grid.place_nest(50,50)

# place food 
# grid.place_food(40, 50, pheromone_map)
# grid.place_food(40, 6, pheromone_map)
grid.place_food(20, 8, pheromone_map)

# create ants (without specifying position yet)
ants_to_deploy = [Ant(pheromone_map, 0, 0, nest) for _ in range(3)]

# add ants to nest
for ant in ants_to_deploy:
    nest.add_ant(ant)

for ant in ants_to_deploy:
    grid.entity_layer.add(ant, nest.row, nest.col)

print("All positions:", grid.entity_layer.positions)
print("Total positions:", len(grid.entity_layer.positions))


# deploy ants (sets their position to nest and returns the list)
ants = nest.deploy_ant()

# Game loop
# keep game running till running is true
while running:

    # Clear screen
    # when removed it kind looks like a heat map and shows where the ants have been 
    screen.fill((brown))

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
        ant.update(grid)
        ant.vision(grid, screen, grid.cell_size, grid.offset_x, grid.offset_y, draw=True)
        ant.draw(screen, grid.cell_size)

    # update and decay pheromone map
    for food in grid.food_cells.values():
        food.emit_scent(pheromone_map)
    pheromone_map.decay(0.03)

    pheromone_map.draw(screen)
    
    # Update entire screen
    pygame.display.flip()
    clock.tick(fps)