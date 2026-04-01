import arcade
import os

from menu.button_sprite import ButtonSprite
from save.save import delete_file
from logic import GameView


click_sound = arcade.load_sound("sound+music/SFX/menu_click.mp3")
MENU_IMAGE = "textures/UI/menu_img.jpg"


class MenuSave(arcade.View):
    def __init__(self, menu_start=None):
        super().__init__()

        self.menu_start = menu_start
        self.menu_music = self.menu_start.music_menu
        self.menu_music_player = self.menu_start.music_menu_player

        # Sprite du menu
        self.menu_sprite = arcade.Sprite(MENU_IMAGE, scale=1.0)
        self.menu_sprite.center_x = self.window.width // 2
        self.menu_sprite.center_y = self.window.height // 2
        self.menu_list = arcade.SpriteList()
        self.menu_list.append(self.menu_sprite)

        # Boutons
        self.button_list = arcade.SpriteList()
        self.button_width = 300
        self.button_height = 60
        spacing = 30
        y_start = self.window.height // 2 + 20

        # Crée chaque bouton comme sprite
        # A gauche
        names = ["SAUVEGARDE-1", "SAUVEGARDE-2", "SAUVEGARDE-3"]
        for i, name in enumerate(names):
            y = y_start - i * (self.button_height + spacing) + 100
            btn = ButtonSprite(
                center_x=self.window.width // 2 - 200,
                center_y=y,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text=name
            )
            self.button_list.append(btn)

        # A droite
        del_names = ["Supprimer 1 ?", "Supprimer 2 ?", "Supprimer 3 ?"]
        for i, name in enumerate(del_names):
            y = y_start - i * (self.button_height + spacing) + 100
            btn = ButtonSprite(
                center_x=self.window.width // 2 + 200,
                center_y=y,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text=name
            )
            self.button_list.append(btn)
        
        # Au centre
        btn = ButtonSprite(
                center_x=self.window.width // 2,
                center_y=200,
                width=self.button_width,
                height=self.button_height,
                color=(255, 255, 255, 180),  # blanc semi-transparent
                text="RETOUR"
            )
        self.button_list.append(btn)

        
        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y

    def on_draw(self):
        self.camera.use()
        self.clear()
        self.menu_list.draw()
        self.button_list.draw()
        # Dessiner le texte sur les boutons
        for btn in self.button_list:
            btn.label.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        # Vérifie quel bouton est cliqué
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                if btn.text == "SAUVEGARDE-1":
                    self.show_game("save1.json")
                elif btn.text == "SAUVEGARDE-2":
                    self.show_game("save2.json")
                elif btn.text == "SAUVEGARDE-3":
                    self.show_game("save3.json")
                elif btn.text == "RETOUR":
                    self.show_start()

                elif btn.text == "Supprimer 1 ?":
                    delete_file("save1.json")
                elif btn.text == "Supprimer 2 ?":
                    delete_file("save2.json")
                elif btn.text == "Supprimer 3 ?":
                    delete_file("save3.json")
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




    def show_game(self, file):
        self.menu_music.stop(self.menu_music_player)
        self.window.show_view(GameView(save_file=file))
       
    

    def show_start(self):
        from sources.menu.menu_start.menu_start import MenuStart
        self.window.show_view(MenuStart())
