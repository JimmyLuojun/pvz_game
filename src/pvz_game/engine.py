# Placeholder for game loop and core engine logic. 
# this is for reusable code for other games.
#src/pvz_game/engine.py
import os
import pygame
from pvz_game.levels import LevelManager
from pvz_game.ui import UI
from pvz_game.entities import Plant, Zombie
from pvz_game.ai import update_zombie_ai
from dotenv import load_dotenv

# Load environment variables (if any)
load_dotenv()

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
        self.game_over = False
        self.victory = False

        # For resource exhaustion (example):
        self.ui.sun = 100  # Starting sun resource

        # For time-based or score-based end:
        self.survival_time = 60  # Survive 60 seconds to win, for example
        self.timer = 0

        # For wave-based or house HP:
        self.house_health = 3  # If a zombie crosses, reduce this to 0 -> game over

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
                if self.ui.sun >= 25:  # Example cost
                    pos = pygame.mouse.get_pos()
                    plant = Plant(pos)
                    self.entities.append(plant)
                    self.ui.sun -= 25
            # Pressing SPACE spawns a Zombie (for testing).
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    z = Zombie((SCREEN_WIDTH, SCREEN_HEIGHT // 2))
                    self.entities.append(z)

    def update(self, dt):
        if self.game_over or self.victory:
            return  # Freeze game state if we've already ended

        # Update all entities and remove ones that are marked as removed
        new_entities = []
        for e in self.entities:
            created = e.update(dt)
            if created:
                new_entities.extend(created)
        self.entities.extend(new_entities)

        # Handle plant refunds before removing them
        for e in self.entities:
            if isinstance(e, Plant) and e.removed and not e.refunded:
                self.ui.sun += 25  # Refund the sun cost
                e.refunded = True

        self.entities = [e for e in self.entities if not e.removed]

        # Time-based victory: track how long the player survives
        self.timer += dt
        if self.timer >= self.survival_time:
            self.victory = True

        # Let the LevelManager spawn zombies (wave-based logic)
        self.level_manager.update(dt, self.entities)

        # Update AI (zombie collisions, etc.)
        for e in self.entities:
            if isinstance(e, Zombie):
                update_zombie_ai(e, self.entities, dt)

        # Check collisions, remove destroyed zombies and update score
        removed_zombies = [z for z in self.entities if isinstance(z, Zombie) and z.removed]
        for z in removed_zombies:
            self.ui.score += 1  # Score-based approach
        self.entities = [e for e in self.entities if not e.removed]

        # 1. House HP system / Classic PvZ loss condition:
        #    If a zombie's x < 0, reduce house health
        for e in self.entities:
            if isinstance(e, Zombie) and e.position.x < 0:
                self.house_health -= 1
                e.removed = True  # remove the zombie
                if self.house_health <= 0:
                    self.game_over = True  # Player loses
        self.entities = [e for e in self.entities if not e.removed]

        # 2. Check if all waves are cleared (and no zombies remain)
        if self.level_manager.all_waves_cleared:
            if not any(isinstance(e, Zombie) for e in self.entities):
                self.victory = True

        # 3. Resource exhaustion (optional)
        if self.ui.sun < 25:
            # You might enforce a rule here if desired
            pass

        # 4. Score-based goal: if the player reaches a certain score, they win
        if self.ui.score >= 100:
            self.victory = True

    def draw(self):
        self.screen.fill((100, 200, 100))  # Green background.
        for entity in self.entities:
            entity.draw(self.screen)
        self.ui.draw(house_health=self.house_health, survival_time=self.survival_time, timer=self.timer)

        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()

        pygame.display.flip()

    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over!", True, (255, 0, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)

    def draw_victory(self):
        font = pygame.font.Font(None, 72)
        text = font.render("Victory!", True, (255, 255, 0))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)
