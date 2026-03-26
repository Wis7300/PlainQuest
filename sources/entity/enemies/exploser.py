import random
import math
import arcade

from sources.entity.enemy import Enemy
from sources.textures.load_sheet import load_sheet



TEXTURES = {
    "idle": "sources/textures/enemy/exploser/exploser_idle.png",      
    "run": "sources/textures/enemy/exploser/exploser_run.png",
    "attack": "sources/textures/enemy/exploser/exploser_attack.png"
}

idle_textures = load_sheet(TEXTURES["idle"], 6)
run_textures = load_sheet(TEXTURES["run"], 6)
attack_textures = load_sheet(TEXTURES["attack"], 4)

explosion_sound = arcade.load_sound("sources/sound+music/SFX/explosion.mp3")

class Exploser(Enemy):
    def __init__(self, x, y, player, **kwargs):
        super().__init__(x = x, y = y, path_or_texture=idle_textures[0])
        self.center_x = x
        self.center_y = y
        self.player = player

        self.hp = 5
        self.speed = 300

        self.attack_range = 50
        self.detection_range = 200
        self.drop_loot = random.choice(["roue dentee", "poudre electrique"])

        self.time_counter = 0
        self.frame_index = 0
        self.state = "IDLE"
        self.target_timer = 0
        self.number_of_attacks = 0

        
        if idle_textures:
            self.texture = idle_textures[0]

    def update_animation(self, delta_time = 1 / 60, *args, **kwargs):
        if self.state == "ATTACK":
            frames = attack_textures
            speed = 0.10
        elif self.state == "RUN":
            frames = run_textures
            speed = 0.12
        else:
            frames = run_textures
            speed = 0.18

        self.time_counter += delta_time
        if self.time_counter >= speed:
            self.time_counter = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.texture = frames[self.frame_index]

            if self.state == "ATTACK" and self.frame_index == 3:
                if self.number_of_attacks < 3:
                    self.number_of_attacks += 1
                elif self.number_of_attacks == 3:
                    explosion_sound.play()
                    self.explode()       

        if self.change_x < 0:
            self.scale_x = -1
        elif self.change_x > 0:
            self.scale_x = 1

    def explode(self):
        self.player.hp -= 20
        self.hp = -1

    def update(self, delta_time = 1 / 60, *args, **kwargs):
        self.update_animation(delta_time)
        if self.hp <= 0:
            self.kill()

    def movement(self, delta_time = 1 / 60):
        if self.state != "ATTACK":
            if self.target_timer <= 0:
                if random.random() < 0.4: 
                    self.state = "IDLE"
                    self.change_x = 0
                    self.change_y = 0
                    self.target_timer = random.uniform(2.0, 4.0)
                else:
                    self.state = "RUN"
                    angle = random.uniform(0, 2 * math.pi)
                    self.change_x = math.cos(angle) * (self.speed / 2) * delta_time
                    self.change_y = math.sin(angle) * (self.speed  / 2) * delta_time
                    self.target_timer = random.uniform(1.0, 3.0)

            self.target_timer -= delta_time

        self.center_x += self.change_x 
        self.center_y += self.change_y

