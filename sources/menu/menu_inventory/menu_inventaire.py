import arcade
import random

from entity.item_cls import *
from entity.item import Item
from menu.menu_end_screen.menu_end_screen import MenuEndScreen


OBJECT_SIZE = 60

texture_to_title = "textures/UI/inventory.png"

class Case(arcade.Sprite):
    def __init__(self, center_x, center_y, width, height, color):
        texture = arcade.make_soft_square_texture(width, color, outer_alpha=color[3])
        super().__init__(texture, scale=1.0)
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

class InventoryMenu(arcade.View):
    def __init__(self, file, inventory, gameview):
        super().__init__()
        self.file = file


        self.camera = arcade.camera.Camera2D()
        self.camera.position = self.window.width // 2, self.window.height // 2

        self.inventory = inventory
        self.gameview = gameview

        
        case_width = 80
        case_height = 80
        self.case_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.text_list = []
        self.name_list = []

        
        # Image inventaire
        self.img_inventory = arcade.load_texture(texture_to_title)
        self.img_inventory_rect = arcade.LBWH(left=self.window.width // 2 - (self.img_inventory.width // 2),
                                    bottom=self.window.height // 2 - (self.img_inventory.height // 2) + 100,
                                    height=self.img_inventory.height,
                                    width=self.img_inventory.width)
        
        # Texte time machine
        self.is_text_time_machine_open = False
        self.text_time_machine = arcade.Text("La machine n'est pas allumée...",
                                x = self.gameview.window.width // 2,
                                y = self.gameview.window.height // 2,
                                font_size=20,
                                anchor_x="center",
                                anchor_y="center",
                                color = (255, 0, 255, 200))
        self.text_time_machine_timer = 2


        

        # Dessin basique des cases d'inventaire
        self.x_start = self.window.width // 4 - 100
        for i in range(0,10):
            for j in range(2,4):
                x_case = i * 100 + self.x_start
                y_case = j * 100 

                case = Case(center_x=x_case, center_y=y_case, width=case_width, height=case_height, color= (100, 100, 100, 125))
                self.case_list.append(case)
        
        self.place_item()

    def on_draw(self):
        self.camera.use()
        self.clear()
        self.case_list.draw()
        self.item_list.draw()
        arcade.draw_texture_rect(texture=self.img_inventory,
                                     rect=self.img_inventory_rect)
        for text in self.text_list:
            text.draw()
        for name in self.name_list:
            name.draw()

        if self.is_text_time_machine_open and self.text_time_machine_timer > 0:
            self.text_time_machine.draw()


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.A:
            self.back_to_game()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for item in self.item_list:
                if (item.center_x - item.width / 2 <= x <= item.center_x + item.width / 2 and
                    item.center_y - item.height / 2 <= y <= item.center_y + item.height / 2):
                    self.drop_item(item.name)


                    self.item_list.clear()
                    self.text_list = []
                    self.place_item()
                    break
        if button == arcade.MOUSE_BUTTON_RIGHT:
            for item in self.item_list:
                if (item.center_x - item.width / 2 <= x <= item.center_x + item.width / 2 and
                    item.center_y - item.height / 2 <= y <= item.center_y + item.height / 2):
                    
                    item_class = self.get_item_class(item.name)
                    
                    if item_class:
                        temp_instance = item_class(x=0, y=0, gameview=self.gameview)
                        if item.name == "time machine":
                            self.is_text_time_machine_open = not self.is_text_time_machine_open
                            self.text_time_machine_timer = 2
                        
                        # Fin du jeu
                        elif item.name == "powered time machine":
                            self.window.show_view(MenuEndScreen(self.gameview))

                        if hasattr(temp_instance, "right_click"):
                            temp_instance.right_click()
                            self.inventory.remove_from_inventory(item.name)
                                
                                
                        
                        self.item_list.clear()
                        self.text_list = []
                        self.place_item()
                        break
                    

        


    def on_mouse_motion(self, x, y, dx, dy):
        self.name_list.clear()
        for item in self.item_list:
            if (item.center_x - 50 <= x <= item.center_x + 50 and
                    item.center_y - 50 <= y <= item.center_y + 50):
                text = arcade.Text(x = item.center_x,
                                       y = item.center_y + 50,
                                       color=arcade.color.BLACK,
                                       text=item.name,
                                       font_size=14)
                self.name_list.append(text)

    def on_update(self, delta_time):
        if self.text_time_machine_timer > 0:
            self.text_time_machine_timer -= delta_time
                
    
    
        
                    
                    

    


    # Fonctions non présentes de base dans arcade

    def get_item_class(self, name: str):
        for cls in Item.__subclasses__():
            if cls.type == name:
                return cls
        return None
    
    def place_item(self):
        
        for index, (item_name, number) in enumerate(self.inventory.inventory):
            item_class = self.get_item_class(item_name)
            i = index % 10
            j = index // 10 + 2 
            x = i * 100 + self.x_start
            y = j * 100 

            if item_class:
                if type(item_class.path_or_texture) == list:
                    item = arcade.Sprite(path_or_texture=item_class.path_or_texture[0])
                else:
                    item = arcade.Sprite(path_or_texture=item_class.path_or_texture)
                

                if item.width > OBJECT_SIZE:
                    item.width = OBJECT_SIZE
                if item.height > OBJECT_SIZE:
                    item.height = OBJECT_SIZE

                item.center_x = x + 13 if "epee" in item_name else x
                item.center_y = y - 15 if "epee" in item_name else y
                item.name = item_name
                self.item_list.append(item)

            
            quantity = arcade.Text(f"{number}", x= x-30 ,y= y-30, color=arcade.color.WHITE, font_size=14)
            self.text_list.append(quantity)

    
    def drop_item(self, item:str):
        """Create a item at the coordonates x,y and store it in the self.item_list"""
        item_class = self.get_item_class(item)
        if item_class == None:
            raise ValueError(f"Item inconnu : {item}")
        self.inventory.remove_from_inventory(item)
        x = random.randint(-100, 100) + self.gameview.player.center_x
        y = random.randint(-100, 100) + self.gameview.player.center_y
        new_item = item_class(x=x, y=y, gameview = self.gameview)
        self.gameview.item_list.append(new_item)
        


    def back_to_game(self):
        self.window.show_view(self.gameview)

