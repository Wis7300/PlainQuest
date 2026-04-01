from entity.item import Item


IMG_PRINTED_CIRCUIT = "textures/item/printed_circuit/printed_circuit.png"

class Printed_circuit(Item):
    type = "circuit imprime"
    path_or_texture = IMG_PRINTED_CIRCUIT
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)
