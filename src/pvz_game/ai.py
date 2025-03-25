# Placeholder for AI behavior logic for enemies. 
#src/pvz_game/ai.py
def update_zombie_ai(zombie, entities, dt):
    # Simple collision check: if a projectile is close to the zombie, it takes damage.
    for entity in entities:
        # Identify projectiles by their yellow color.
        if hasattr(entity, "color") and entity.color == (255, 255, 0):
            dx = zombie.position.x - entity.position.x
            dy = zombie.position.y - entity.position.y
            distance = (dx**2 + dy**2) ** 0.5
            if distance < zombie.radius + entity.radius:
                zombie.take_damage(1)
                entity.removed = True
