from sources.entity.item import Item

RED_POTION_IMG = "sources/textures/item/potion/red_potion.png"
PINK_POTION_IMG = "sources/textures/item/potion/pink_potion.png"

class Potion(Item):
    type = 'potion'
    def init(self, x, y,
            hp_healed, 
            gameview = None,
            scale=1,
            **kwargs):
        super().__init__(x=x, y=y, character_scale=scale, **kwargs)
        self.center_x = x
        self.center_y = y 
        self.hp_healed = hp_healed
        self.gameview = gameview
        

    def right_click(self):
        self.gameview.player.hp = min(self.gameview.player.max_hp, self.gameview.player.hp + self.hp_healed)


class RedPotion(Potion, Item):
    type = "potion rouge"
    path_or_texture = RED_POTION_IMG
    def __init__(self, x, y, gameview):
        self.hp_healed = 50
        self.gameview = gameview
        super().__init__(x=x, y=y, hp_healed=self.hp_healed, gameview = gameview, path_or_texture= self.path_or_texture)

class PinkPotion(Potion, Item):
    type = "potion rose"
    path_or_texture = PINK_POTION_IMG
    def __init__(self, x, y, gameview):
        self.gameview = gameview
        self.hp_healed = 30
        super().__init__(x=x, y=y, hp_healed=self.hp_healed, gameview = gameview, path_or_texture=self.path_or_texture)