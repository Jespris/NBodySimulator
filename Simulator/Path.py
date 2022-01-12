from Vector import Vector2
from CelestialBody import VirtualBody
from SimulationEngine import SimulationEngine
from Universe import Universe


class Path:
    def __init__(self):
        self.points: list[Vector2] = []
        self.color = None


class CelestialPath:
    def __init__(self):
        self.virtual_bodies: list[VirtualBody] = []
        self.reference_index = 0
        self.central_body = None
        self.reference_initial_position = Vector2.zero()
        self.num_steps = 500
        self.time_step = 0.1

    def get_paths(self, engine: SimulationEngine, get_relative):
        self.central_body = engine.central_body
        # print("Central body:", str(self.central_body))
        paths: list[Path] = []
        self.virtual_bodies = []
        # initialize virtual bodies (don't move actual bodies)
        for body in engine.bodies:
            new_virtual = VirtualBody(body)
            self.virtual_bodies.append(new_virtual)
            newPath = Path()
            newPath.color = body.color
            paths.append(newPath)

            if body == self.central_body and get_relative:
                # print("Reference body found!")
                self.reference_index = engine.bodies.index(body)
                self.reference_initial_position = body.pos

        # simulate
        for step in range(self.num_steps):
            reference_body_pos = self.virtual_bodies[self.reference_index].position if get_relative else Vector2.zero()
            # update velocities
            for i in range(len(self.virtual_bodies)):
                self.virtual_bodies[i].velocity += self.calculate_acceleration(i, self.virtual_bodies) * self.time_step

            # update positions
            for i in range(len(self.virtual_bodies)):
                newPos = self.virtual_bodies[i].position + self.virtual_bodies[i].velocity * self.time_step
                self.virtual_bodies[i].position = newPos
                if get_relative:
                    reference_offset = reference_body_pos - self.reference_initial_position
                    newPos -= reference_offset

                if get_relative and i == self.reference_index:
                    newPos = self.reference_initial_position

                try:
                    paths[i].points.append(newPos)
                except IndexError:
                    print("Error, index", i, "out of range!")

        return paths

    @staticmethod
    def calculate_acceleration(i, virtual_bodies):
        acceleration = Vector2.zero()
        for j in range(len(virtual_bodies)):
            if i == j:
                continue
            force_dir = (virtual_bodies[j].position - virtual_bodies[i].position).normalize()
            distance = (virtual_bodies[j].position - virtual_bodies[i].position).magnitude()
            acceleration += force_dir * Universe.Big_G * virtual_bodies[j].mass / distance

        return acceleration
