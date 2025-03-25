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
        self.current_wave = 1
        self.max_waves = 5
        self.spawn_timer = 0
        self.spawn_interval = 3  # seconds between spawn events
        self.zombies_per_wave = 5
        self.zombies_spawned_this_wave = 0
        self.all_waves_cleared = False  # This attribute is now defined

    def update(self, dt, entities):
        if self.all_waves_cleared:
            return

        self.spawn_timer += dt

        if self.current_wave <= self.max_waves:
            if self.zombies_spawned_this_wave < self.zombies_per_wave:
                if self.spawn_timer >= self.spawn_interval:
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    zombie = Zombie((SCREEN_WIDTH, y))
                    entities.append(zombie)
                    self.zombies_spawned_this_wave += 1
                    self.spawn_timer = 0
            else:
                # Wave completed; move to the next wave.
                self.current_wave += 1
                self.zombies_spawned_this_wave = 0

        # Once all waves have been spawned, mark as cleared.
        if self.current_wave > self.max_waves:
            self.all_waves_cleared = True

