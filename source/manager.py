import pygame


def Singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


@Singleton
class SceneManager:
    def __init__(self):
        self.next_scene = None
        self.current_scene = None

    def update(self):
        if self.next_scene is not None:
            self.current_scene = self.next_scene
            self.next_scene = None

        if self.current_scene is not None:
            self.current_scene.update()

    def render(self):
        self.current_scene.render()

    def set_scene(self, scene):
        self.next_scene = scene
