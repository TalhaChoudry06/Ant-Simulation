import pygame

class EntityLayer:
    def __init__(self, rows, cols):
        self.positions = {}  # keys: (row, col), values: list of entities

    def add(self, row, col, entity):
        self.positions.setdefault((row, col), []).append(entity)

    def remove(self, row, col, entity):
        if (row, col) in self.positions:
            self.positions[(row, col)].remove(entity)
            if not self.positions[(row, col)]:
                del self.positions[(row, col)]

    def move(self, old_pos, new_pos, entity):
        self.remove(*old_pos, entity)
        self.add(*new_pos, entity)

    def get(self, row, col):
        return self.positions.get((row, col), [])
