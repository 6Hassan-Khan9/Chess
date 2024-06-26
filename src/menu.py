import pygame
import pygame_menu
from pygame_menu import sound
import os
from main import Main
from const import *

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load(os.path.join("..", "assets", "chess.png")))


def start_game(*AI):
    main = Main(AI[0])
    main.mainloop()


if __name__ == "__main__":

    my_theme = pygame_menu.themes.THEME_DARK.copy()

    my_theme.title = False
    my_theme.background_color = pygame_menu.baseimage.BaseImage(
        image_path=os.path.join("..", "assets", "bg.png"),
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
    )
    my_theme.widget_font = pygame_menu.font.FONT_MUNRO
    my_theme.widget_font_shadow = True
    my_theme.widget_font_shadow_color = (0, 0, 0)
    my_theme.widget_font_size = 48
    my_theme.widget_font_shadow_offset = 3
    my_theme.widget_selection_effect = pygame_menu.widgets.SimpleSelection()

    menu = pygame_menu.Menu("Chess", WIDTH, HEIGHT, theme=my_theme)

    engine = sound.Sound()

    engine.set_sound(
        pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION,
        os.path.join("..", "assets", "sounds", "option.mp3"),
        1,
    )

    menu.set_sound(engine, recursive=True)  # Apply on menu and all sub-menus

    menu.add.button(
        "Player Versus Player",
        start_game,
        False,
        cursor=pygame_menu.locals.CURSOR_HAND,
        selection_color=(151, 186, 35, 10),
    )
    menu.add.button(
        "Player Versus Computer",
        start_game,
        True,
        cursor=pygame_menu.locals.CURSOR_HAND,
        selection_color=(151, 186, 35, 10),
    )
    menu.add.button(
        "Quit",
        pygame_menu.events.EXIT,
        cursor=pygame_menu.locals.CURSOR_HAND,
        selection_color=(186, 35, 50, 10),
    )

    menu.mainloop(surface)
