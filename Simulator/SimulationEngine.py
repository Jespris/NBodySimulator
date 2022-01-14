"""
Main Engine of simulation
"""
import math
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
        self.central_body: CelestialBody = None
        # self.create_solar_system()
        self.create_binary_system()

        self.new_celestial_body = NewCelestialBody()
        self.new_in_progress = False

    def toggle_pause(self):
        self.isPaused = not self.isPaused

    def toggle_new_body(self):
        self.new_in_progress = not self.new_in_progress
        if self.new_in_progress:
            self.new_celestial_body = NewCelestialBody()

    def change_sim_speed(self, amount):
        new_speed = self.simulation_speed * amount
        if 0.0000001 <= new_speed <= 0.001:
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
        print("Creating new body!")
        colors = ("blue", "red", "orange", "brown", "yellow", "green", "darkblue", "pink")
        newBody = CelestialBody(self.new_celestial_body.pos,
                                self.new_celestial_body.radius,
                                self.new_celestial_body.gravity, 1,
                                self.new_celestial_body.initial_velocity,
                                self.new_celestial_body.name,
                                p.Color(colors[random.randint(0, len(colors) - 1)]))
        self.bodies.append(newBody)
        self.new_celestial_body = NewCelestialBody()
        self.new_in_progress = False

    def create_solar_system(self):
        # data for ratio between distances from https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html
        sun_radius = 109
        # earth radius is 1
        # earth mass is 1
        # earth density is 1
        self.bodies.append(CelestialBody(Vector2(0, 0), sun_radius, 333000, 0.26, Vector2(12000, 0), "Sun", p.Color("yellow")))
        self.central_body = self.bodies[0]

        earth_pos = Vector2(sun_radius * 215, 0)
        self.bodies.append(CelestialBody(earth_pos, 1, 1, 1, self.get_init_velocity_for_circular_orbit(self.bodies[0], earth_pos) * 155, "Earth", p.Color("blue")))

        """
        moon_pos = earth_pos + Vector2(60, 0)
        self.bodies.append(CelestialBody(moon_pos, 0.27, 0.17, 0.6,
                                         self.get_init_velocity_for_circular_orbit(self.bodies[0], moon_pos) * 160 +
                                         self.get_init_velocity_for_circular_orbit(self.bodies[1], moon_pos - earth_pos) * 20,
                                         "Moon", p.Color("grey")))
        """

        mercury_pos = Vector2(sun_radius * 66, 0)
        self.bodies.append(
            CelestialBody(mercury_pos, 0.38, 0.38, 0.99, self.get_init_velocity_for_circular_orbit(self.bodies[0], mercury_pos) * 90,
                          "Mercury", p.Color("grey")))

        venus_pos = Vector2(sun_radius * 155, 0)
        self.bodies.append(
            CelestialBody(venus_pos, 0.95, 0.91, 0.95,
                          self.get_init_velocity_for_circular_orbit(self.bodies[0], venus_pos) * 130,
                          "Venus", p.Color("burlywood4")))

        mars_pos = earth_pos * 1.5
        self.bodies.append(
            CelestialBody(mars_pos, 0.53, 0.38, 0.71,
                          self.get_init_velocity_for_circular_orbit(self.bodies[0], mars_pos) * 190,
                          "Mars", p.Color("red")))

        jupiter_pos = earth_pos * 5.2
        self.bodies.append(
            CelestialBody(jupiter_pos, 11, 2.4, 0.24,
                          self.get_init_velocity_for_circular_orbit(self.bodies[0], jupiter_pos) * 350,
                          "Jupiter", p.Color("bisque3")))

        saturn_pos = earth_pos * 9.6
        self.bodies.append(
            CelestialBody(saturn_pos, 9.5, 0.92, 0.13,
                          self.get_init_velocity_for_circular_orbit(self.bodies[0], saturn_pos) * 450,
                          "Saturn", p.Color("bisque")))

        uranus_pos = earth_pos * 19.2
        self.bodies.append(
            CelestialBody(uranus_pos, 4, 0.89, 0.23,
                          self.get_init_velocity_for_circular_orbit(self.bodies[0], uranus_pos) * 650,
                          "Uranus", p.Color("cadetblue1")))

        neptune_pos = earth_pos * 30.2
        self.bodies.append(
            CelestialBody(neptune_pos, 3.9, 1.1, 0.30,
                          self.get_init_velocity_for_circular_orbit(self.bodies[0], neptune_pos) * 800,
                          "Neptune", p.Color("cadetblue4")))

    def create_binary_system(self):
        self.bodies.append(
            CelestialBody(Vector2(0, 0), 200, 333000, 0.26, Vector2(0, 20000), "Sun", p.Color("yellow")))
        self.bodies.append(
            CelestialBody(Vector2(100000, 0), 200, 333000, 0.26, Vector2(0, -20000), "Sun2", p.Color("blue")))
        self.bodies.append(
            CelestialBody(Vector2(500000, 0), 3.9, 1.1, 0.30,
                          Vector2(0, -80000),
                          "Planet", p.Color("red")))
        self.bodies.append(
            CelestialBody(Vector2(250000, 0), 3.9, 1.1, 0.30,
                          Vector2(0, -40000),
                          "Planet", p.Color("green")))
        self.bodies.append(
            CelestialBody(Vector2(10000, 0), 3.9, 1.1, 0.30,
                          Vector2(0, -8000),
                          "Planet", p.Color("chocolate")))

    @staticmethod
    def get_init_velocity_for_circular_orbit(parent: CelestialBody, pos: Vector2):
        distance = (parent.pos - pos).magnitude()
        wanted_speed = math.sqrt(Universe.Big_G * parent.mass / distance)
        child_pos_unit_vector = (parent.pos - pos).normalize()
        child_angle_to_parent = child_pos_unit_vector.angle()
        init_velocity = Vector2(math.sin(child_angle_to_parent) * child_pos_unit_vector.y * wanted_speed,
                                -math.cos(child_angle_to_parent) * child_pos_unit_vector.x * wanted_speed)
        print("magnitude:", init_velocity.magnitude(), "wanted speed:", wanted_speed)
        return init_velocity

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
