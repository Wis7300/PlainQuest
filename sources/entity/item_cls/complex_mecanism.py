from entity import Item

IMG_COMPLEX_MECANISM = "textures/item/complex_mecanism/complex_mecanism.png"

class ComplexMecanism(Item):
    type = "mecanisme complexe"
    path_or_texture = IMG_COMPLEX_MECANISM
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
