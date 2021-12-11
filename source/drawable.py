import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.set_xy(0, 0)

    def set_xy(self, x, y):
        surface_size = pygame.display.get_surface().get_size()
        self.rect.center = (surface_size[0] / 2 + x, surface_size[1] / 2 + y)

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


class Font:
    def __init__(self, font_path, size):
        self.font = pygame.font.Font(font_path, size)
        self.text_surface = None
        self.text = ""
        self.is_dirty = True
        self.text_rect = None
        self.x = 0
        self.y = 0
        self.color = (0, 0, 0)

    def set_text(self, text):
        self.text = text
        self.is_dirty = True

    def set_xy(self, x, y):
        surface_size = pygame.display.get_surface().get_size()

        self.x = surface_size[0] / 2 + x
        self.y = surface_size[1] / 2 + y
        self.is_dirty = True

    def set_color(self, r, g, b):
        self.color = (r, g, b)
        self.is_dirty = True

    def update(self):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        if self.is_dirty:
            self.update()
            self.is_dirty = False

        screen.blit(self.text_surface, self.text_rect)
