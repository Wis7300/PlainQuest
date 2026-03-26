from sources.entity.item_cls.sword import Sword
from sources.entity.item import Item
from sources.textures.load_sheet import load_sheet


IMG_COIN = "sources/textures/item/sword/fist.png"

texture = load_sheet(IMG_COIN, 6)

class Fist(Sword, Item):
    type = "poing epee"
    damage = 1
    scale_factor = 1
    path_or_texture = texture
    def __init__(self, x, y, gameview):
        super().__init__(x, y, gameview=gameview, texture = self.path_or_texture, damage=self.damage, scale=self.scale_factor)
    