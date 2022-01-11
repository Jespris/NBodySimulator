"""
Main

TODO:
    - fix camera zoom to center correctly
    - fix relative to center body line draw thingy
    - implement adding celestial bodies live
    - implement time controls
"""
import math

import pygame as p
from win32api import GetSystemMetrics
from Vector import Vector2
from SimulationEngine import SimulationEngine
from Display import Display

# GLOBALS
SCREENSIZE = 1
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
    test()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    running = False
                elif e.key == p.K_SPACE:
                    Simulation_Engine.toggle_pause()
                ResolveKeyDownAxis(e.key, display)

            elif e.type == p.KEYUP:
                ResolveKeyUpAxis(e.key, display)

            elif e.type == p.MOUSEWHEEL:
                # print(e.y)
                display.zoom_level += e.y * display.zoom_speed

            elif e.type == p.MOUSEBUTTONDOWN:
                display.mouse_down = True
                display.last_mouse_pos = p.mouse.get_pos()

            elif e.type == p.MOUSEBUTTONUP:
                display.mouse_down = False
                display.camera_movement = Vector2.zero()

        p.display.flip()
        screen.fill(p.Color("black"))
        display.update_paths(Simulation_Engine)
        display.camera_drag(p.mouse.get_pos())
        display.draw_simulation(screen, Simulation_Engine)
        delta_time = clock.tick(FPS)
        Simulation_Engine.Update(delta_time)


def ResolveKeyDownAxis(key, display):
    if key == p.K_LEFT or key == p.K_a:
        display.camera_movement.x = 1
    elif key == p.K_RIGHT or key == p.K_d:
        display.camera_movement.x = -1
    if key == p.K_UP or key == p.K_w:
        display.camera_movement.y = 1
    elif key == p.K_DOWN or key == p.K_s:
        display.camera_movement.y = -1


def ResolveKeyUpAxis(key, display):
    if key == p.K_LEFT or key == p.K_a or key == p.K_RIGHT or key == p.K_d:
        display.camera_movement.x = 0
    if key == p.K_UP or key == p.K_w or key == p.K_DOWN or key == p.K_s:
        display.camera_movement.y = 0


def test():
    print(Vector2(5, 1).normalize())


if __name__ == "__main__":
    main()


