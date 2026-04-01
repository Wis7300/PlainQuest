import arcade



texture_to_title = "textures/UI/plain_quest.png"
texture_to_arcade = "textures/UI/fait_avec_arcade.png"

class MenuIntro(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = (10, 15, 30)
        self.end_background_color = (122, 103, 245)

        self.time = 0
        self.alpha = 0


        # Image du titre
        self.img1 = arcade.load_texture(texture_to_title)
        self.img1_rect = arcade.LBWH(left=self.window.width // 2 - (self.img1.width // 2),
                                    bottom=self.window.height // 2 - 50,
                                    height=self.img1.height,
                                    width=self.img1.width)

        # Image Arcade
        self.img2 = arcade.load_texture(texture_to_arcade)
        self.img2_rect = arcade.LBWH(left=self.window.width // 2 - (self.img2.width // 2),
                                    bottom=self.window.height // 2 - 50,
                                    height=self.img2.height,
                                    width=self.img2.width)
        
        

    def on_update(self, delta_time):
        self.time += 2

        # Première image (titre)
        if self.time < 250:
            self.alpha = min(self.alpha + 2, 255)
        elif self.time >= 350 and self.time < 600:
            self.alpha = max(self.alpha -2, 0)

         # text2 est affiché
        elif self.time >= 700 and self.time < 950:
            self.alpha = min(self.alpha + 2, 255)
        elif self.time >= 1050 and self.time < 1300:
            self.alpha = max(self.alpha -1, 0)
        
        if self.time >= 1500:
            self.open_start()
        
    def on_draw(self):
        self.clear()
        arcade.draw_lrbt_rectangle_filled(0, self.window.width, 0, self.window.height,
        (0, 0, 0, self.alpha))
        if self.time <= 700:
            arcade.draw_texture_rect(texture=self.img1,
                                     rect=self.img1_rect, 
                                     alpha = self.alpha)
        elif self.time < 1400 and self.time > 700:
            arcade.draw_texture_rect(texture=self.img2,
                                     rect=self.img2_rect, 
                                     alpha = self.alpha)


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.open_start()


    def open_start(self):
        from menu.menu_start.menu_start import MenuStart
        self.window.show_view(MenuStart())
        
