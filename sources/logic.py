import arcade
import math
import random

from sources.save.save import save_file, load_file, dict_to_sprite_list, sprite_list_to_dict
import sources.entity as entity
from sources.entity.item_cls.swords.fist import Fist
from sources.inventory.inventory import Inventory
from sources.map.map1.map1 import MapEngine
from sources.menu.menu_trade.menu_trade import MenuTrade
from sources.menu.menu_pause.menu_pause import MenuPause
from sources.menu.menu_gameover.menu_gameover import MenuGameover
from sources.menu.menu_craft.menu_craft import MenuCraft
from sources.menu.menu_inventory.menu_inventaire import InventoryMenu
from sources.menu.menu_end_screen.menu_end_screen import MenuEndScreen




# Taille des écrans / fenetre
MAP_HEIGHT = 4800
MAP_WIDTH = 4800

# Taille des diff mobs
PLAYER_SIZE = 50
ENEMY_SIZE = 45
ITEM_SIZE = 30
SWORD_SIZE = 120

# Vitesse des diff mobs
PLAYER_SPEED = 400
CAMERA_PAN_SPEED =0.2

# SFX
opening_menu_sound = arcade.load_sound("sources/sound+music/SFX/opening_menu.mp3")
wood_hit_sound = arcade.load_sound("sources/sound+music/SFX/wood_hit.mp3")
stone_hit_sound = arcade.load_sound("sources/sound+music/SFX/stone_hit.mp3")
hurt_sound = arcade.load_sound("sources/sound+music/SFX/hurt.mp3")





