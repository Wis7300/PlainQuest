from sources.entity import Item

IMG_STICK = "sources/textures/item/stick/stick.png"

class Stick(Item):
    type = "baton"
    path_or_texture = IMG_STICK
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)