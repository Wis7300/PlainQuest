from entity import Item

IMG_PLANK = "textures/item/plank/plank.png"

class Plank(Item):
    type = "planche"
    path_or_texture = IMG_PLANK
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
