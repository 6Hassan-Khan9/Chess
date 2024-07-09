import pygame
import pygame_menu
from pygame_menu import sound
import os
from selection import Selection
from main import Main
from const import *

class Menu:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Electronic Chess")
        pygame.display.set_icon(pygame.image.load(os.path.join("..", "assets", "images", "wolf-menu.png")))

        self.my_theme = pygame_menu.themes.THEME_DARK.copy()
        self.my_theme.background_color = (19, 20, 19)
        self.my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
        self.my_theme.title_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
        self.my_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
        self.my_theme.widget_font_shadow = False
        self.my_theme.widget_font_size = 36
        self.my_theme.widget_selection_effect = pygame_menu.widgets.SimpleSelection()

        self.menu = pygame_menu.Menu("Main Menu", WIDTH, HEIGHT, theme=self.my_theme)

        # engine = sound.Sound()
        # engine.set_sound(
        #     pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION,
        #     os.path.join("..", "assets", "sounds", "option.mp3"),
        #     1,
        # )
        # self.menu.set_sound(engine, recursive=True) 

        self.menu.add.button(
            "Player Versus Player",
            self.start_game,
            False,
            cursor=pygame_menu.locals.CURSOR_HAND,
            selection_color=(148, 134, 129, 10),
        )
        self.menu.add.button(
            "Player Versus Computer",
            self.start_game,
            True,
            cursor=pygame_menu.locals.CURSOR_HAND,
            selection_color=(148, 134, 129, 10),
        )
        self.menu.add.button(
            "Quit",
            pygame_menu.events.EXIT,
            cursor=pygame_menu.locals.CURSOR_HAND,
            selection_color=(186, 35, 50, 10),
        )
        self.menu.add.label(
            "Electronic Chess 2024",
            font_size=22,
            font_shadow=False,
            font_name=pygame_menu.font.FONT_OPEN_SANS_LIGHT
        ).translate(8, 260)
        self.menu.add.image(
        os.path.join("..", "assets", "images", "wolf-menu.png"),
        scale=(0.4, 0.4)
        ).translate(5, 25)
        self.menu.mainloop(self.screen)

    def start_game(self, *AI):
        selection = Selection()
        selected_side = selection.mainloop()
        if selected_side:
            main = Main(AI[0], selected_side)
            main.mainloop()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

if __name__ == "__main__":
    menu = Menu()
    menu.mainloop()
