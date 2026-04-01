import arcade
import pyglet
from menu.menu_intro.menu_intro import MenuIntro

path_window_icon = "sources/textures/UI/logo.png"
icon = pyglet.image.load(path_window_icon)
arcade.enable_timings()

class Game:
    def __init__(self):
        window.show_view(MenuIntro())

window = arcade.Window(fullscreen=True, vsync=True, width=1280, height=720, title="PlainQuest")
window.center_window()
window.activate()
window.set_icon(icon)

game = Game()
arcade.run()
