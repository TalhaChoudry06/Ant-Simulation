import random
from env.Food import Food

class AntState:
    def update(self, ant, grid):
        raise NotImplementedError

class SearchingState(AntState):
    def update(self, ant, grid):
        ant.pheromone_map.deposit(ant.row, ant.col, 0.5, pheromone_type="search")
        for r, c in ant.vision(grid):
            #test
            ant.perception(grid)

            if (r, c) in grid.food_cells:
                print("food found")
                # Food found
                # need to fix so that just because food is in vision dosent mean it gets picked up automatically, add pathfinding to food so its in a 1 block radius around then pick up
                if grid.food_cells[(r, c)].take():
                    grid.remove_food(r, c)
                    print("food gone at", r, c)
                ant.carrying_food = True
                ant.set_state(ReturningState())

                return  # Exit early once food is found

        # If no food found, move randomly
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = random.choice(directions)
        ant.move(dr, dc, grid)

class ReturningState(AntState):
    def update(self, ant, grid):
        # 1. Drop pheromone at current position
        ant.pheromone_map.deposit(ant.row, ant.col, 0.3, pheromone_type="return")

        # debug
        if ant.nest is None:
            assert False, "Ant has no nest assigned!"

        # 2. Move toward the nest
        # USE HELPER FUNCTIONS
        dr = dc = 0
        if ant.row < ant.nest.row:
            dr = 1
        elif ant.row > ant.nest.row:
            dr = -1

        if ant.col < ant.nest.col:
            dc = 1
        elif ant.col > ant.nest.col:
            dc = -1

        ant.move(dr, dc, grid)

        # 3. Check if ant is at nest
        if (ant.row, ant.col) == (ant.nest.row, ant.nest.col):
            ant.carrying_food = False
            ant.set_state(SearchingState())

