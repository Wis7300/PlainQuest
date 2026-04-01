from entity import Item

IMG_COIN = "textures/item/iron_ingot/iron_ingot.png"

class IronIngot(Item):
    type = "lingot de fer"
    path_or_texture = IMG_COIN
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
