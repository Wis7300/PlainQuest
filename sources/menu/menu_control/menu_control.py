import arcade

from sources.menu.button_sprite import ButtonSprite

click_sound = arcade.load_sound("sources/sound+music/SFX/menu_click.mp3")
MENU_IMAGE = "sources/textures/UI/menu_img.jpg"
path_to_img_control = "sources/textures/UI/control.png"
img_control = arcade.load_texture(path_to_img_control)

class MenuControl(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.WHITE

        self.text_list = []
        self.button_list = arcade.SpriteList()
        self.menu_list = arcade.SpriteList()

        # Sprite du menu
        self.menu_sprite = arcade.Sprite(MENU_IMAGE, scale=1.0)
        self.menu_sprite.center_x = self.window.width // 2
        self.menu_sprite.center_y = self.window.height // 2
        self.menu_list = arcade.SpriteList()
        self.menu_list.append(self.menu_sprite)


        movement_text = arcade.Text(text="Z,S,Q,D => Haut, Bas, Gauche, Droite",
                                    x = self.window.width // 2,
                                    y = self.window.height // 2 + 100,
                                    color = (0,0,0,200),
                                    font_size=20,
                                    width= self.window.width // 2,
                                    anchor_x= 'center',
                                    multiline=True)
        self.text_list.append(movement_text)
        
        inventory_text = arcade.Text(text="A => Ouverture inventaire \n" 
                                    "Dans l'inventaire : \n" 
                                    "- Clique droit : utilisation de l'objet (si possible) \n" 
                                    "- Clique gauche : drop de l'objet",
                                    x = self.window.width // 2,
                                    y = self.window.height // 2,
                                    color = (0,0,0,200),
                                    font_size=20,
                                    width= self.window.width // 2,
                                    multiline= True,
                                    anchor_x="center")
        self.text_list.append(inventory_text)
        
        craft_text = arcade.Text(text="C => Ouverture menu de craft \n" 
                                    "Dans le menu : \n" 
                                    "- Clique gauche sur un bouton : craft de l'objet",
                                    x = self.window.width // 2,
                                    y = self.window.height // 2 - 150,
                                    color = (0,0,0,200),
                                    font_size=20,
                                    multiline= True,
                                    width= self.window.width // 2,
                                    anchor_x="center")
        self.text_list.append(craft_text)
        
        interaction_text = arcade.Text(text="E => Ouverture menu d'échange (si suffisement proche) \n" 
                                    "Dans le menu : \n" 
                                    "- Clique gauche sur le bouton: action du bouton",
                                    x = self.window.width // 2,
                                    y = self.window.height // 2 - 300,
                                    color = (0,0,0,200),
                                    font_size=20,
                                    multiline= True,
                                    width= self.window.width // 2,
                                    anchor_x="center")
        self.text_list.append(interaction_text)

        attack_text = arcade.Text(text="Clique gauche : attaque du joueur : \n" 
                                    "- si clique à gauche du joueur : attaque à gauche \n" \
                                    "- si clique à droite du joueur : attaque à droite",
                                    x = self.window.width // 2,
                                    y = self.window.height // 2 - 450,
                                    color = (0,0,0,200),
                                    font_size=20,
                                    width= self.window.width // 2,
                                    multiline=True,
                                    anchor_x="center")
        self.text_list.append(attack_text)

        button_back = ButtonSprite(center_x=self.window.width // 2,
                                        center_y= self.window.height // 2 - 600,
                                        width = 300,
                                        height = 60,
                                        color = (255,255,255,200),
                                        text = "RETOUR")
        self.button_width = button_back.width
        self.button_height = button_back.height
        self.button_list.append(button_back)
        self.text_list.append(button_back.label)

        self.img_control_rect = arcade.LBWH(left=self.window.width // 2 - (img_control.width // 2),
                                    bottom=self.window.height // 2 - (img_control.height // 2) + 200,
                                    height=img_control.height,
                                    width=img_control.width)

        # Camera
        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y
        self.camera_y = self.camera.position[1]
        self.max_y = self.camera_y
        self.min_y = (self.camera_y * 1.5) - (len(self.text_list) * 100) + 50

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.menu_list.draw()
        arcade.draw_texture_rect(texture=img_control,
                                     rect=self.img_control_rect)
        self.button_list.draw()
        for text in self.text_list:
            text.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        x = x + self.camera.position[0] - self.window.width / 2
        y = y + self.camera.position[1] - self.window.height / 2
        for btn in self.button_list:
            condition = (btn.center_x - btn.base_width / 2 <= x <= btn.center_x + btn.base_width / 2 and 
            btn.center_y - btn.base_height / 2 <= y <= btn.center_y + btn.base_height / 2)
            
            if condition:
            
                btn.width = btn.base_width + 10
                btn.height = btn.base_height + 10
            else:
                
                btn.width = self.button_width
                btn.height = self.button_height

    def on_mouse_press(self, x, y, button, modifiers):
        x = x + self.camera.position[0] - self.window.width / 2
        y = y + self.camera.position[1] - self.window.height / 2
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.button_list:
                if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and
                    btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                    if btn.text == "RETOUR":
                        from sources.menu.menu_start.menu_start import MenuStart
                        self.window.show_view(MenuStart())
                    click_sound.play()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0 and self.camera_y >= self.min_y:
            self.camera_y -= 20
        elif scroll_y > 0 and self.camera_y <= self.max_y:
            self.camera_y += 20

    def on_update(self, delta_time):
        self.camera.position = self.window.center_x, self.camera_y