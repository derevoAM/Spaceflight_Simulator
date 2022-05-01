import pygame
import textures as t
import parts as p
import pygame.draw as dr

# Этот файл просто возвращает холст с нарисованной ракетой

# объявили экран, на котором будем рисовать
#rocket_image = pygame.Surface([ROCKETWINDOWWIDTH, ROCKETWINDOWHEIGHT], pygame.SRCALPHA)

class Rocket:
    def __init__(self):
        self.grid_x = 30
        self.grid_y = 20
        self.block_x = 10
        self.block_y = 10
        self.width = self.grid_x * self.block_x
        self.height = self.grid_y * self.block_y
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        self.parts = []

    def add_part(self, part_entity):
        """
        В деталях заранее прописаны координаты
        """
        part_entity.surface = self.surface
        self.parts.append(part_entity)
        part_entity.draw()

    def recount(self):
        """
        Вот это надо делать всегда после изменения составляющих ракеты
        После этого слетит сетка, но зато избавимся от копий деталей
        Операция жрёт время (потенциально)
        """
        x_min = self.width
        y_min = self.width
        for part_entity in self.parts:
            if part_entity.x < x_min:
                x_min = part_entity.x
            if part_entity.y < y_min:
                y_min = part_entity.y
        for part_entity in self.parts:
            part_entity.x -= x_min
            part_entity.y -= y_min
        self.surface = pygame.Surface([self.width, self.height], pygame.SRCALPHA)
        for part_entity in self.parts:
            part_entity.surface = self.surface
            part_entity.draw()

    def get_surface(self):
        return self.surface

    def draw_grid(self):
        grey = (125, 125, 125)
        for i in range(self.block_x + 1):
            dr.line(self.surface, grey, (i * self.grid_x, 0), (i * self.grid_x, self.height))
        for j in range(self.block_y + 1):
            dr.line(self.surface, grey, (0,j * self.grid_y), (self.width, j * self.grid_y))

    def draw(self, gridded = 0):
        if gridded:
            self.draw_grid()
        for part_entity in self.parts:
            part_entity.draw()

screen = pygame.display.set_mode((900, 900))
engine = p.Engine(0, x = 4, y = 140)
r = Rocket()
r.add_part(engine)
#r.recount()
r.draw(gridded=1)
screen.blit(r.get_surface(), dest=[100,100])
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()


