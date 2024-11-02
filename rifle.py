from gun import Gun


class Rifle(Gun):

    def __init__(self):
        super().__init__('Rifle', 10, 10, 20)