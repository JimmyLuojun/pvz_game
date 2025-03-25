# Placeholder for level data and management. 
#src/pvz_game/levels.py
from pvz_game.entities import Zombie

class LevelManager:
    def __init__(self):
        self.spawn_timer = 0
        self.spawn_interval = 5  # Spawn a zombie every 5 seconds

    def update(self, dt, entities):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            # Spawn a zombie at a random vertical position.
            zombie = Zombie((800, 100 + int(400 * (self.spawn_timer % 1))))
            entities.append(zombie)
            self.spawn_timer = 0
