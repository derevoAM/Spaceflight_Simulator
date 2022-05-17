import pygame

import parts as p
import trajectory_calculation


class Rocket:
    """
    Rocket class. Has an aray of parts, physical engine and a canvas, which as a drawn rocket on it
    """

    def __init__(self):
        """
        constructor
        initializes characteristics
        """
        self.width = 100
        self.height = 900
        self.surface = pygame.Surface([100, 900], pygame.SRCALPHA)
        self.angle = -90
        self.parts = []
        self.engine_bottom = 0
        self.fire_texture = pygame.image.load("textures/fire/fire.png")

        self.physics_engine = None

    def activate_stage(self):
        """
        recounts rocket parameters
        """
        self.physics_engine = trajectory_calculation.PhysicsEngine(5, *self.get_active_parameters())

    def activate_all(self):
        """
        activates all rocket parts
        """
        for part in self.parts:
            part.active = True

    def get_active_parameters(self):
        """
        returns characteristics of the rocket as a sum of the part's characteristics
        """
        initial_mass = 0
        exhaust_speed = 0
        fuel_consumption = 0
        capacity = 0
        fuel = 0

        for part in self.parts:
            initial_mass += part.mass
            if part.type == "fueltank" and part.active:
                capacity += part.capacity
                fuel += part.capacity * part.fullness

            elif part.type == "engine" and part.active:
                exhaust_speed = part.output * part.power
                fuel_consumption = part.output * part.consumption

        return [initial_mass, exhaust_speed, fuel_consumption, capacity, fuel]

    def add_part(self, part_entity):
        """
        adding part to the rocket
        part_entity - Entity class object
        """
        part_entity.surface = self.surface
        self.parts.append(part_entity)
        part_entity.draw()

    def recount(self):
        """
        This function builds rocket from it's parts array.
        It makes rocket parts to follow the order from up to down:
        capsule, fueltanks, engine
        """
        fuel_tanks_y = [0]
        cabin_height = 0
        part_counter = 0
        for part_entity in self.parts:
            if part_entity.type == "fueltank":
                fuel_tanks_y.append(fuel_tanks_y[-1] + part_entity.texture.get_height())
            elif part_entity.type == "cabin":
                cabin_height = part_entity.texture.get_height()
                self.width = part_entity.texture.get_width()
        for part_entity in self.parts:
            if part_entity.type == "fueltank":
                part_entity.y = cabin_height + fuel_tanks_y[part_counter]
                part_counter += 1
            elif part_entity.type == "engine":
                part_entity.y = cabin_height + fuel_tanks_y[-1]
                self.engine_bottom = part_entity.y + part_entity.texture.get_height()
        self.surface = pygame.Surface([self.width, self.engine_bottom + 200], pygame.SRCALPHA)
        for part_entity in self.parts:
            part_entity.surface = self.surface
            part_entity.draw()

    def get_surface(self):
        """
        returns canvas with the drawn rocket on it
        """
        return self.surface

    def draw(self, engine_power):
        """
        draws rocket on it's canvas and adds engine fire
        engine power - percentage of current power from maximum
        """
        self.surface = pygame.Surface([self.width, self.engine_bottom + 200], pygame.SRCALPHA)
        for part_entity in self.parts:
            part_entity.surface = self.surface
            part_entity.draw()
        fire_scaled = pygame.transform.scale(self.fire_texture, [self.width * 2 // 3,
                                                                 self.fire_texture.get_height() * engine_power / 300])
        self.surface.blit(fire_scaled, dest=[(self.width // 2) - (fire_scaled.get_width() // 2), self.engine_bottom])


def load_rocket(sourcefile):
    """
    loads rocket from the file
    sourcefile - path to the file with rocket
    """
    rocket_entity = Rocket()
    with open(sourcefile, "r") as f:
        part_lines = f.readlines()
    for part_line in part_lines:
        part_line_array = part_line.split()
        part_type = part_line_array[0]
        print(part_type, part_line_array[1], part_line_array[2])
        part_entity = None
        if part_type == "engine":
            # А другие параметры не волнуют, ракету мы загружаем только при старте
            part_entity = p.Engine(0, x=int(part_line_array[1]), y=int(part_line_array[2]))
        elif part_type == "fueltank":
            part_entity = p.FuelTank(0, x=int(part_line_array[1]), y=int(part_line_array[2]))
        elif part_type == "cabin":
            part_entity = p.Cabin(0, x=int(part_line_array[1]), y=int(part_line_array[2]))
        rocket_entity.add_part(part_entity)
    return rocket_entity


def save_rocket(rocket_entity, outfile):
    """
    saves the rocket to the file
    rocket_entity - Rocket class object
    outfile - path to the file
    """
    with open(outfile, "w") as file:
        for part_entity in rocket_entity.parts:
            file.write(str(part_entity.type) + " " + str(part_entity.x) + " " + str(part_entity.y) + "\n")


if __name__ == "__main__":
    print("this module is not for direct use")
