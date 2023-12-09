# напиши свой код здесь

key_switch_camera = 'c' # камера привязана к герою или нет
key_switch_mode = 'z' # можно проходить сквозь препятствия или нет

key_forward = 'w'   # шаг вперёд (куда смотрит камера)
key_back = 's'      # шаг назад
key_left = 'a'      # шаг влево (вбок от камеры)
key_right = 'd'     # шаг вправо
key_up = 'e'      # шаг вверх
key_down = 'q'     # шаг вниз

key_turn_left = 'n'     # поворот камеры направо (а мира - налево)
key_turn_right = 'm'    # поворот камеры налево (а мира - направо)

key_build = 'b'     # построить блок перед собой
key_destroy = 'v'   # разрушить блок перед собой

key_savemap = 'k'
key_loadmap = 'l'

class Hero():
    def __init__(self, pos, land):
        # создаем свойство land
        self.land = land
        self.mode = True # режим прохождения сквозь всё
        # создаем свойство hero и загружаем модель
        self.hero = loader.loadModel('smiley')
        # цвет для hero
        self.hero.setColor(1, 0.5, 0)
        # размер для hero
        self.hero.setScale(0.3)
        # позиция для hero
        self.hero.setPos(pos)
        # устанавливаем родительский узел render
        self.hero.reparentTo(render)
        # вызываем метод для закрепления камеры на игроке
        self.cameraBind()
        self.accept_events()

    # метод для закрепления камеры на игроке
    def cameraBind(self):
        # выключить управление камеры с помощью мыши
        base.disableMouse()
        # поворот камеры на 180 градусов
        base.camera.setH(180)
        # привязываем камеру к игроку
        base.camera.reparentTo(self.hero)
        # установить камеру в указанные координаты
        base.camera.setPos(0, 0, 1.5)
        # показывает  прикреплена камера или нет
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        # помещаем узел камеры в координатах x,y,z (минус - потому что камера повернута на 180 градусов)
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        # привязываем камеру к узлу render
        base.camera.reparentTo(render)
        # включаем управление мышью
        base.enableMouse()
        # показывает  прикреплена камера или нет
        self.cameraOn = False


    def changeView(self):
        # алгоритм смены вида камеры
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        # обработка поворота камеры влево (вокруг оси z)
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        # обработка поворота камеры вправо (вокруг оси z)
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):
        ''' возвращает координаты, в которые переместится персонаж, стоящий в точке (x, y),
        если он делает шаг в направлении angle'''

        # получаем координаты x,y,z игрока и округляем их
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        # вычисляем изменение координат x, y в зависимости от угла поворота камеры (метод check_dir)
        dx, dy = self.check_dir(angle)
        # изменяем значения координат
        x_to = x_from + dx
        y_to = y_from + dy
        # возвращаем измененные значения координат
        return x_to, y_to, z_from

    # метод определяет движение игрока как наблюдателя
    def just_move(self, angle):
        '''перемещается в нужные координаты в любом случае'''
        # узнаем координаты куда смотрит игрок
        pos = self.look_at(angle)
        # перемещаем игрока в полученные координаты
        self.hero.setPos(pos)

    # метод определяет вид движения в зависимости от self.mode
    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)
    
    def check_dir(self,angle):
        ''' возвращает округленные изменения координат X, Y, 
        соответствующие перемещению в сторону угла angle.
        Координата Y уменьшается, если персонаж смотрит на угол 0,
        и увеличивается, если смотрит на угол 180.    
        Координата X увеличивается, если персонаж смотрит на угол 90,
        и уменьшается, если смотрит на угол 270.    
            угол 0 (от 0 до 20)      ->        Y - 1
            угол 45 (от 25 до 65)    -> X + 1, Y - 1
            угол 90 (от 70 до 110)   -> X + 1
            от 115 до 155            -> X + 1, Y + 1
            от 160 до 200            ->        Y + 1
            от 205 до 245            -> X - 1, Y + 1
            от 250 до 290            -> X - 1
            от 290 до 335            -> X - 1, Y - 1
            от 340                   ->        Y - 1  '''
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)


    # движение вперед
    def forward(self):
        # получаем текущий угол поворота игрока + смещение % получаем остаток от деления на 360
        angle =(self.hero.getH()) % 360
        # вызываем метод move_to
        self.move_to(angle)

    # движение назад
    def back(self):
        # получаем текущий угол поворота игрока + смещение % получаем остаток от деления на 360
        angle = (self.hero.getH()+180) % 360
        # вызываем метод move_to
        self.move_to(angle)

    # движение влево
    def left(self):
        # получаем текущий угол поворота игрока + смещение % получаем остаток от деления на 360
        angle = (self.hero.getH() + 90) % 360
        # вызываем метод move_to
        self.move_to(angle)

    # движение вправо
    def right(self):
        # получаем текущий угол поворота игрока + смещение % получаем остаток от деления на 360
        angle = (self.hero.getH() + 270) % 360
        # вызываем метод move_to
        self.move_to(angle)

    # изменение игрового режима
    def changeMode(self):
        # алгоритм изменения игрового режима
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    # основной режим (от лица игрока)
    def try_move(self, angle):
        '''перемещается, если может'''
        pos = self.look_at(angle)
        # обработка перемещений
        if self.land.isEmpty(pos):
            # перед нами свободно. Возможно, надо упасть вниз:
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            # перед нами занято. Если получится, заберёмся на этот блок:
            pos = pos[0], pos[1], pos[2] + 1
            # не получится забраться - стоим на месте
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)


    # движение вверх
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    # движение вниз
    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    # создает блок
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    # уничтожает блок
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    # метод для подписи на все необходимые события
    def accept_events(self):
        # при разовом нажатии на клавишу выполняется метод turn_left
        base.accept(key_turn_left, self.turn_left)
        # при постоянном нажатии на клавишу выполняется метод turn_left
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)

        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.changeMode)

        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)

        base.accept(key_build, self.build)
        base.accept(key_destroy, self.destroy)

        base.accept(key_savemap, self.land.saveMap)
        base.accept(key_loadmap, self.land.loadMap)
       