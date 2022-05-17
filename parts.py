class Entity:
    """
    Just a class whose object will be statically drawn on the rocket
    Can draw itself on the screen of the rocket.
    """

    def __init__(self, surface, x=0, y=0, size=1, mass=0):
        """
        part object class constructor
        surface - object of class pygame.surface
        x, y - coordinates of the upper left corner of the image on the screen.
        size - size of the part (for future, small, large or medium)
        mass = mass of the pattern
        has activity fields
        (shows the program whether the component is currently working)
        """
        self.surface = surface
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.texture = None
        self.active = 1

    def draw(self):
        """
        Draws itself simply by pasting a rectangle of texture into the right place of the rocket's canvas
        """
        self.surface.blit(self.texture, dest=[self.x, self.y])


class Engine(Entity):
    """
    Rocket engine class
    """

    def __init__(self, surface, power=0, consumption=0, x=0, y=0, mass=0):
        """
        Here we already have the following fields
        consumption - fuel consumption
        power - output power at maximum fuel consumption
        output - percentage of current power from output power
        In the type field - type.
        """
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.power = power
        self.consumption = consumption
        self.output = 1
        self.power_on = 0
        self.type = "engine"


class FuelTank(Entity):
    """
    Fuel tank class
    """

    def __init__(self, surface, capacity=0, x=0, y=0, mass=0):
        """
        Here we already have the following fields
        capacity - tank capacity
        fullness - percentage of current fuel amount from full
        In the type field - type.
        """
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.capacity = capacity
        self.fullness = 1
        self.type = "fueltank"


class Cabin(Entity):
    """
    cabin class
    """

    def __init__(self, surface, x=0, y=0, mass=0):
        """
        Here is the type.
        """
        Entity.__init__(self, surface, x=x, y=y, mass=mass)
        self.type = "cabin"


if __name__ == "__main__":
    print("this module is not for direct use")
