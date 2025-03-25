# Placeholder for level data and management. 
#src/pvz_game/levels.py
import random
import os
from pvz_game.entities import Zombie

# Optionally, use environment variables for screen dimensions:
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))

class LevelManager:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_interval = 5  # Spawn a zombie every 5 seconds

    def update(self, dt, entities):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            # Spawn a zombie at the right edge, with a random vertical position.
            # Here, we add a margin of 50 pixels at the top and bottom for aesthetics.
            y = random.randint(50, SCREEN_HEIGHT - 50)
            zombie = Zombie((SCREEN_WIDTH, y))
            entities.append(zombie)
            self.spawn_timer = 0

