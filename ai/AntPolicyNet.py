import torch
import torch.nn as nn
import torch.nn.functional as F

class AntPolicyNet(nn.Module):
    def __init__(self, input_size, output_size=8):
        super(AntPolicyNet, self).__init__()
        # First layer: input_size -> 64 neurons
        self.fc1 = nn.Linear(input_size, 64)
        
        # Second layer: 64 -> 32 neurons
        self.fc2 = nn.Linear(64, 32)
        
        # Output layer: 32 -> 8 neurons (one for each direction)
        self.fc3 = nn.Linear(32, output_size)

    def forward(self, x):
        # Apply first layer + ReLU activation
        x = F.relu(self.fc1(x))
        
        # Apply second layer + ReLU activation
        x = F.relu(self.fc2(x))
        
        # Output layer (raw scores, no activation)
        x = self.fc3(x)
        return x




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
