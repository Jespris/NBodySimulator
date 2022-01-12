"""
Contains UI elements
"""


from Vector import Vector2
import pygame as p


class UI_Object:
    def __init__(self, name, pos: Vector2, size, color=p.Color("white"), is_circle=False, function=None):
        self.name = name
        self.position: Vector2 = pos
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.has_border = False
        self.border_thickness = 2
        self.is_circle = is_circle
        self.layer = 0
        self.show = True
        self.function = function

    def do_function(self):
        self.function()

    def draw(self, screen):
        if self.is_circle:
            if self.has_border:
                p.draw.circle(screen, p.Color("black"), self.position.tuple(), max(self.width, self.height))
            p.draw.circle(screen, self.color, self.position.tuple(),
                          max(self.width - self.border_thickness, self.height - self.border_thickness))
        else:
            # rectangle
            if self.has_border:
                p.draw.rect(screen, p.Color("black"),
                            p.Rect(self.position.x - self.width // 2, self.position.y - self.height // 2,
                                   self.width, self.height))
            p.draw.rect(screen, self.color, p.Rect(self.position.x - self.width // 2 + self.border_thickness,
                                                   self.position.y - self.height // 2 + self.border_thickness,
                                                   self.width - 2 * self.border_thickness,
                                                   self.height - 2 * self.border_thickness))


class Button(UI_Object):
    def __init__(self, name, pos, size, on_click, is_circle=False):
        super().__init__(name, pos, size, is_circle=is_circle)
        self.is_clicked = False
        self.on_click = on_click
        self.radius = max(self.width, self.height)
        self.click_color = p.Color("grey")

    def draw(self, screen):
        super().draw(screen)
        if self.is_clicked:
            if self.is_circle:
                radius = self.radius - self.border_thickness
                p.draw.circle(screen, self.click_color, self.position.tuple(), radius)
            else:
                p.draw.rect(screen, self.click_color,
                            p.Rect(self.position.x - self.width // 2 + self.border_thickness,
                                   self.position.y - self.height // 2 + self.border_thickness,
                                   self.width - 2 * self.border_thickness,
                                   self.height - 2 * self.border_thickness))


class TextObject(UI_Object):
    def __init__(self, name, pos, size, text, text_function=None):
        super().__init__(name, pos, size, function=text_function)
        self.text = text
        self.text_size = min(self.width, self.height) // 2  # tweak this for better text fitting
        self.font = p.font.Font('freesansbold.ttf', self.text_size)
        self.bold = False

    def draw(self, screen):
        text_surface = self.font.render(self.text, self.bold, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position.tuple()
        screen.blit(text_surface, text_rect)

    def do_function(self):
        self.text = self.function()


class Form(TextObject):

    COLOR_INACTIVE = p.Color("white")
    COLOR_ACTIVE = p.Color("grey")

    def __init__(self, name, pos, size):
        super().__init__(name, pos, size, "")
        self.active = False
        self.input_box = p.Rect(self.position.x - self.width // 2, self.position.y - self.height // 2,
                                self.width, self.height)
        self.active_color = self.COLOR_INACTIVE
        self.text_color = p.Color("black")

    def handle_event(self, event):
        updated_this = False
        if event.type == p.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = not self.active
                print("Clicked on this form: " + self.name)
                updated_this = True
            else:
                self.active = False
            self.active_color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == p.KEYDOWN:
            if self.active:
                if event.key == p.K_RETURN:
                    print("Submitted form with text: " + self.text)
                    self.text = ""
                elif event.key == p.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                updated_this = True

        return updated_this

    def draw(self, screen):
        super().draw(screen)
        p.draw.rect(screen, self.active_color, self.input_box, 2)








