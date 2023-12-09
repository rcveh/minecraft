from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        # Метод который отвечает за загрузку карты с файла
        x, y = self.land.loadLand("land.txt")
        # создаем игрока с позицией на карте
        self.hero = Hero((x//2, y//2, 2), self.land)
        # устанавливаем угол обзора 90 градусов
        self.camLens.setFov(90)

game = Game()
game.run()