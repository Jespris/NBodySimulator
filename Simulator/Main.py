"""
Main

TODO:
    - implement adding celestial bodies live
"""

import pygame as p
from win32api import GetSystemMetrics
from Vector import Vector2
from SimulationEngine import SimulationEngine
from Display import Display, FORM, BUTTON

# GLOBALS
SCREENSIZE = 0.6
WIDTH = int(GetSystemMetrics(0) * SCREENSIZE)
HEIGHT = int(GetSystemMetrics(1) * SCREENSIZE)
FPS = 30


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("N-Body Simulator")
    screen.fill(p.Color("black"))
    clock = p.time.Clock()
    Simulation_Engine = SimulationEngine()
    display = Display(WIDTH, HEIGHT)
    display.create_ui_objects(Simulation_Engine)
    # test(display)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    running = False
                ResolveKeyDown(e, display, Simulation_Engine)

            elif e.type == p.KEYUP:
                ResolveKeyUpAxis(e.key, display)

            elif e.type == p.MOUSEWHEEL:
                # print(e.y)
                display.zoom(e.y)

            elif e.type == p.MOUSEBUTTONDOWN:
                done = Resolve_UI_Click(e, display)
                if not done:
                    display.mouse_down = True
                    display.last_mouse_pos = p.mouse.get_pos()

            elif e.type == p.MOUSEBUTTONUP:
                display.mouse_down = False
                display.camera_movement = Vector2.zero()

        p.display.flip()
        screen.fill(p.Color("black"))
        delta_time = clock.tick(FPS)
        Simulation_Engine.Update(delta_time, display)
        display.update_paths(Simulation_Engine)
        display.camera_drag(p.mouse.get_pos())
        display.draw_simulation(screen, Simulation_Engine)


def Resolve_UI_Click(e, display):
    for ui in display.ui_objects:
        done = False
        if ui.type == FORM:
            done = ui.handle_event(e)
        elif ui.type == BUTTON:
            done = ui.is_clicked = ui.get_clicked(p.mouse.get_pos())

        if done:
            return True
    return False


def ResolveKeyDown(event, display, engine):
    for ui in display.ui_objects:
        if ui.type == FORM:
            done = ui.handle_event(event)
            if done:
                return

    key = event.key

    if key == p.K_LEFT or key == p.K_a:
        display.camera_movement.x = 1
    elif key == p.K_RIGHT or key == p.K_d:
        display.camera_movement.x = -1
    if key == p.K_UP or key == p.K_w:
        display.camera_movement.y = 1
    elif key == p.K_DOWN or key == p.K_s:
        display.camera_movement.y = -1

    if key == p.K_z:
        engine.change_sim_speed(0.1)
    elif key == p.K_x:
        engine.change_sim_speed(10)

    if key == p.K_c:
        display.show_paths = not display.show_paths

    if key == p.K_SPACE:
        engine.toggle_pause()


def ResolveKeyUpAxis(key, display):
    if key == p.K_LEFT or key == p.K_a or key == p.K_RIGHT or key == p.K_d:
        display.camera_movement.x = 0
    if key == p.K_UP or key == p.K_w or key == p.K_DOWN or key == p.K_s:
        display.camera_movement.y = 0


def test(display):
    screen_pos = display.world_coordinate_to_screen_pixel(Vector2(2, 2))
    print("Screen pos of world coordinate (2, 2) is: " + str(screen_pos))
    print("World pos of screen coordinate " + str(screen_pos) + " is: " + str(display.screen_pixel_to_world_coordinate(screen_pos)))


if __name__ == "__main__":
    main()
    p.quit()


