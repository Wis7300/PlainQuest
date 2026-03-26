from sources.entity import Item

IMG_POWERED_TIME_MACHINE = "sources/textures/item/time_machine/powered_time_machine.png"

class PoweredTimeMachine(Item):
    type = "machine a voyager dans le temps allumee"
    path_or_texture = IMG_POWERED_TIME_MACHINE
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, path_or_texture = self.path_or_texture)