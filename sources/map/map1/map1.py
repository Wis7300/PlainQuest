import arcade
import random
import os
import json

# --- Configuration ---
PATH_TO_TEXTURES = "textures/map/map1"
TILE_SIZE = 120
CHUNK_SIZE = 8       
VIEW_DISTANCE = 3    
WORLD_SEED = 12345 




tex_tiles = [arcade.load_texture(os.path.join(PATH_TO_TEXTURES, f"herbe_{i}.png")) for i in range(1, 5)]
tree_tex = arcade.load_texture(os.path.join(PATH_TO_TEXTURES, "arbre.png"))
rock_tex = arcade.load_texture(os.path.join(PATH_TO_TEXTURES, "rocher.png"))

# --- LIMITES DU MONDE ---
MAP_LIMIT_MIN = -5  
MAP_LIMIT_MAX = 5   
GRAPHICAL_MARGIN = 400

class MapEngine:
    def __init__(self, gameview=None , seed = None):
        self.player = gameview.player
        self.camera = gameview.camera
        self.gameview = gameview
        self.seed = seed if seed is not None else WORLD_SEED
        
        self.tile_list = arcade.SpriteList()
        self.scene_list = arcade.SpriteList() 
        self.hit_box_list = arcade.SpriteList()
        
        self.camera = None
        self.loaded_chunks = {} 
        self.map_memory = {}    # Garde les chunks en mémoire vive pendant la session
        self.show_hitboxes = False

        self.can_attack = True
        self.can_enemy_spawn = True
        self.can_pnj_spawn = True

    def setup(self):
        self.camera = arcade.camera.Camera2D()
        
        
        

    def generate_chunk(self, cx, cy):
        chunk_key = f"{cx},{cy}"
        
        # --- LOGIQUE DE LA SEED ---
        # On initialise le générateur aléatoire spécifiquement pour ce chunk
        # cx * 1000 + cy crée un identifiant unique pour chaque position
        random.seed(self.seed + (cx * 1000 + cy))
        
        if chunk_key not in self.map_memory:
            chunk_data = []
            for row in range(CHUNK_SIZE):
                for col in range(CHUNK_SIZE):
                    tx, ty = cx * CHUNK_SIZE + col, cy * CHUNK_SIZE + row
                    rand = random.random()
                    obj = "tree" if rand < 0.08 else ("rock" if rand < 0.12 else None)
                    chunk_data.append({"tx": tx, "ty": ty, "type": obj, "tex_idx": random.randint(0, 3)})
            self.map_memory[chunk_key] = chunk_data

        # Création des sprites (identique à avant)
        for item in self.map_memory[chunk_key]:
            tile = arcade.Sprite(tex_tiles[item['tex_idx']])
            tile.center_x, tile.center_y = item['tx'] * TILE_SIZE, item['ty'] * TILE_SIZE
            self.tile_list.append(tile)

            if item['type'] == "tree":
                tree = arcade.Sprite(tree_tex)
                tree.center_x = tile.center_x
                tree.bottom = tile.bottom + 5
                tree.properties["type"] = "tree"
                tree.hit_box_points = [] 
                self.scene_list.append(tree)

                hb = arcade.SpriteSolidColor(100, 40, arcade.color.WHITE)
                hb.center_x, hb.center_y = tree.center_x, tree.center_y - 100
                hb.alpha = 0 
                hb.properties["type"] = "tree"
                hb.hp, hb.max_hp = 5, 5
                hb.drop_loot = "buche"
                self.hit_box_list.append(hb)

            elif item['type'] == "rock" and item['tex_idx'] == 0:
                rock = arcade.Sprite(rock_tex, scale=2.0)
                rock.center_x, rock.center_y = tile.center_x, tile.center_y
                rock.properties["type"] = "rock"
                rock.hp, rock.max_hp = 10, 10
                rock.drop_loot = "pierre"
                self.scene_list.append(rock)
                self.hit_box_list.append(rock)
        
        # TRÈS IMPORTANT : On remet une seed aléatoire pour ne pas bloquer 
        # le reste du jeu (mouvements ennemis, drops, etc.) sur la même valeur
        random.seed()

    def update(self, delta_time):
        # Murs invisibles
        self.min_px = MAP_LIMIT_MIN * CHUNK_SIZE * TILE_SIZE
        self.max_px = -self.min_px

        self.player.center_x = max(self.min_px, min(self.player.center_x, self.max_px))
        self.player.center_y = max(self.min_px, min(self.player.center_y, self.max_px))

        # Transparence arbres
        for s in self.scene_list:
            if s.properties.get("type") == "tree":
                dist = arcade.get_distance_between_sprites(self.player, s)
                if (dist < 220 and self.player.center_y > s.center_y - 20) or dist < 100:
                    s.alpha = 140
                    self.player.alpha = 140
                else:
                    s.alpha = 255
                    self.player.alpha = 255

        # Chargement chunks dans les limites
        p_cx = int(self.player.center_x // (CHUNK_SIZE * TILE_SIZE))
        p_cy = int(self.player.center_y // (CHUNK_SIZE * TILE_SIZE))

        for y in range(p_cy - VIEW_DISTANCE, p_cy + VIEW_DISTANCE + 1):
            for x in range(p_cx - VIEW_DISTANCE, p_cx + VIEW_DISTANCE + 1):
                margin_chunks = int(GRAPHICAL_MARGIN / (CHUNK_SIZE * TILE_SIZE)) + 1

                if (MAP_LIMIT_MIN - margin_chunks <= x <= MAP_LIMIT_MAX + margin_chunks and
                MAP_LIMIT_MIN - margin_chunks <= y <= MAP_LIMIT_MAX + margin_chunks):
                    if (x, y) not in self.loaded_chunks:
                        self.loaded_chunks[(x, y)] = True
                        self.generate_chunk(x, y)

        self.camera.position = self.player.position

        

    def draw_border(self):
        border_color = (0, 0, 0, 120)  # noir semi-transparent

        # écran visible
        left = self.camera.position[0] - (self.gameview.window.width // 2 + 100)
        right = self.camera.position[0] + (self.gameview.window.width // 2 + 100)
        bottom = self.camera.position[1] - (self.gameview.window.height // 2 + 100)
        top = self.camera.position[1] + (self.gameview.window.height // 2 + 100)

        # zones hors map
        # gauche
        arcade.draw_lrbt_rectangle_filled(
            min(left, self.min_px),
            max(left, self.min_px),
            bottom,
            top,
            border_color
        )

        # droite
        arcade.draw_lrbt_rectangle_filled(
            min(self.max_px, right),
            max(self.max_px, right),
            bottom,
            top,
            border_color
        )

        # bas
        arcade.draw_lrbt_rectangle_filled(
            self.min_px,
            self.max_px,
            min(bottom, self.min_px),
            max(bottom, self.min_px),
            border_color
        )

        # haut
        arcade.draw_lrbt_rectangle_filled(
            self.min_px,
            self.max_px,
            min(self.max_px, top),
            max(self.max_px, top),
            border_color
        )
        
