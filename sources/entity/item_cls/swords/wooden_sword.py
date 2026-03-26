from sources.entity.item_cls.sword import Sword
from sources.entity.item import Item
from sources.textures.load_sheet import load_sheet

IMG_SWORD = "sources/textures/item/sword/wooden sword.png"

texture = load_sheet(IMG_SWORD, 6)

class WoodenSword(Sword, Item):
    damage = 3
    scale_factor = 2
    type = "epee en bois"
    path_or_texture = texture
    def __init__(self, x, y, gameview):
        super().__init__(x, y, texture = self.path_or_texture, damage=self.damage, gameview=gameview)
        
        

