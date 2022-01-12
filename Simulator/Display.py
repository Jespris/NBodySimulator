"""
Display engine
"""
import random

from Vector import Vector2
from SimulationEngine import SimulationEngine
import pygame as p
from Path import Path, CelestialPath
from UI import UI_Object, Button, TextObject, Form


# UI Types
BUTTON = "button"
UI = "ui"
FORM = "form"
TEXT = "text"


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
        self.show_new_panel = False
        self.delta_time = 0
        self.celestial_path = CelestialPath()
        self.ui_objects: list[UI_Object] = []
        self.ui_layers = 2

        self.background_stars = []
        self.create_background_stars(500)

    def create_background_stars(self, number):
        for i in range(number):
            self.background_stars.append((random.randint(0, self.width), random.randint(0, self.height)))

    def create_ui_objects(self, engine: SimulationEngine):
        fps_counter = TextObject("FPS counter", Vector2(self.width - 80, 40), (50, 50), "99", self.get_fps)
        self.ui_objects.append(fps_counter)

        new_body_panel = UI_Object("New Celestial Body Panel", Vector2(self.width // 2, 120), (320, 240), color=p.Color("grey4"))
        self.ui_objects.append(new_body_panel)

        name_form = Form("Name form", Vector2(self.width // 2, 20), (200, 40))
        name_form.layer = 1
        name_form.type = FORM
        name_form.prompt_text = "Name: "
        self.ui_objects.append(name_form)

        radius_form = Form("Radius form", Vector2(self.width // 2, 60), (200, 40))
        radius_form.layer = 1
        radius_form.type = FORM
        radius_form.prompt_text = "Radius: "
        self.ui_objects.append(radius_form)

        gravity_form = Form("Gravity form", Vector2(self.width // 2, 100), (200, 40))
        gravity_form.layer = 1
        gravity_form.type = FORM
        gravity_form.prompt_text = "Gravity: "
        self.ui_objects.append(gravity_form)

        pos_form = Form("Pos form", Vector2(self.width // 2 - 40, 140), (120, 40))
        pos_form.layer = 1
        pos_form.type = FORM
        pos_form.prompt_text = "Pos x: "
        self.ui_objects.append(pos_form)

        posY_form = Form("PosY form", Vector2(self.width // 2 + 60, 140), (80, 40))
        posY_form.layer = 1
        posY_form.type = FORM
        posY_form.prompt_text = "y: "
        self.ui_objects.append(posY_form)

        vel_form = Form("Vel form", Vector2(self.width // 2 - 40, 180), (120, 40))
        vel_form.layer = 1
        vel_form.type = FORM
        vel_form.prompt_text = "Vel x: "
        self.ui_objects.append(vel_form)

        velY_form = Form("VelY form", Vector2(self.width // 2 + 60, 180), (80, 40))
        velY_form.layer = 1
        velY_form.type = FORM
        velY_form.prompt_text = "y: "
        self.ui_objects.append(velY_form)

        pause_button = Button("Pause Button", Vector2(30, self.height - 30), (30, 30), engine.toggle_pause)
        pause_button.type = BUTTON
        self.ui_objects.append(pause_button)

        new_body_button = Button("NewBody Button", Vector2(self.width // 2, 220), (200, 40), engine.create_new_body())
        new_body_button.type = BUTTON
        new_body_button.layer = 1
        new_body_button.prompt_text = "Create New!"
        self.ui_objects.append(new_body_button)

    def get_form_text(self, form_name):
        for ui in self.ui_objects:
            if ui.type == FORM:
                if ui.name == form_name:
                    return ui.saved_text

    def update(self, time, newBody):
        self.delta_time = time
        for ui in self.ui_objects:
            ui.update(self.delta_time)
        self.show_new_panel = newBody


    def get_fps(self):
        return "FPS: " + str(self.delta_time)

    def update_paths(self, engine: SimulationEngine):
        """
        if not self.paths and engine.isPaused:
            self.get_paths(engine)
        if not engine.isPaused:
            self.paths = []
        """
        if self.show_paths:
            self.paths = self.celestial_path.get_paths(engine, self.draw_relative_to_body, self.show_new_panel)

    def world_coordinate_to_screen_pixel(self, pos: Vector2):
        # (0, 0) is in the center of the screen
        # x increase is to the right
        # y increase is upwards
        return Vector2((pos.x * self.zoom_level) + self.offset.x, (-pos.y * self.zoom_level) + self.offset.y)

    def screen_pixel_to_world_coordinate(self, pos: Vector2):
        return Vector2((pos.x - self.offset.x) / self.zoom_level, -((pos.y - self.offset.y) / self.zoom_level))

    def draw_simulation(self, screen, engine: SimulationEngine):
        self.move_camera()
        self.draw_stars(screen)
        self.draw_paths(screen)
        self.draw_bodies(screen, engine)
        self.draw_ui(screen)

    def draw_stars(self, screen):
        for star in self.background_stars:
            screen.set_at(star, p.Color("white"))

    def draw_ui(self, screen):
        new_body_elements = ("Name form", "Gravity form", "Radius form", "Pos form", "PosY form",
                             "Vel form", "VelY form", "NewBody Button", "New Celestial Body Panel")
        for ui in self.ui_objects:
            for name in new_body_elements:
                if ui.name == name:
                    ui.show = self.show_new_panel
        for layer in range(self.ui_layers):
            for ui in self.ui_objects:
                if ui.show:
                    if ui.layer == layer:
                        if ui.function is not None:
                            ui.do_function()
                        ui.draw(screen)

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


