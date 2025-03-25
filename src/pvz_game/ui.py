# Placeholder for UI elements (menus, HUD, etc.). 
#src/pvz_game/ui.py
import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.score = 0  # Update this value during gameplay

    def draw(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
