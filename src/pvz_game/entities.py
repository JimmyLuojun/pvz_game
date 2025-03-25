# Placeholder for classes related to plants, zombies, and projectiles. 
#src/pvz_game/entities.py
import pygame

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
    def __init__(self, pos):
        super().__init__(pos)
        self.color = (0, 255, 0)  # Green
        self.radius = 20
        self.shoot_timer = 0
        self.shoot_interval = 2  # Seconds between shots
        self.projectiles_shot = 0  # Count of projectiles fired
        self.refunded = False  # Track if sun has been refunded

    def update(self, dt):
        self.shoot_timer += dt
        new_entities = []
        if self.shoot_timer >= self.shoot_interval and self.projectiles_shot < 2:
            self.shoot_timer = 0
            new_entities.append(Projectile((self.position.x + self.radius, self.position.y)))
            self.projectiles_shot += 1
        if self.projectiles_shot >= 2:
            self.removed = True
            # Refund sun points since the plant is now finished
            # (Make sure to check if this refund should only happen once)
            # For example, you might add:
            # self.refunded = True  # and in engine, if plant.removed and not plant.refunded, refund sun
        return new_entities

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

class Zombie(GameEntity):
    def __init__(self, pos):
        super().__init__(pos)
        self.color = (255, 0, 0)  # Red
        self.radius = 20
        self.speed = 50
        self.hp = 1  # A single hit defeats the zombie

    def update(self, dt):
        self.position.x -= self.speed * dt
        if self.position.x < -self.radius:
            self.removed = True
        return []

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.removed = True
