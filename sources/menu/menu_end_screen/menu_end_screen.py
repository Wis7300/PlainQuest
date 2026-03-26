import arcade

from sources.menu.menu_intro.menu_intro import MenuIntro


class MenuEndScreen(arcade.View):
    def __init__(self, gameview):
        self.gameview = gameview
        super().__init__()

        self.background_color = arcade.color.BLACK

        self.text_list = []
        self.congrats_text = arcade.Text(text="Bien joué ! Tu as réussi à remonter le temps et donc à \n " \
                                                "empêcher le monde de finir en ruine comme tu l'as aperçu ! ",
                                        x = self.window.width // 2,
                                        y = self.window.height // 2 + 100,
                                        color = arcade.color.WHITE,
                                        font_size=20,
                                        anchor_x="center",
                                        anchor_y="center",
                                        multiline = True,
                                        width = self.window.width // 2)
        self.text_list.append(self.congrats_text)

        self.thanks_text = arcade.Text(text="Merci d'avoir joué à ce jeu ! " \
                                        "                                   " \
                                        "Appuyez sur Entrée pour continuer ou " \
                                        "sur Échap pour revenir au menu principal.",
                                        x = self.window.width // 2,
                                        y = self.window.height // 2 - 100,
                                        color = arcade.color.WHITE,
                                        font_size=20,
                                        multiline=True,
                                        width=self.window.width // 2,
                                        anchor_x="center",
                                        anchor_y="center")
        self.text_list.append(self.thanks_text)

        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y

    def on_draw(self):
        self.clear()
        self.camera.use()
        for text in self.text_list:
            text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(MenuIntro())

        if symbol in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.NUM_ENTER):
            self.window.show_view(self.gameview)