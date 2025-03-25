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
    # Load the plant image only once for all Plant objects.
    plant_image = None

    def __init__(self, pos):
        super().__init__(pos)
        # For refund logic, initialize refunded flag.
        self.refunded = False
        if Plant.plant_image is None:
            image_path = os.path.join("assets", "images", "plant.png")
            Plant.plant_image = pygame.image.load(image_path).convert_alpha()
            Plant.plant_image = pygame.transform.scale(Plant.plant_image, (40, 40))
        self.image = Plant.plant_image
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
        self.shoot_timer = 0
        self.shoot_interval = 2  # Seconds between shots
        self.projectiles_shot = 0  # Count how many projectiles have been fired

    def update(self, dt):
        self.shoot_timer += dt
        new_entities = []
        if self.shoot_timer >= self.shoot_interval and self.projectiles_shot < 2:
            self.shoot_timer = 0
            new_entities.append(Projectile((self.position.x + self.rect.width, self.position.y)))
            self.projectiles_shot += 1
        if self.projectiles_shot >= 2:
            self.removed = True
        return new_entities

    def draw(self, surface):
        self.rect.center = (int(self.position.x), int(self.position.y))
        surface.blit(self.image, self.rect)

class Zombie(GameEntity):
    # Load the zombie image only once for all Zombie objects.
    zombie_image = None

    def __init__(self, pos):
        super().__init__(pos)
        if Zombie.zombie_image is None:
            image_path = os.path.join("assets", "images", "zombie.png")
            Zombie.zombie_image = pygame.image.load(image_path).convert_alpha()
            Zombie.zombie_image = pygame.transform.scale(Zombie.zombie_image, (40, 40))
        self.image = Zombie.zombie_image
        self.rect = self.image.get_rect(center=(int(self.position.x), int(self.position.y)))
        self.speed = 50
        self.hp = 1  # One hit defeat
        # Set radius for collision detection based on image size.
        self.radius = self.rect.width // 2

    def update(self, dt):
        self.position.x -= self.speed * dt
        self.rect.centerx = int(self.position.x)
        if self.position.x < -self.rect.width:
            self.removed = True
        return []

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.removed = True
