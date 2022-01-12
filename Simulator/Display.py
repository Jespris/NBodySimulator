"""
Display engine
"""

from Vector import Vector2
from SimulationEngine import SimulationEngine
import pygame as p
from Path import Path, CelestialPath
from UI import UI_Object, Button, TextObject, Form


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zoom_level = 5
        self.zoom_speed = 0.5
        self.offset = Vector2(self.width // 2, self.height // 2)
        self.camera_movement = Vector2.zero()
        self.camera_speed = 10
        self.last_mouse_pos = None
        self.mouse_down = False
        self.drag_speed = 0.1
        self.paths: list[Path] = []
        self.draw_relative_to_body = True
        self.show_paths = True
        self.delta_time = 0
        self.celestial_path = CelestialPath()
        self.ui_objects: list[UI_Object] = []
        self.forms: list[Form] = []
        self.ui_layers = 1
        self.create_ui_objects()

    def create_ui_objects(self):
        fps_counter = TextObject("FPS counter", Vector2(self.width - 80, 40), (50, 50), "99", self.get_fps)
        self.ui_objects.append(fps_counter)
        test_form = Form("test_form", Vector2(150, 40), (300, 40))
        self.forms.append(test_form)

    def update_deltatime(self, time):
        self.delta_time = time

    def get_fps(self):
        return "FPS: " + str(self.delta_time)

    def update_paths(self, engine: SimulationEngine):
        """
        if not self.paths and engine.isPaused:
            self.get_paths(engine)
        if not engine.isPaused:
            self.paths = []
        """
        if not engine.isPaused and self.show_paths:
            self.paths = self.celestial_path.get_paths(engine, self.draw_relative_to_body)

    def world_coordinate_to_screen_pixel(self, pos: Vector2):
        # (0, 0) is in the center of the screen
        # x increase is to the right
        # y increase is upwards
        return Vector2((pos.x * self.zoom_level) + self.offset.x, (-pos.y * self.zoom_level) + self.offset.y)

    def screen_pixel_to_world_coordinate(self, pos: Vector2):
        return Vector2((pos.x - self.offset.x) / self.zoom_level, -((pos.y - self.offset.y) / self.zoom_level))

    def draw_simulation(self, screen, engine: SimulationEngine):
        self.move_camera()
        self.draw_paths(screen)
        self.draw_bodies(screen, engine)
        self.draw_ui(screen)

    def draw_ui(self, screen):
        for layer in range(self.ui_layers):
            for ui in self.ui_objects:
                if ui.show:
                    if ui.layer == layer:
                        if ui.function is not None:
                            ui.do_function()
                        ui.draw(screen)
            for form in self.forms:
                if form.show:
                    if form.layer == layer:
                        form.draw(screen)

    def draw_paths(self, screen):
        if self.show_paths:
            for path in self.paths:
                for i in range(0, len(path.points) - 1):
                    start = self.world_coordinate_to_screen_pixel(path.points[i]).tuple()
                    end = self.world_coordinate_to_screen_pixel(path.points[i + 1]).tuple()
                    p.draw.line(screen, path.color, start, end, 4)

    def draw_bodies(self, screen, engine):
        for body in engine.bodies:
            screen_pos = self.world_coordinate_to_screen_pixel(body.pos)
            radius = body.radius * self.zoom_level
            p.draw.circle(screen, body.color, screen_pos.tuple(), radius)

    def move_camera(self):
        self.offset += self.camera_movement * self.camera_speed

    def camera_drag(self, mouse_pos):
        # ...
        if self.mouse_down:
            self.camera_movement = Vector2(mouse_pos[0] - self.last_mouse_pos[0], mouse_pos[1] - self.last_mouse_pos[1]) * self.drag_speed
        self.last_mouse_pos = mouse_pos

    def zoom(self, dir_amount):
        # zoom so that the world coordinate in the center of the screen stays the same
        new_level = self.zoom_level + dir_amount * self.zoom_speed
        if new_level < 0.2:
            new_level = 0.2
        elif new_level > 10:
            new_level = 10

        world_coord_in_center = self.screen_pixel_to_world_coordinate(Vector2(self.width // 2, self.height // 2))
        self.zoom_level = new_level
        # move camera so that world coordinate is in center
        self.move_camera_to_world_coordinate(world_coord_in_center)

    def move_camera_to_world_coordinate(self, pos: Vector2):
        # change offset by difference between screen pos of world coordinate and center of screen
        difference = Vector2(self.width // 2, self.height // 2) - self.world_coordinate_to_screen_pixel(pos)
        self.offset += difference


