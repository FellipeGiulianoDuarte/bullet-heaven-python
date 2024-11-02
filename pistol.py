from gun import Gun


class Pistol(Gun):

    def __init__(self):
        super().__init__('Pistol', 15, 1.5, 15)