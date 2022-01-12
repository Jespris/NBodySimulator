"""
Contains class celestialbody
"""

from Universe import Universe
from Vector import Vector2
import pygame as p


class NewCelestialBody:
    def __init__(self):
        self.pos = Vector2.zero()
        self.radius = 1
        self.gravity = 1
        self.initial_velocity = Vector2.zero()
        self.name = "Unnamed"
        self.color = p.Color("white")

    def update(self):
        if self.radius < 1:
            self.radius = 1
        if self.name == "":
            self.name = "Unnamed"


class CelestialBody:
    def __init__(self, pos, radius, gravity, initial_velocity, name, color):
        self.pos = pos
        self.radius = radius
        self.surface_gravity = gravity
        self.velocity = initial_velocity
        self.name = name
        self.color = color
        self.mass = self.surface_gravity * radius * radius / Universe.Big_G

    def UpdateVelocity(self, acceleration, time_step):
        self.velocity += acceleration * time_step

    def UpdatePosition(self, time_step):
        self.pos += self.velocity * time_step
        # print(self.name + " position: " + str(self.pos))

    def __eq__(self, other):
        if isinstance(other, CelestialBody):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name


class VirtualBody:
    def __init__(self, body: CelestialBody):
        self.position: Vector2 = body.pos
        self.velocity: Vector2 = body.velocity
        self.mass = body.mass




