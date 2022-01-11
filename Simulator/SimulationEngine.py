"""
Main Engine of simulation
"""
import pygame as p

from CelestialBody import CelestialBody
from Vector import Vector2
from Universe import Universe


class SimulationEngine:
    def __init__(self):
        self.bodies: list[CelestialBody] = []
        self.delta_time = 0
        self.simulation_speed = 0.001
        self.isPaused = True
        self.create_bodies()
        self.central_body = None

    def toggle_pause(self):
        self.isPaused = not self.isPaused

    def Update(self, delta_time):
        self.delta_time = delta_time
        # print("Delta time: " + str(self.delta_time) + "ms")
        if not self.isPaused:
            for body in self.bodies:
                acceleration = self.calculate_acceleration(body.pos, body)
                body.UpdateVelocity(acceleration, self.delta_time * self.simulation_speed)

            for body in self.bodies:
                body.UpdatePosition(self.delta_time * self.simulation_speed)

    def create_bodies(self):
        self.bodies.append(CelestialBody(Vector2(0, -25), 10, 100, Vector2(5, 0), "Sun", p.Color("yellow")))
        self.central_body = self.bodies[0]
        self.bodies.append(CelestialBody(Vector2(50, 70), 1, 1, Vector2(40, -40), "Planet", p.Color("blue")))

    def calculate_acceleration(self, point: Vector2, ignore_body):
        acceleration = Vector2.zero()
        for otherBody in self.bodies:
            if otherBody != ignore_body:
                square_distance = (otherBody.pos - point).magnitude()
                force_direction = (otherBody.pos - point).normalize()
                # print(force_direction)
                acceleration += force_direction * Universe.Big_G * otherBody.mass / square_distance
                # print("Acceleration: " + str(acceleration))
        return acceleration