class GameView(arcade.View):
    def __init__(self, save_file = ""):
        
        self.save_file = save_file

        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        
        self.music_player = None
        self.music_menu = arcade.Sound("sources/sound+music/music/game_music.mp3")

        # Recupère les données stockées
        data = load_file(self.save_file)        

        # Inventaire
        self.inventory_cls = Inventory(save_file)
        self.inventory = self.inventory_cls.inventory
        

        # Player
        self.player_list = arcade.SpriteList(use_spatial_hash=False)
        self.player = entity.Player(x= data["player"]["player_x"],
                             y= data["player"]["player_y"],
                             name_or_precise_type = "JP")
        self.player.hp = data["player"].get("player_hp", self.player.hp)
        self.attack_direction = 1
        self.player_list.append(self.player)


            

        # Ennemis 
        self.current_number_enemy = 0
        try:
            if dict_to_sprite_list(data["enemy_list"]) != []:
                self.enemy_list = dict_to_sprite_list(data["enemy_list"])
        except:
            self.enemy_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemy_bullet_list = arcade.SpriteList(use_spatial_hash=True)
        self.number_max_enemy = 100


        # Items 
        try:
            if dict_to_sprite_list(data["item_list"]) != []:
                self.item_list = dict_to_sprite_list(data["item_list"])
        except:
            self.item_list = arcade.SpriteList(use_spatial_hash=True)

        
        
        
        
        # Caméra
        self.camera = arcade.camera.Camera2D()
        self.camera_x, self.camera_y = self.camera.position

        # Map
        self.seed = data.get("seed", random.randint(0, 1000000))
        self.map1 = MapEngine(gameview=self, seed=self.seed)
        self.map1.setup()
        self.player.map = self.map1
        
        

        if self.map1.can_attack:
            self.choose_best_sword()

        # Pnj
        self.pnj_list = arcade.SpriteList()
        self.create_pnj(2500, 2500, 1)
        

        # Débug Menu
        self.is_debug_menu_open = False
            
        # End Game
        self.has_end_screen_been_opened = False
        

        # Sauvegarde
        self.stuff_to_save = {
                            "player":{
                                "player_x":self.player.center_x,
                                "player_y": self.player.center_y,
                                "player_hp": self.player.hp
                                },
                            "inventory": self.inventory,
                            "seed":self.seed
                            # "enemy_list": sprite_list_to_dict(self.enemy_list),
                            # "item_list": sprite_list_to_dict(self.item_list)
                            }
        


    def on_draw(self):
        self.camera.use()
        self.clear()

        # la map actuelle ;(
        arcade.draw_lbwh_rectangle_filled(left=0,
                                          bottom=0,
                                          width=MAP_WIDTH,
                                          height=MAP_HEIGHT,
                                          color=arcade.color.BLUE_SAPPHIRE)
           
        
        # Ensuite la map
        self.map1.tile_list.draw()


        # Puis le joueur 
        self.player_list.draw()
        
        # Puis les éléments de la map
        self.map1.scene_list.sort(key=lambda x: x.center_y, reverse=True)
        self.map1.scene_list.draw(pixelated=True)

        # Le barre de vie du joueur 
        self.player.hp_bar_list.draw()

        # Puis les pnj
        self.pnj_list.draw()
        
        # Les items 
        self.item_list.draw()

        # Puis les ennemis
        self.enemy_list.draw()

        # Puis l'épée
        if self.map1.can_attack:    
            self.sword_list.draw()

        # Et enfin les balles
        self.enemy_bullet_list.draw()

        self.map1.draw_border()

        # Débug Menu 
        if self.is_debug_menu_open:
            arcade.draw_text(f"x: {self.player.center_x:.2f} y: {self.player.center_y:.2f} -- "
                            f"camera_x: {self.camera_x:.2f} camera_y: {self.camera_y:.2f} -- "
                            f"enemies: {len(self.enemy_list)} fps: {arcade.get_fps():.0f} -- "
                            f"hp: {self.player.hp}",
            self.camera_x - ((self.window.width - PLAYER_SIZE) // 2),
            self.camera_y + ((self.window.height - PLAYER_SIZE) // 2),
            arcade.color.WHITE,
            14)
            self.player.draw_hit_box()
            self.map1.hit_box_list.draw_hit_boxes() 
            self.sword_list.draw_hit_boxes()    



    def on_update(self, delta_time):


        # Caméra
        self.pan_camera_to_player(CAMERA_PAN_SPEED)
        self.camera_x, self.camera_y = self.camera.position

        
        # Check si le player ne peut pas pickup d'item
        self.pickup_item()

        # Mise à jour des données de sauvegarde 
        self.stuff_to_save = {
                            "player":{
                                "player_x":self.player.center_x,
                                "player_y": self.player.center_y,
                                "player_hp": self.player.hp
                                },
                            "inventory": self.inventory,
                            "seed":self.seed
                            # "enemy_list": sprite_list_to_dict(self.enemy_list),
                            # "item_list": sprite_list_to_dict(self.item_list)
                            }
        

        #                                           ---- Bullets ----

        
        for enemy in self.enemy_list:
            if enemy.__class__.__name__ == "Exploser":
                continue
            self.enemy_bullet_list.extend([b for b in enemy.bullet_list if b not in self.enemy_bullet_list])
        self.enemy_bullet_list.update()

        
        

        # Regarde si le joueur touche une bullet 
        for bullet in self.enemy_bullet_list:
            if arcade.check_for_collision_with_list(bullet, self.player_list):
                self.player.hp -= 1
                hurt_sound.play()
                bullet.remove_from_sprite_lists()

        if self.player.hp <= 0:
            self.open_gameover()    


        # Pnj
        self.pnj_list.update(delta_time)

        closest_pnj, dist = arcade.get_closest_sprite(self.player, self.pnj_list)
        if closest_pnj and dist < 100:
            if arcade.key.E in self.player.key_pressed:
                self.window.show_view(MenuTrade(self, closest_pnj))




        # Update de la map 
        self.map1.update(delta_time)

        
        self.sword_attack()
        
        
        

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            save_file(self.stuff_to_save, self.save_file)
            self.open_pause()
        elif symbol == arcade.key.A:
            opening_menu_sound.play()
            save_file(self.stuff_to_save, self.save_file)
            self.open_inventory()
        elif symbol == arcade.key.C:
            opening_menu_sound.play()
            self.open_craft()
        elif symbol == arcade.key.F3:
            self.is_debug_menu_open = not self.is_debug_menu_open
        elif symbol == arcade.key.K:
            self.player.hp = 0
        else:
            self.player.key_pressed.add(symbol)

        


    def on_key_release(self, symbol, modifiers):
        if symbol in self.player.key_pressed:
            self.player.key_pressed.remove(symbol)


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.map1.can_attack:
                world_x = x + self.camera_x - (self.window.width // 2)
                if  world_x < self.player.center_x:
                    self.attack_direction = -1 
                else:
                    self.attack_direction = 1
                for sword in self.sword_list:
                    if sword.attack_cooldown <=0:
                        sword.left_click()
                        sword.attack_cooldown = 0.5

    

    def on_show_view(self):
        self.music_player = self.music_menu.play(loop=True, volume=0.2)
        self.camera.position = self.player.position
        if len(self.enemy_list) < self.number_max_enemy:
            self.create_enemy(number_of_enemy = self.number_max_enemy - len(self.enemy_list))
        if self.map1.can_attack:
            self.choose_best_sword()

    def on_hide_view(self):
        self.player.key_pressed.clear()
        self.music_menu.stop(self.music_player)
        
        
    
    def on_fixed_update(self, delta_time):
        # Mise à jour régulière des animations
        self.enemy_list.update_animation(delta_time)
        self.enemy_list.update(delta_time)
        self.player_list.update(delta_time)

        if self.map1.can_attack:
            self.sword_list.update_animation(delta_time)

        # Déplacements des ennemis
        self.enemy_movement(delta_time=delta_time)

    def on_mouse_leave(self, x, y):
        self.player.key_pressed.clear()
        

        

# Fonction non présentes de base dans arcade
    def pan_camera_to_player(self, panning_fraction: float = 1.0):
        """Manage scrolling -- from Arcade docs"""
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player.position,
            self.window.delta_time,
            panning_fraction)
        

    # Items
    def get_item_class(self, name: str):
        for cls in entity.Item.__subclasses__():
            if cls.type == name:
                return cls
        return None


    def drop_item(self, x:int|float, y:int|float, item:str):
        """Create a item at the coordonates x,y and store it in the self.item_list"""
        item_class = self.get_item_class(item)
        if item_class == None:
            raise ValueError(f"Item inconnu : {item}")
        new_item = item_class(x=x, y=y, gameview=self)
        self.item_list.append(new_item)


    # Inventaire
    def pickup_item(self):
        """Add the items in collision with the player to the inventory"""
        for item in self.item_list:
            if arcade.get_distance_between_sprites(item, self.player) <= 100:
                self.inventory_cls.add_to_inventory(item.type)
                item.remove_from_sprite_lists()
                self.inventory_cls.choose_best_sword()



    # Differents menus
    def open_pause(self):
        self.window.show_view(MenuPause(self.save_file, gameview=self))

    def open_inventory(self):
        inventory_menu = InventoryMenu(file=self.save_file,
                                        inventory=self.inventory_cls,
                                        gameview=self)
        self.window.show_view(inventory_menu)

    def open_gameover(self):
        for item in self.inventory:
            for _ in range(item[1]):
                x_uncertainty = random.randint(-100, 100) 
                y_uncertainty = random.randint(-100, 100) 
                self.drop_item(x=self.player.center_x + x_uncertainty,
                            y = self.player.center_y + y_uncertainty,
                            item= item[0])
        
        self.window.show_view(MenuGameover(file=self.save_file, gameview=self))

    def open_craft(self):
        self.window.show_view(MenuCraft(gameview=self, file=self.save_file))

    def open_end_screen(self):
        if not self.has_end_screen_been_opened:
            self.window.show_view(MenuEndScreen(gameview=self))
            self.has_end_screen_been_opened = True


    # Ennemis
    def enemy_movement(self, delta_time:float) -> None:
        """Define the 3 modes of the enemy 

                - if the enemy can attack, it will
                - if the enemy can't attack but can detect the player, it will follow him
                - if the enemy can't detect the enemy, it will follow a random movement"""
        for enemy in self.enemy_list:
            # si l'enemi peut il va attaquer
            if math.dist((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y)) < enemy.attack_range:
                enemy.state = "ATTACK" # joue l'animation d'attaque 

            # si l'ennemy est trop loin pr attaquer il va s'approcher
            elif math.dist((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y)) < enemy.detection_range:
                enemy.state = "RUN" # joue l'animation de déplacement 
                angle = math.atan2((self.player.center_y - enemy.center_y),
                                    (self.player.center_x - enemy.center_x))
                old_x, old_y = enemy.center_x, enemy.center_y
                enemy.center_x += math.cos(angle) * enemy.speed * delta_time

                if arcade.check_for_collision_with_list(enemy, self.enemy_list) or arcade.check_for_collision_with_list(enemy, self.map1.hit_box_list):
                    enemy.center_x = old_x

                if math.cos(angle) * enemy.speed * delta_time > 0:
                    enemy.scale_x = 1
                else:
                    enemy.scale_x = -1

                enemy.center_y += math.sin(angle) * enemy.speed * delta_time
                if arcade.check_for_collision_with_list(enemy, self.enemy_list) or arcade.check_for_collision_with_list(enemy, self.map1.hit_box_list):
                    enemy.center_y = old_y

            # si l'ennemi ne detecte pas le joueur, mouvement de base du ennemi
            elif math.dist((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y)) < 1500:
                enemy.movement()

            # si l'ennemi est vrm trop loin, il ne se déplace pas
            else:
                pass
            

    def create_enemy(self, number_of_enemy:int = 100, area_of_spawn:tuple = ((-MAP_WIDTH, -MAP_HEIGHT), (MAP_WIDTH, MAP_HEIGHT))):
        """Create (number_of_enemy) enemy and add them to the self.enemy_list.
        do not put too many enemies in a limited space : the program could run endlessly"""
        if self.map1.can_enemy_spawn:
            enemy_classes = entity.Enemy.__subclasses__()
            x_min, y_min = area_of_spawn[0]
            x_max, y_max = area_of_spawn[1]
            for _ in range(number_of_enemy):
                x = random.randint(int(x_min), int(x_max))
                y = random.randint(int(y_min), int(y_max))
                enemy_class = random.choice(enemy_classes)
                enemy = enemy_class(x=x, y=y, player = self.player)
                self.enemy_list.append(enemy)

    def create_pnj(self, x, y, number_of_pnj):
        if self.map1.can_pnj_spawn:
            for i in range(number_of_pnj):
                pnj = entity.Pnj(x=x+ random.randint(-50, 50), y=y + random.randint(-50, 50))
                self.pnj_list.append(pnj)

    # Epées 
    def sword_attack(self) -> None:
        if self.map1.can_attack:
            for sword in self.sword_list:
                if self.attack_direction == 1:
                    sword.center_x = self.player.center_x + 40
                else:
                    sword.center_x = self.player.center_x - 40
                    sword.scale_x = -abs(sword.scale_x)  
                sword.center_y = self.player.center_y



                # Regarde les collsions entre l'épée et les ennemis et auquel cas leur enlève 1 hp
                if sword.is_attacking:
                    for enemy in arcade.check_for_collision_with_list(sword, self.enemy_list):
                        if enemy in self.enemy_list:
                            if not enemy in sword.already_attacked:
                                enemy.hp -= sword.damage
                                sword.already_attacked.add(enemy)
                                if enemy.hp <= 0:
                                    self.drop_item(x = enemy.center_x,
                                                y = enemy.center_y,
                                                item= enemy.drop_loot)
                                    

                    for elt in arcade.check_for_collision_with_list(sword, self.map1.hit_box_list):
                        if not elt in sword.already_attacked:
                            if elt.properties.get("type") == "tree":
                                wood_hit_sound.play()
                            elif elt.properties.get("type") == "rock":
                                stone_hit_sound.play()
                                print("ok")
                            elt.hp -= sword.damage
                            sword.already_attacked.add(elt)
                            if elt.hp <= 0:
                                self.drop_item(x = elt.center_x + random.randint(-100, 100),
                                               y = elt.center_y + random.randint(-100, 100),
                                               item= elt.drop_loot)
                                elt.hp = elt.max_hp
                                
    def choose_best_sword(self):
        self.sword_list = arcade.SpriteList(use_spatial_hash=False)

        best_sword = self.inventory_cls.choose_best_sword()
        sword = best_sword(x= self.player.center_x,
                        y = self.player.center_y, gameview=self)
        if sword.type == "poing epee":
            sword.scale = 0.4
        
        self.sword_list.append(sword)