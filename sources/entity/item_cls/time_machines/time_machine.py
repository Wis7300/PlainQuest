import arcade
from entity import Item

IMG_TIME_MACHINE = "textures/item/time_machine/time_machine.png"

class TimeMachine(Item):
    type = "machine a voyager dans le temps" 
    path_or_texture = IMG_TIME_MACHINE
    def __init__(self, x, y, gameview=None, **kwargs):
        self.gameview = gameview

        super().__init__(x, y, path_or_texture = self.path_or_texture)
        
