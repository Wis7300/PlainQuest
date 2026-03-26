from sources.entity.item_cls.sword import Sword
from sources.entity.item import Item
from sources.textures.load_sheet import load_sheet

IMG_SWORD = "sources/textures/item/sword/styled sword.png"

sword_texture = load_sheet(IMG_SWORD, 6)

class StyledSword(Sword, Item):
    damage = 10
    scale_factor = 2
    type = 'epee stylee'
    path_or_texture = sword_texture
    def __init__(self, x, y, gameview):
        super().__init__(x, y, texture = self.path_or_texture, damage=self.damage, gameview=gameview)
        
