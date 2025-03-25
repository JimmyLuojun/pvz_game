 # tests/test_game_logic.py
import pygame
import pytest
from pvz_game.entities import Zombie, Plant, Projectile

def test_zombie_take_damage():
    zombie = Zombie((400, 300))
    initial_hp = zombie.hp
    zombie.take_damage(1)
    assert zombie.hp == initial_hp - 1
    zombie.take_damage(100)
    assert zombie.removed is True

def test_plant_shoot():
    plant = Plant((100, 100))
    # Simulate enough time passing for the plant to shoot.
    new_entities = plant.update(2)
    assert len(new_entities) == 1
    projectile = new_entities[0]
    assert isinstance(projectile, Projectile)
