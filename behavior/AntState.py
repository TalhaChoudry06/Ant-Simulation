import random
from env.Food import Food
import torch
import torch.nn.functional as F
from ai.AntPolicyNet import AntPolicyNet
import random
from constants import DIRECTIONS

class AntState:
    def update(self, ant, grid):
        raise NotImplementedError

# class SearchingState(AntState):
    # def update(self, ant, grid):
    #     ant.pheromone_map.deposit(ant.row, ant.col, 0.5, pheromone_type="search")
    #     observation_vector = ant.perception(grid)
    #     obs_tensor = torch.tensor(observation_vector, dtype=torch.float32).unsqueeze(0)
    #     action = ()

    #     for r, c in ant.vision(grid):
    #         if (r, c) in grid.food_cells and abs(ant.row - r) <= 1 and abs(ant.col - c) <= 1:
    #             print("food found")
    #             # Food found
    #             # need to fix so that just because food is in vision dosent mean it gets picked up automatically, add pathfinding to food so its in a 1 block radius around then pick up
    #             if grid.food_cells[(r, c)].take():
    #                 grid.remove_food(r, c)
    #                 print("food gone at", r, c)
    #             ant.carrying_food = True
    #             print("ant is carrying food:", {ant.carrying_food})
    #             ant.set_state(ReturningState())

    #             return  # Exit early once food is found

    #     # If no food found, move randomly
    #     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    #     dr, dc = random.choice(directions)
    #     ant.move(dr, dc, grid)

class SearchingState:
    def update(self, ant, grid):
        # 1. Get observation vector
        obs = ant.perception(grid)

        # 2. Convert to tensor and add batch dimension
        obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)

        # 3. Feed through policy network to get logits (raw scores)
        logits = ant.policy_net(obs_tensor) # shape: [1, 8]

        # 4. Get valid directions as boolean mask (shape [8])
        # You need to implement this in Ant class
        # Example: [True, False, True, ..., True]
        valid_mask = torch.tensor(ant.get_valid_directions(grid), dtype=torch.bool)

        # 5. Mask invalid logits to -inf (so softmax will assign them 0 probability)
        masked_logits = logits[0].masked_fill(~valid_mask, float('-inf'))  # shape: [8]

        # 6. Apply softmax to get a probability distribution
        probs = F.softmax(masked_logits, dim=0)  # shape: [8]

        # 7. Sample one action index using the probabilities
        action_index = torch.multinomial(probs, num_samples=1).item()

        # 8. Map action index to movement and move and deposit pheormones.
        dr, dc = DIRECTIONS[action_index]
        ant.pheromone_map.deposit(ant.row, ant.col, 0.5, pheromone_type="search")
        ant.move(dr, dc, grid)

class ReturningState(AntState):
    def update(self, ant, grid):
        ant.pheromone_map.deposit(ant.row, ant.col, 0.8, pheromone_type="return")
        # observation_vector = ant.perception(grid)
        # obs_tensor = torch.tensor(observation_vector, dtype=torch.float32).unsqueeze(0)
        # action = ()

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
