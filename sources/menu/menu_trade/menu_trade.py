import arcade

from sources.menu.button_sprite import ButtonSprite
from sources.entity.pnj.pnj import Pnj
from sources.inventory.inventory import get_item_class

path_to_trade_texture = "sources/textures/UI/trade.png"
img_trade = arcade.load_texture(path_to_trade_texture)

class MenuTrade(arcade.View):
    def __init__(self, gameview, pnj: Pnj):
        super().__init__()
        self.gameview = gameview
        self.pnj = pnj
        self.inventory_cls = self.gameview.inventory_cls
        self.trade = self.pnj.trade_config
        
        self.background_color = arcade.color.DARK_SLATE_BLUE
        self.button_list = arcade.SpriteList()
        self.display_sprites = arcade.SpriteList() 
        self.text_list = []
        self.label_list = []

        self.button_width = 200
        self.button_height = 50

        # Image 
        self.img_trade_rect = arcade.LBWH(left=self.window.width // 2 - (img_trade.width // 2),
                                    bottom=self.window.height // 2 - (img_trade.height // 2) + 200,
                                    height=img_trade.height,
                                    width=img_trade.width)

        # Boutons 
        # Trade
        self.trade_button = ButtonSprite(
            center_x=self.window.width // 2,
            center_y=self.window.height // 2 - 100, 
            width=self.button_width,
            height=self.button_height,
            color=(255, 255, 255, 200),
            text="Echange")
        self.button_list.append(self.trade_button)
        self.text_label_trade_button = self.trade_button.label
        self.text_list.append(self.text_label_trade_button)

        # Reroll
        self.reroll_button = ButtonSprite(
            center_x = self.window.width // 2,
            center_y = self.trade_button.center_y - 100,
            width = self.button_width,
            height = self.button_height,
            color = (255, 255, 255, 200),
            text= "Changer l'échange")
        self.button_list.append(self.reroll_button)
        self.text_label_reroll_button = self.reroll_button.label
        self.text_list.append(self.text_label_reroll_button)


       
        # Textes
        self.text_required = arcade.Text(f"x{self.trade['qty_required']}", 
                         self.window.width // 2 - 150, self.window.height // 2 - 100,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        self.text_list.append(self.text_required)

        self.text_result = arcade.Text(f"x{self.trade['qty_result']}", 
                         self.window.width // 2 + 150, self.window.height // 2 - 100,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        self.text_list.append(self.text_result)

        # Nom d'items
        self.is_label_shown = False
        self.label_required = arcade.Text(text=self.trade["required"],
                                                 x = self.window.width // 2 - 250,
                                                 y = self.window.height // 2,
                                                 color = (255, 255, 255 ,200), font_size=20, anchor_x="center")
        self.label_list.append(self.label_required)
        
        self.label_result = arcade.Text(text=self.trade["result"],
                                                 x = self.window.width // 2 + 250,
                                                 y = self.window.height // 2,
                                                 color = (255, 255, 255, 200), font_size=20, anchor_x="center")
        self.label_list.append(self.label_result)
    

        self.setup_trade_icons()

        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.center_x, self.window.center_y

    

    def on_draw(self):
        self.clear()
        self.camera.use()
        
        # Image
        arcade.draw_texture_rect(texture=img_trade,
                                     rect=self.img_trade_rect)
        # Bouton
        self.button_list.draw()
        
        # Textures
        self.display_sprites.draw()

        # Textes
        for text in self.text_list:
            text.draw()

        # Labels
        if self.is_label_shown:
            for label in self.label_list:
                label.draw()
        

        

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_label_shown = False
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and 
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                btn.width = btn.base_width + 10
                btn.height = btn.base_height + 10
                
                if btn.text == "Echange":
                    self.is_label_shown = True
                    self.choose_color(btn)
            else:
                btn.width = self.button_width
                btn.height = self.button_height
                btn.color = (255, 255, 255, 200)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.button_list:
            if (btn.center_x - btn.width / 2 <= x <= btn.center_x + btn.width / 2 and
                btn.center_y - btn.height / 2 <= y <= btn.center_y + btn.height / 2):
                if btn.text == "Echange":
                    if self.inventory_cls.get_quantity(self.trade["required"]) >= self.trade["qty_required"]:  
                        self.pnj.trade(self.inventory_cls)
                        self.choose_color(btn)
                elif btn.text == "Changer l'échange":
                    self.pnj.reroll_trade()
                    self.reinitialize()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE or key == arcade.key.E:
            self.window.show_view(self.gameview)


    # Fonctions non présentes dans arcade

    def setup_trade_icons(self):
        """Get the textures of the required and result items and create sprites for them"""
         
        # Items requis 
        req_cls = get_item_class(self.trade["required"])
        if req_cls:
            tex = req_cls.path_or_texture
            if isinstance(tex, list): tex = tex[0]
            
            req_sprite = arcade.Sprite(tex, scale=1.5)
            req_sprite.center_x = self.window.width // 2 - 250
            req_sprite.center_y = self.window.height // 2 - 100
            self.display_sprites.append(req_sprite)

        # Items résultats
        res_cls = get_item_class(self.trade["result"])
        if res_cls:
            tex = res_cls.path_or_texture
            if isinstance(tex, list): tex = tex[0]
            
            res_sprite = arcade.Sprite(tex, scale=1.5)
            res_sprite.center_x = self.window.width // 2 + 250
            res_sprite.center_y = self.window.height // 2 - 100
            self.display_sprites.append(res_sprite)

    def reinitialize(self):
        self.trade = self.pnj.trade_config
        self.text_required.text = f"x{self.trade['qty_required']}"
        self.text_result.text = f"x{self.trade['qty_result']}"
        self.label_required.text = f"{self.trade['required']}"
        self.label_result.text = f"{self.trade['result']}"
        self.display_sprites.clear()
        self.setup_trade_icons()
        

    def choose_color(self, btn):
        if self.inventory_cls.get_quantity(self.trade["required"]) >= self.trade["qty_required"]:
            btn.color = (50, 200, 50, 200)
        else:
            btn.color = (200, 50, 50, 200)