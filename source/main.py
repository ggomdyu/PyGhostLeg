import os
import manager
import drawable
import pygame
import random

print("Enter the number of participants.")
member_count = int(input())
print("Enter the names of participants.")
participants = []
for i in range(member_count):
    participants.append(input())
print("Enter the number of legs to draw.")
max_depth = int(input())
blank_index = random.randint(0, member_count - 1)


def make_leg_table():
    leg_table = [[0 for y in range(member_count)] for x in range(max_depth)]
    for i in range(0, max_depth):
        member_a = random.randint(0, member_count - 2)
        member_b = member_a + 1
        leg_table[i][member_a] = 1
        leg_table[i][member_b] = 1

    return leg_table


def traverse_leg(leg_id, leg_table):
    current_x = leg_id
    current_depth = max_depth - 1
    paths = []

    while current_depth >= 0:
        if leg_table[current_depth][current_x] == 0:
            paths.append((current_x, current_x))
        elif current_x > 0 and leg_table[current_depth][current_x - 1] == 1:
            paths.append((current_x, current_x - 1))
            current_x = current_x - 1
        elif current_x < member_count - 1 and leg_table[current_depth][current_x + 1] == 1:
            paths.append((current_x, current_x + 1))
            current_x = current_x + 1
        current_depth -= 1

    return paths


class GameScene:
    def __init__(self, screen):
        self.sprites = pygame.sprite.Group()
        self.fonts = []
        self.blank_participant = ""
        self.screen = screen
        self.scene_manager = manager.SceneManager()
        self.leg_width = 100
        self.leg_height = 50

        self.init_background()
        self.init_legs()
        self.init_texts()

    def init_background(self):
        self.add_sprite(drawable.Sprite("assets/image/background.png"), 0, 0)

    def init_texts(self):
        for i in range(0, len(participants)):
            x = (member_count - 1) * -self.leg_height + i * self.leg_width
            self.add_font(participants[i], x, self.calc_leg_y(0, self.leg_height) - 50)
            self.add_font("꽝" if i == blank_index else "O", x, -self.calc_leg_y(0, self.leg_height) + 50)

        self.add_font(self.blank_participant + "님 당신은 꽝입니다!", 0, self.screen.get_height() / 2 - 50)

    def calc_leg_y(self, y, height):
        ret = y * height + (max_depth - 1) / 2 * -height
        if max_depth % 2 == 0:
            ret -= height / 2

        return ret

    def init_legs(self):
        # Render x-axis lines.
        legs = make_leg_table()
        for y in range(0, max_depth):
            for x in range(0, member_count - 1):
                if legs[y][x] == 1:
                    leg_x = (member_count - 2) * -self.leg_height + x * self.leg_width
                    leg_y = self.calc_leg_y(y, self.leg_height)
                    self.add_sprite(drawable.Sprite("assets/image/leg2.png"), leg_x, leg_y)
                    break

        # Render y-axis lines.
        for y in range(0, max_depth):
            for x in range(0, member_count):
                leg_x = (member_count - 1) * -self.leg_height + x * self.leg_width
                leg_y = self.calc_leg_y(y, self.leg_height)
                self.add_sprite(drawable.Sprite("assets/image/leg.png"), leg_x, leg_y)

        paths = traverse_leg(blank_index, legs)
        x = 0
        y = len(paths)
        for path in paths:
            y -= 1

            # Render x-axis red lines.
            leg_down_x = (member_count - 1) * -self.leg_height + path[0] * self.leg_width
            leg_up_x = (member_count - 1) * -self.leg_height + path[1] * self.leg_width
            leg_y = self.calc_leg_y(y, self.leg_height)
            self.add_sprite(drawable.Sprite("assets/image/red_leg_down.png"), leg_down_x, leg_y)
            self.add_sprite(drawable.Sprite("assets/image/red_leg_up.png"), leg_up_x, leg_y)

            # Render y-axis red lines.
            if path[0] != path[1]:
                x = min(path[0], path[1])
                self.add_sprite(drawable.Sprite("assets/image/red_leg2.png"),
                                (member_count - 2) * -self.leg_height + x * self.leg_width, leg_y)

            x += 1

        self.blank_participant = participants[paths[len(legs) - 1][1]]
        pass

    def add_sprite(self, sprite, x, y):
        sprite.set_xy(x, y)
        self.sprites.add(sprite)

    def add_font(self, text, x, y):
        font = drawable.Font("assets/font/DOSMyungjo.ttf", 20)
        font.set_text(text)
        font.set_xy(x, y)
        font.set_color(0, 0, 0)
        self.fonts.append(font)

    def update(self):
        self.sprites.update()

    def render(self):
        self.sprites.draw(self.screen)

        for font in self.fonts:
            font.draw(self.screen)


def main():
    os.chdir(os.path.join(os.path.dirname(__file__), "../"))

    pygame.init()
    pygame.display.set_caption("PyGhostLeg")

    sm = manager.SceneManager()
    sm.set_scene(GameScene(pygame.display.set_mode([480, 800])))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sm.update()
        sm.render()
        pygame.display.flip()


if __name__ == "__main__":
    main()
