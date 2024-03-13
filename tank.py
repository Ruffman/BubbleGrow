import pygame as pg



SIZE_CLASS = {
    "scout": [50, 100],
    "fighter": [60, 80],
    "freighter": [70, 70],
    "tank": [80, 60],
    "capital": [120, 50],
}


class Tank(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.surface = pg.display.get_surface()
        self.color = "white"
        self.size_class = "tank"
        self.size = SIZE_CLASS[self.size_class][0]
        self.speed = SIZE_CLASS[self.size_class][1]

        self.image = pg.image.load("art/tanks/bubble.png")
        self.rect = self.image.get_rect()


    def update(self) -> None:
        pass
        # self.rect.center = pg.mouse.get_pos()

    def move(self, x_axis, y_axis):
        self.rect.center += pg.Vector2(x_axis*self.speed, y_axis*self.speed)
