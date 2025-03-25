# Placeholder for classes related to plants, zombies, and projectiles. 
#src/pvz_game/entities.py
import pygame
import os

class GameEntity:
    def __init__(self, pos):
        self.position = pygame.math.Vector2(pos)
        self.removed = False

    def update(self, dt):
        """Update the entity. Return a list of new entities (if any)."""
        return []

    def draw(self, surface):
        pass

class Projectile(GameEntity):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = (255, 255, 0)  # Yellow
        self.radius = 5
        self.speed = 300

    def update(self, dt):
        self.position.x += self.speed * dt
        if self.position.x > 800:
            self.removed = True
        return []

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

class Plant(GameEntity):
    # Class variable to store animation frames for all Plant objects.
    plant_images = []
    frame_interval = 0.2  # seconds per frame

    def __init__(self, pos):
        super().__init__(pos)
        # For refund logic, initialize refunded flag.
        self.refunded = False
        # Load images once if not already loaded.
        if not Plant.plant_images:
            plant_dir = os.path.join("assets", "images", "plant")
            # List of frame filenames (adjust if needed).
            frame_files = [
                "frame_002.png", "frame_003.png", "frame_004.png",
                "frame_005.png", "frame_006.png", "frame_007.png"
            ]
            for filename in frame_files:
                image_path = os.path.join(plant_dir, filename)
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (40, 40))
                Plant.plant_images.append(image)
        self.images = Plant.plant_images
        self.current_frame = 0
        self.animation_timer = 0
        self.rect = self.images[self.current_frame].get_rect(center=(int(self.position.x), int(self.position.y)))
        self.shoot_timer = 0
        self.shoot_interval = 2  # seconds between shots
        self.projectiles_shot = 0  # Count of projectiles fired

    def update(self, dt):
        # Update animation frame
        self.animation_timer += dt
        if self.animation_timer >= Plant.frame_interval:
            self.animation_timer -= Plant.frame_interval
            self.current_frame = (self.current_frame + 1) % len(self.images)

        # Shooting logic: fire a projectile every shoot_interval if fewer than 2 have been shot.
        self.shoot_timer += dt
        new_entities = []
        if self.shoot_timer >= self.shoot_interval and self.projectiles_shot < 2:
            self.shoot_timer = 0
            new_entities.append(Projectile((self.position.x + self.rect.width, self.position.y)))
            self.projectiles_shot += 1

        # When 2 projectiles have been fired, mark the plant for removal.
        if self.projectiles_shot >= 2:
            self.removed = True

        return new_entities

    def draw(self, surface):
        # Update the rect position and draw the current frame.
        self.rect.center = (int(self.position.x), int(self.position.y))
        surface.blit(self.images[self.current_frame], self.rect)

class Zombie(GameEntity):
    # Class variable to store animation frames for all Zombie objects.
    zombie_images = []
    frame_interval = 0.2  # seconds per frame

    def __init__(self, pos):
        super().__init__(pos)
        if not Zombie.zombie_images:
            zombie_dir = os.path.join("assets", "images", "zombie")
            # List of zombie frame filenames.
            frame_files = [
                "frame_12.png", "frame_13.png", "frame_15.png", "frame_16.png",
                "frame_17.png", "frame_18.png", "frame_20.png", "frame_21.png"
            ]
            for filename in frame_files:
                image_path = os.path.join(zombie_dir, filename)
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (40, 40))
                Zombie.zombie_images.append(image)
        self.images = Zombie.zombie_images
        self.current_frame = 0
        self.animation_timer = 0
        self.rect = self.images[self.current_frame].get_rect(center=(int(self.position.x), int(self.position.y)))
        self.speed = 50
        self.hp = 1  # One hit defeat
        self.radius = self.rect.width // 2  # For collision detection

    def update(self, dt):
        # Update animation frame
        self.animation_timer += dt
        if self.animation_timer >= Zombie.frame_interval:
            self.animation_timer -= Zombie.frame_interval
            self.current_frame = (self.current_frame + 1) % len(self.images)
        # Movement logic: move left
        self.position.x -= self.speed * dt
        self.rect.centerx = int(self.position.x)
        if self.position.x < -self.rect.width:
            self.removed = True
        return []

    def draw(self, surface):
        surface.blit(self.images[self.current_frame], self.rect)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.removed = True
