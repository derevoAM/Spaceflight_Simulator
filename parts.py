import pygame


class Entity:
    """
    Просто класс, объект которого будет статично отрисован на ракете
    Умеет отрисовывать себя на экране ракеты.
    """

    def __init__(self, surface, x=0, y=0, size=1, mass=0):
        """
        конструктор класса объекта детали
        surface - объект класса pygame.surface
        x, y - координаты левого верхнего угла изображения на экране.
        size - размер детали(на будущее, маленький, большой или средний)
        mass = масса детали
        имеет поля текстуры (путь к файлу, где хранится изображение) и активности
        (показывает программе, работает ли сейчас данный компонент)
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.texture = None
        self.active = 0

    def draw(self):
        """
        Рисует себя просто вклеиванием прямоугольника текстуры в нужное место холста ракеты
        """
        self.surface.blit(self.texture, dest=[self.x, self.y])


class Engine(Entity):
    """
    Класс ракетного двигателя
    """

    def __init__(self, surface, power=0, consumption=0, x=0, y=0, mass=0):
        """
        Здесь уже имеются поля
        consumption - потребление топлива
        power - выходная мощность при максимальном потреблении горючего
        output - процентная доля текущей мощности от выходной
        тут в поле текстуры уже стоит определённый путь к файлу, а в поле типа - тип.
        """
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.power = power
        self.consumption = consumption
        self.output = 100
        self.power_on = 0
        self.type = "engine"


class FuelTank(Entity):
    """
    Класс топливного бака
    """

    def __init__(self, surface, capacity=0, x=0, y=0, mass=0):
        """
        Здесь уже имеются поля
        capacity - вместимость бака
        fullness - процентная доля текущего количества топлива от полного
        тут в поле текстуры уже стоит определённый путь к файлу, а в поле типа - тип.
        """
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.capacity = capacity
        self.fullness = 100
        self.type = "fueltank"


class Cabin(Entity):
    """
    класс кабины
    """

    def __init__(self, surface, x=0, y=0, mass=0):
        """
        здесь прописан путь к текстуре и тип.
        """
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.type = "cabin"


if __name__ == "__main__":
    # Код для первичной проверки работы
    screen = pygame.display.set_mode((900, 900))
    rocket_image = pygame.Surface([400, 500], pygame.SRCALPHA)
    engine = Engine(screen, x=200, y=100)
    engine.texture = pygame.image.load("textures/engines/big_engine_100x75.png")
    engine.draw()
    print(engine.texture.get_height())
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

    pygame.quit()
