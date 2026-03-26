import arcade
import random

from sources.entity.entity import Entity
from sources.textures.load_sheet import load_sheet
from sources.map.map1.map1 import MapEngine

MAP_WIDTH = 5000
MAP_HEIGHT = 5000

TEXTURES = {
    "idle": "sources/textures/player/player_idle.png",
    "run": "sources/textures/player/player_run.png"
}

idle_textures = load_sheet(TEXTURES["idle"], 1)
run_textures = load_sheet(TEXTURES["run"], 6)


class Player(Entity):

    PLAYER_SPEED = 400
    PLAYER_HP = 100

    def __init__(self, x: int | float, y: int | float,
                 name_or_precise_type=None,
                 path_or_texture=None):

        self.speed = self.PLAYER_SPEED
        self.hp = self.PLAYER_HP
        self.max_hp = self.PLAYER_HP

        
        self.hp_bar_list = arcade.SpriteList()
        
        self.key_pressed = set()

        self.time_counter = 0
        self.frame_index = 0
        self.state = "IDLE"

        super().__init__(
            x, y,
            name_or_precise_type=name_or_precise_type,
            path_or_texture=idle_textures[0] if idle_textures else None,
            speed=self.speed,
            hp=self.hp
        )

        self.center_x = x
        self.center_y = y

        if idle_textures:
            self.texture = idle_textures[0]

        self.hp_bar_border = arcade.SpriteSolidColor(width=104, height=14, color=arcade.color.BLACK, center_x=self.center_x, center_y = self.center_y + 50)
        self.hp_bar_list.append(self.hp_bar_border)

        self.hp_bar_interior = arcade.SpriteSolidColor(width=int((self.hp / self.max_hp) * 100), height=10, color=arcade.color.RED, center_x=self.center_x, center_y = self.center_y + 50)
        self.hp_bar_list.append(self.hp_bar_interior)


    def update_animation(self, delta_time=1 / 60):

        # Déterminer l'état selon le mouvement
        if self.change_x != 0 or self.change_y != 0:
            self.state = "RUN"
        else:
            self.state = "IDLE"

        # Choix des frames selon l'état
        if self.state == "RUN":
            frames = run_textures
            speed = 0.10
        else:
            frames = idle_textures
            speed = 0.2

        if not frames:
            return

        self.time_counter += delta_time
        if self.time_counter >= speed:
            self.time_counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.texture = frames[self.frame_index]

        # Flip horizontal
        if self.change_x < 0:
            self.scale_x = -1
        elif self.change_x > 0:
            self.scale_x = 1



    def update(self, delta_time=1/60):
        self.update_animation(delta_time)
        self.move(delta_time)

        # Mettre à jour la barre de vie
        self.hp_bar_border.center_x, self.hp_bar_border.center_y = self.center_x, self.center_y + 50
        self.hp_bar_interior.center_x, self.hp_bar_interior.center_y = self.center_x, self.center_y + 50
        self.hp_bar_interior.width = int((self.hp / self.max_hp) * 100)


    


    def move(self, delta_time=1/60):
        """Set the change_x and change_y with the values presents in the self.key_press set"""
        self.change_x = 0
        self.change_y = 0

        if arcade.key.Z in self.key_pressed:
            self.change_y += self.speed * delta_time
        if arcade.key.S in self.key_pressed:
            self.change_y -= self.speed * delta_time
        if arcade.key.D in self.key_pressed:
            self.change_x += self.speed * delta_time
        if arcade.key.Q in self.key_pressed:
            self.change_x -= self.speed * delta_time


        # --- mouvement X ---
        old_x = self.center_x
        self.center_x += self.change_x
        if arcade.check_for_collision_with_list(self, self.map.hit_box_list):
            self.center_x = old_x


        # --- mouvement Y ---
        old_y = self.center_y
        self.center_y += self.change_y
        if arcade.check_for_collision_with_list(self, self.map.hit_box_list):
            self.center_y = old_y