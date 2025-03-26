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
        # Compute time left if needed
        if survival_time:
            time_left = max(0, int(survival_time - timer))
        else:
            time_left = 0

        # Combine everything into one line
        info_text = (
            f"Score: {self.score} | "
            f"Sun: {self.sun} | "
            f"House HP: {house_health if house_health is not None else 'N/A'} | "
            f"Time Left: {time_left}s"
        )
        
        # Render and draw at the top
        text_surface = self.font.render(info_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

