# Placeholder for game loop and core engine logic. 
# this is for reusable code for other games.
#src/pvz_game/engine.py
import os
import pygame
from pvz_game.levels import LevelManager
from pvz_game.ui import UI
from pvz_game.entities import Plant, Zombie
from pvz_game.ai import update_zombie_ai

# If you're using environment variables, import them here:
from dotenv import load_dotenv
load_dotenv()

# Example environment variable usage (optional):
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))
FPS = int(os.getenv("FPS", 60))

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Plants vs. Zombies")
        self.clock = pygame.time.Clock()
        self.level_manager = LevelManager()
        self.ui = UI(self.screen)
        self.entities = []  # List of all game entities (plants, zombies, projectiles)
        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds since last frame
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Left mouse click plants a new Plant at mouse position.
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                plant = Plant(pos)
                self.entities.append(plant)
            # Pressing SPACE spawns a Zombie (for testing).
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    zombie = Zombie((SCREEN_WIDTH, SCREEN_HEIGHT // 2))
                    self.entities.append(zombie)

    def update(self, dt):
        # Let the LevelManager spawn zombies if needed.
        self.level_manager.update(dt, self.entities)

        new_entities = []
        # Update all entities; if an entity creates new ones (like a plant shooting), add them.
        for entity in self.entities:
            created = entity.update(dt)
            if created:
                new_entities.extend(created)
        self.entities.extend(new_entities)

        # Update AI for zombies.
        for entity in self.entities:
            if isinstance(entity, Zombie):
                update_zombie_ai(entity, self.entities, dt)

        # Check for removed zombies to update score
        removed_zombies = [z for z in self.entities if isinstance(z, Zombie) and z.removed]
        for z in removed_zombies:
            self.ui.score += 1

        # Remove all entities marked for removal (zombies, projectiles, etc.)
        self.entities = [e for e in self.entities if not e.removed]

    def draw(self):
        self.screen.fill((100, 200, 100))  # Green background.
        # Draw each entity.
        for entity in self.entities:
            entity.draw(self.screen)
        # Draw UI elements.
        self.ui.draw()
        pygame.display.flip()
