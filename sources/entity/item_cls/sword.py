import math
import arcade.hitbox as hitbox
from sources.entity import Item
from sources.textures.load_sheet import load_sheet

IMG_SWORD = "sources/textures/item/sword/stone sword.png"



class Sword(Item):
    type = "epee"
    path_or_texture = IMG_SWORD

    def __init__(self, x, y, texture=IMG_SWORD, damage: int = 0, gameview=None, **kwargs):
        self.gameview = gameview

        super().__init__(x, y, path_or_texture=self.path_or_texture)

        self.center_x = x
        self.center_y = y
        self.damage = damage
        
        self.attack_cooldown = 0

        self.attack_frames = texture


        self.is_attacking = False
        self.state = "IDLE"
        self.already_attacked = set()        

        self.frame_index = 0
        self.time_counter = 0
        self.attack_speed = 0.10  # ~6 FPS

        if self.type == "poing epee":
            self.new_hit_box = hitbox.HitBox(((-30, -30), (-30, 30), (30, 30), (30, -30)))
        else:
            self.new_hit_box = hitbox.HitBox(((-20, -20), (-20, 20), (20, 20), (20, -20)))
        self.hit_box = self.new_hit_box


    def left_click(self):
        self.is_attacking = True
        self.already_attacked.clear()
        self.frame_index = 0
        self.time_counter = 0
        self.state = "ATTACK"

    def update_animation(self, delta_time=1 / 60):

        if self.attack_cooldown >= 0:
            if self.type == 'epee stylée':
                self.attack_cooldown -= delta_time * 2
            else:
                self.attack_cooldown -= delta_time

        pivot_x = self.gameview.player.center_x
        pivot_y = self.gameview.player.center_y

        

        # position épée
        if self.gameview.attack_direction == 1:
            offset_x = 50
        else:
            offset_x = -50

        self.center_x = pivot_x + offset_x
        self.center_y = pivot_y

        # animation idle
        if not self.is_attacking:
            self.texture = self.attack_frames[0]
            return

        # Flip
        fixed_scale_x = self.scale_factor
        if self.gameview.attack_direction == -1:
            self.scale_x = - self.scale_y
        else:
            self.scale_x = self.scale_y

        

        # Animation
        self.time_counter += delta_time
        if self.time_counter >= self.attack_speed:
            self.time_counter = 0
            self.frame_index += 1

            if self.frame_index >= len(self.attack_frames):
                self.is_attacking = False
                self.frame_index = 0
                self.state = "IDLE"
                
                self.texture = self.attack_frames[0]
            else:
                frame = self.attack_frames[self.frame_index]
                self.texture = frame

        

        

        