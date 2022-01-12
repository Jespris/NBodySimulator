"""
Main Engine of simulation
"""
import random

import pygame as p

from CelestialBody import CelestialBody, NewCelestialBody
from Vector import Vector2
from Universe import Universe


class SimulationEngine:
    def __init__(self):
        self.bodies: list[CelestialBody] = []
        self.delta_time = 0
        self.simulation_speed = 0.001
        self.isPaused = True
        self.central_body: CelestialBody
        self.create_bodies()

        self.new_celestial_body = NewCelestialBody()
        self.new_in_progress = False

    def toggle_pause(self):
        self.isPaused = not self.isPaused

    def change_sim_speed(self, amount):
        new_speed = self.simulation_speed * amount
        if 0.00001 <= new_speed <= 0.1:
            self.simulation_speed = new_speed

    def Update(self, delta_time, display):
        self.delta_time = delta_time
        # print(self.central_body)
        # print("Delta time: " + str(self.delta_time) + "ms")
        if not self.isPaused:
            for body in self.bodies:
                acceleration = self.calculate_acceleration(body.pos, body)
                body.UpdateVelocity(acceleration, self.delta_time * self.simulation_speed)

            for body in self.bodies:
                body.UpdatePosition(self.delta_time * self.simulation_speed)

        display.update(delta_time, self.new_in_progress)

        self.update_new_body(display)

    def update_new_body(self, display):
        if self.new_in_progress:
            self.new_celestial_body.name = display.get_form_text("Name form")
            try:
                radius = int(display.get_form_text("Radius form"))
            except ValueError:
                # print("Invalid value for radius!")
                radius = 1
            if radius == 0:
                radius = 1
            self.new_celestial_body.radius = radius

            try:
                gravity = int(display.get_form_text("Gravity form"))
            except ValueError:
                # print("Invalid value for gravity!")
                gravity = 1
            self.new_celestial_body.gravity = gravity

            try:
                x = int(display.get_form_text("Pos form"))
                y = int(display.get_form_text("PosY form"))
                if x is None:
                    x = 0
                if y is None:
                    y = 0
                pos = Vector2(x, y)
            except (ValueError, TypeError):
                pos = Vector2.zero()
            self.new_celestial_body.pos = pos

            try:
                x = int(display.get_form_text("Vel form"))
                y = int(display.get_form_text("VelY form"))
                if x is None:
                    x = 0
                if y is None:
                    y = 0
                vel = Vector2(x, y)
            except (ValueError, TypeError):
                vel = Vector2.zero()
            self.new_celestial_body.initial_velocity = vel

            print("Updated the new celestial body stats:")
            print("name: " + self.new_celestial_body.name)
            print("radius: " + str(self.new_celestial_body.radius))
            print("gravity: " + str(self.new_celestial_body.gravity))
            print("position: " + str(self.new_celestial_body.pos))
            print("velocity: " + str(self.new_celestial_body.initial_velocity))

    def create_new_body(self):
        colors = ("blue", "red", "orange", "brown", "yellow", "green", "darkblue", "pink")
        newBody = CelestialBody(self.new_celestial_body.pos,
                                self.new_celestial_body.radius,
                                self.new_celestial_body.gravity,
                                self.new_celestial_body.initial_velocity,
                                self.new_celestial_body.name,
                                p.Color(colors[random.randint(0, len(colors) - 1)]))
        self.bodies.append(newBody)
        self.new_celestial_body = NewCelestialBody()

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
