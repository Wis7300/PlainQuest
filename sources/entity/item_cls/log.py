from entity import Item

IMG_LOG = "textures/item/log/log.png"

class Log(Item):
    type = "buche"
    path_or_texture = IMG_LOG

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
