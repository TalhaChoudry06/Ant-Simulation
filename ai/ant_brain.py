import torch
import torch.nn as nn

class AntBrain(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, x):
        return self.model(x)


# 8 neurons, for 8 movement actions.
# Your neural network will output 8 numbers — 
# each number represents the "score" or "confidence" 
# the network has that the ant should move in that direction.
# NN(input vector)→output vector of length 8
# You take the argmax (the index of the largest output value) 
# to pick the best move.

# The activation for this layer is usually softmax 
# to convert raw scores (logits) into probabilities.

# Up (north)

# Down (south)

# Left (west)

# Right (east)

# Up-left (northwest)

# Up-right (northeast)

# Down-left (southwest)

# Down-right (southeast)

# Why 8 outputs?
