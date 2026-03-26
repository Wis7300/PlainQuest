import arcade
import random
import json
import os
from sources.entity.entity import Entity

# Configuration des constantes
PNJ_HP = 20
PNJ_TEXTURES = [
    "sources/textures/pnj/img_man.png",
    "sources/textures/pnj/img_woman.png"
]

class Pnj(Entity):
    def __init__(self, x, y):
        """
        Load a random texture for the PNJ
        """
        texture_path = random.choice(PNJ_TEXTURES)
        super().__init__(
            x=x,
            y=y,
            path_or_texture=texture_path,
            hp=PNJ_HP
        )
        self.trade_config = self.load_random_trade()

        self.change_x = 0
        self.change_y = 0
        self.move_timer = 0

    def load_random_trade(self) -> dict:
        """Load the trades from the JSON file and return a random trade"""
        try:
            file_path = "sources/entity/pnj/trades.json" 

            with open(file_path, "r") as f:
                data = json.load(f)
                trades_list = data.get("possible_trades", [])
                
                if trades_list:
                    return random.choice(trades_list)
                
        except Exception as e:
            print(f"Erreur lors du chargement des trades : {e}")
        return {"required": "log", "qty_required": 5, "result": "stone_sword", "qty_result": 1}


    def update(self, delta_time):
        """Move the PNJ every 2sec"""
        self.move_timer += 1
        if self.move_timer > 120:  
            if random.random() < 0.3:  
                self.change_x = random.uniform(-1, 1)
                self.change_y = random.uniform(-1, 1)
            else:
                self.change_x = 0
                self.change_y = 0
            self.move_timer = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

    def trade(self, player_inventory):
        """
        Do the trade with the player
        """
        req_item = self.trade_config["required"]
        req_qty = self.trade_config["qty_required"]
        res_item = self.trade_config["result"]
        res_qty = self.trade_config["qty_result"]

        current_qty = player_inventory.get_quantity(req_item)

        if current_qty >= req_qty:
            # Echange
            try:
                player_inventory.remove_from_inventory(req_item, req_qty)
                player_inventory.add_to_inventory(res_item, res_qty)
                return f"Troc réussi ! +{res_qty} {res_item}"
            except ValueError as e:
                return f"Erreur : {e}"
            
    def reroll_trade(self):
        self.trade_config = self.load_random_trade()
