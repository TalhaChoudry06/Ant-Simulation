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

            if (r, c) in grid.food_cells and abs(ant.row - r) <= 1 and abs(ant.col - c) <= 1:
                print("food found")
                # Food found
                # need to fix so that just because food is in vision dosent mean it gets picked up automatically, add pathfinding to food so its in a 1 block radius around then pick up
                if grid.food_cells[(r, c)].take():
                    grid.remove_food(r, c)
                    print("food gone at", r, c)
                ant.carrying_food = True
                print("ant is carrying food:", {ant.carrying_food})
                ant.set_state(ReturningState())

                return  # Exit early once food is found

        # If no food found, move randomly
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = random.choice(directions)
        ant.move(dr, dc, grid)

import random

class ReturningState(AntState):
    def update(self, ant, grid):
        ant.pheromone_map.deposit(ant.row, ant.col, 0.3, pheromone_type="return")

        if ant.nest is None:
            assert False, "Ant has no nest assigned!"

        # Calculate vector to nest
        d_row = ant.nest.row - ant.row
        d_col = ant.nest.col - ant.col

        # Normalize to -1, 0, or 1
        dr = (d_row > 0) - (d_row < 0)
        dc = (d_col > 0) - (d_col < 0)

        # Create possible moves, with some randomness
        moves = [(dr, dc)]

        if dr != 0: moves.append((dr, 0))
        if dc != 0: moves.append((0, dc))

        # Add slight randomness for realism
        moves.append((random.choice([-1, 0, 1]), random.choice([-1, 0, 1])))

        # Shuffle to make it more ant-like
        random.shuffle(moves)

        # Try each move and pick the first valid one
        for move_dr, move_dc in moves:
            new_row = ant.row + move_dr
            new_col = ant.col + move_dc
            if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:
                ant.move(move_dr, move_dc, grid)
                break

        # At nest?
        if (ant.row, ant.col) == (ant.nest.row, ant.nest.col):
            ant.carrying_food = False
            ant.set_state(SearchingState())
