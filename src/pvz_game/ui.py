# Placeholder for UI elements (menus, HUD, etc.). 
#src/pvz_game/ui.py
import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.score = 0  # Score from defeated zombies
        self.sun = 100  # Starting resource (sun)

    def draw(self, house_health=None, survival_time=None, timer=0):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Draw sun/resource
        sun_text = self.font.render(f"Sun: {self.sun}", True, (255, 255, 0))
        self.screen.blit(sun_text, (10, 50))

        # Optionally draw house health if provided
        if house_health is not None:
            hp_text = self.font.render(f"House HP: {house_health}", True, (255, 100, 100))
            self.screen.blit(hp_text, (10, 90))

        # Optionally draw survival time if provided
        if survival_time is not None:
            time_left = max(0, int(survival_time - timer))
            time_text = self.font.render(f"Time Left: {time_left}s", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 130))

