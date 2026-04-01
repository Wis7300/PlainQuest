import arcade
import os

from menu.button_sprite import ButtonSprite
from menu.menu_save.menu_save import MenuSave
from menu.menu_control.menu_control import MenuControl

MENU_IMAGE = "textures/UI/menu_img.jpg"

click_sound = arcade.load_sound("sound+music/SFX/menu_click.mp3")


texture_to_title = "textures/UI/plain_quest.png"


class MenuStart(arcade.View):
    def __init__(self):
        super().__init__()

        self.music_menu_player = None
        self.music_menu = arcade.Sound("sound+music/music/menu_music.mp3")
        
        
        
        

        # Sprite du menu
        self.menu_sprite = arcade.Sprite(MENU_IMAGE, scale=1.0)
        self.menu_sprite.center_x = self.window.width // 2
        self.menu_sprite.center_y = self.window.height // 2
        self.menu_list = arcade.SpriteList()
        self.menu_list.append(self.menu_sprite)

        # Image du titre
        self.img1 = arcade.load_texture(texture_to_title)
        self.img1_rect = arcade.LBWH(left=self.window.width // 2 - (self.img1.width // 2),
                                    bottom=self.window.height - (self.img1.height + 50),
                                    height=self.img1.height,
                                    width=self.img1.width)

        # Boutons
        self.button_list = arcade.SpriteList()
        self.button_width = 300
        self.button_height = 60
        spacing = 30
        y_start = self.window.height // 2 + 50

        # Crée chaque bouton comme sprite
        names = ["JOUER", "CONTRÔLES", "QUITTER"]
        for i, name in enumerate(names):
            y = y_start - i * (self.button_height + spacing)
            btn = ButtonSprite(
                center_x=self.window.width // 2,
                center_y=y,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text=name
            )
            self.button_list.append(btn)
        
        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y

    def on_draw(self):
        self.camera.use()
        self.clear()
        self.menu_list.draw()
        arcade.draw_texture_rect(texture=self.img1,
                                     rect=self.img1_rect)
        self.button_list.draw()
        # Dessiner le texte sur les boutons
        for btn in self.button_list:
            btn.label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Vérifie quel bouton est cliqué
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                if btn.text == "JOUER":
                    self.show_save()
                elif btn.text == "CONTRÔLES":
                    self.window.show_view(MenuControl())
                elif btn.text == "QUITTER":
                    arcade.close_window()
                click_sound.play()

    def on_mouse_motion(self, x, y, dx, dy):

        for btn in self.button_list:
            condition = (btn.center_x - btn.base_width / 2 <= x <= btn.center_x + btn.base_width / 2 and 
            btn.center_y - btn.base_height / 2 <= y <= btn.center_y + btn.base_height / 2)
            
            if condition:
            
                btn.width = btn.base_width + 10
                btn.height = btn.base_height + 10
            else:
                
                btn.width = self.button_width
                btn.height = self.button_height

    def on_show_view(self):
        self.music_menu_player = self.music_menu.play(loop=True, volume=0.2)
        

    def show_save(self):
        self.window.show_view(MenuSave(self))
        
