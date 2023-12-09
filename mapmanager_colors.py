class Mapmanager():
    # Управление картой
    def __init__(self):
        self.model = 'block' # модель кубика лежит в файле block.egg
        # # используются следующие текстуры: 
        self.texture = 'block.png'          
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ] #rgba
        # создаём основной узел карты:
        self.startNew() 
        # self.addBlock((0,10, 0))

    def startNew(self):
        # создаёт основу для новой карты
        self.land = render.attachNewNode("Land") # узел, к которому привязаны все блоки карты

    def getColor(self, z):
        # если z меньше длины списка цветов
        if z < len(self.colors):
            # верни цвет под индексом z со списка цветов
            return self.colors[z]
        else:
            # иначе верни цвет с последним индексом со списка цветов
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        # создаём строительные блоки 
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture)) 
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)

    def clear(self):
        # убираем старый узел карты
        self.land.removeNode()
        # создаем новый узел карты
        self.startNew()

    def loadLand(self, filename):
        # создаёт карту земли из текстового файла
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x += 1
                y += 1


