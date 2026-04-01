from entity.item import Item

IMG_ELECTRIC_POWDER = "textures/item/electric_powder/electric_powder.png"

class ElectricPowder(Item):
    type = "poudre electrique"
    path_or_texture = IMG_ELECTRIC_POWDER
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
