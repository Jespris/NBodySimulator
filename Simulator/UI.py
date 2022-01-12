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
        self.type = "ui"
        self.image: p.image = None
        self.is_clickable = False

    def do_function(self):
        self.function()

    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.position.tuple())
        else:
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

    def update(self, delta_time):
        pass

    def get_clicked(self, mouse):
        if not self.is_clickable or not self.show:
            return False
        vector_mouse = Vector2(mouse[0], mouse[1])
        if self.is_circle:
            if max(self.width, self.height) >= (vector_mouse - self.position).magnitude():
                return True
        else:
            if self.position.x - self.width // 2 <= vector_mouse.x <= self.position.x + self.width // 2 and \
                    self.position.y - self.height // 2 <= vector_mouse.y <= self.position.y + self.height // 2:
                print("clicked on: " + self.name)
                return True
        return False


class Button(UI_Object):
    def __init__(self, name, pos, size, on_click, is_circle=False):
        super().__init__(name, pos, size, is_circle=is_circle)
        self.is_clicked = False
        self.on_click = on_click
        self.radius = max(self.width, self.height)
        self.click_color = p.Color("grey")
        self.click_time = 0.2  # time the button is greyed out (s)
        self.time_until_not_clicked = 0
        self.is_clickable = True
        self.prompt_text = ""
        self.text_size = min(self.width, self.height) // 2  # tweak this for better text fitting
        self.font = p.font.Font('freesansbold.ttf', self.text_size)
        self.bold = False

    def draw(self, screen):
        super().draw(screen)
        text_surface = self.font.render(self.prompt_text, self.bold, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position.tuple()
        screen.blit(text_surface, text_rect)
        if self.time_until_not_clicked > 0:
            if self.is_circle:
                radius = self.radius - self.border_thickness
                p.draw.circle(screen, self.click_color, self.position.tuple(), radius)
            else:
                p.draw.rect(screen, self.click_color,
                            p.Rect(self.position.x - self.width // 2 + self.border_thickness,
                                   self.position.y - self.height // 2 + self.border_thickness,
                                   self.width - 2 * self.border_thickness,
                                   self.height - 2 * self.border_thickness))

    def update(self, delta_time):
        if self.is_clicked:
            # print("button clicked")
            self.time_until_not_clicked = self.click_time
            if self.on_click is not None:
                self.on_click()
            self.is_clicked = False

        if self.time_until_not_clicked > 0:
            self.time_until_not_clicked -= delta_time / 1000

        if self.time_until_not_clicked < 0:
            self.time_until_not_clicked = 0


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
        self.active_color = self.COLOR_INACTIVE
        self.text_color = p.Color("black")
        self.is_clickable = True
        self.saved_text = ""
        self.prompt_text = ""

    def handle_event(self, event):
        updated_this = False
        mouse = p.mouse.get_pos()
        if event.type == p.MOUSEBUTTONDOWN:
            if self.get_clicked(mouse):
                self.active = not self.active
                print("Clicked on this form: " + self.name)
                updated_this = True
            else:
                self.active = False
            self.active_color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == p.KEYDOWN:
            if self.active:
                if event.key == p.K_RETURN:
                    self.saved_text = self.text
                    self.active = False
                elif event.key == p.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                updated_this = True

        return updated_this

    def draw(self, screen):
        text_surface = self.font.render(self.prompt_text + self.text, self.bold, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position.tuple()
        screen.blit(text_surface, text_rect)
        p.draw.rect(screen, self.active_color,
                    p.Rect(self.position.x - self.width // 2, self.position.y - self.height // 2,
                           self.width, self.height), 4)








