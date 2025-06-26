import random

class AntState:
    def update(self, ant, grid):
        raise NotImplementedError

class SearchingState(AntState):
    def update(self, ant, grid):
        for r, c in ant.vision(grid):  # Use Ant's vision method
            if (r, c) in grid.food_cells:
                print("food found")
                # Food found
                ant.carrying_food = True
                grid.remove_food(r, c)
                ant.pheromone_map.deposit(ant.row, ant.col, 0.5)
                ant.set_state(ReturningState())
                return  # Exit early once food is found

        # If no food found, move randomly
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = random.choice(directions)
        ant.move(dr, dc, grid)

class ReturningState(AntState):
    def update(self, ant, grid):
        # 1. Drop pheromone at current position
        ant.pheromone_map.deposit(ant.row, ant.col, 0.3)

        # debug
        if ant.nest is None:
            assert False, "Ant has no nest assigned!"

        # 2. Move toward the nest
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
