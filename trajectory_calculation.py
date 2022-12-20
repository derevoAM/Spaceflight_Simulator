import numpy as np


class Constants:
    """
    Constants used throughout the script execution
    """

    def __init__(self, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, initial_mass):
        """
        Initializing constants class
        :param gas_exhaust_speed: engine characteristic
        :param fuel_consumption: engine characteristic
        :param fuel_tank_capacity: overall tanks capacity
        :param initial_mass: initial rocket mass
        """
        self.rad_Earth = 6.37e6
        self.rad_Moon = 1.74e6
        self.mu_Earth = 4e14
        self.mu_moon = 4.91e12
        self.moon_rad = 3.85e8
        self.moon_period = 27.3 * 24 * 3600 / 2 / np.pi
        self.initial_fas = 99 / 180 * np.pi
        self.log_size = 500

        self.gas_exhaust_speed = gas_exhaust_speed
        self.fuel_consumption = fuel_consumption
        self.fuel_tank_capacity = fuel_tank_capacity
        self.initial_mass = initial_mass

        self.step = 0.5


class RocketParameters:

    def __init__(self, initial_parameters, initial_rocket_mass, tanks_fullness):
        """
        Initializing RocketParameters class
        :param initial_parameters: [x, y, vx, vy] array, consisting of initial rocket coordinates and velocity
        :param initial_rocket_mass: initial rocket mass
        :param tanks_fullness: mass of fuel stored in tanks
        """
        self.parameters = np.array(initial_parameters)
        self.direction = np.array([1, 0])
        self.current_time = 0.0
        self.predictive_orbit = np.ndarray(shape=(0, 4), dtype=float)

        self.current_stage_mass = initial_rocket_mass
        self.fuel_remained = tanks_fullness
        self.engine_power = 1.0

        self.engine_is_on_flag = True
        self.collision_flag = False

    def is_empty(self):
        """
        :return: true if no fuel is available, otherwise false
        """
        return self.fuel_remained <= 0


class PhysicsEngine:

    def __init__(self, initial_rocket_mass, gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, tanks_fullness,
                 initial_parameters):
        """
        Initializing PhysicsEngine class
        :param initial_rocket_mass: initial rocket mass
        :param gas_exhaust_speed: engine characteristic
        :param fuel_consumption: engine characteristic
        :param fuel_tank_capacity: overall tanks capacity
        :param tanks_fullness: mass of fuel stored in tanks
        :param initial_parameters: [x, y, vx, vy] array, consisting of initial rocket coordinates and velocity
        """
        self.constants = Constants(gas_exhaust_speed, fuel_consumption, fuel_tank_capacity, initial_rocket_mass)
        self.rocket_parameters = RocketParameters(initial_parameters, initial_rocket_mass, tanks_fullness)

    def set_predicative_orbit_log_size(self, new_size):
        """
        Function to set the number of predicative points to be calculated on each step
        :param new_size: number of points
        """
        self.constants.log_size = new_size

    def set_rocket_direction(self, angle):
        """
        Function to update rocket_direction, creates directional vector of length 1
        :param angle: new rocket angle in radians (zero angle is Ox axis, increasing counterclockwise)
        """
        self.rocket_parameters.direction = np.array([np.cos(angle), np.sin(angle)])

    def turn_rocket(self, angle):
        """
        Changing rocket angle
        :param angle: angle of rotation in radians, can be either positive or negative (positive angle refers to turning
        rocket
        counterclockwise)
        """
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        self.rocket_parameters.direction = np.dot(rotation_matrix, self.rocket_parameters.direction)

    def reduce_mass(self):
        """
        Function to reduce rocket mass on each step.
        :return:
        """

        if self.rocket_parameters.engine_is_on_flag and not self.rocket_parameters.is_empty():
            self.rocket_parameters.fuel_remained -= self.rocket_parameters.engine_power * self.constants.step * \
                                                    self.constants.fuel_consumption
            self.rocket_parameters.current_stage_mass -= \
                self.rocket_parameters.engine_power * self.constants.step * self.constants.fuel_consumption

        if self.rocket_parameters.fuel_remained <= 0:
            self.rocket_parameters.fuel_remained = 0

    def switch_engine(self, flag, power=1.0):
        """
        Function to switch engine on/off and change it's power
        :param flag: true if engine is working, otherwise false
        :param power: power coefficient, default is 1
        """
        self.rocket_parameters.engine_is_on_flag = flag
        self.rocket_parameters.engine_power = power

    def detect_collision(self):
        """
        Function to detect collision with Earth
        """
        if np.linalg.norm(self.rocket_parameters.parameters[:2]) < self.constants.rad_Earth:
            self.rocket_parameters.collision_flag = True

    def calc_moon_position(self, time):
        """
        Calculating moon position in the particular moment of time
        :param time: time of calculation
        :return: array [x, y] of moon coordinates
        """
        return self.constants.moon_rad * np.array(
            [np.cos(self.constants.initial_fas + time / self.constants.moon_period),
             np.sin(self.constants.initial_fas + time / self.constants.moon_period)])

    def calc_acceleration_earth(self, parameters, position_norm):
        """
        Calculating gravitational acceleration by Earth
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param position_norm: the norm of vector earth-rocket
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        return - self.constants.mu_Earth / position_norm ** 3 * parameters[:2]

    def calc_acceleration_engine(self):
        """
        Calculating acceleration by engine working
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        if self.rocket_parameters.engine_is_on_flag and not self.rocket_parameters.is_empty():
            return self.rocket_parameters.engine_power * \
                   self.constants.fuel_consumption * self.constants.gas_exhaust_speed / \
                   self.rocket_parameters.current_stage_mass * \
                   self.rocket_parameters.direction

        else:
            return np.zeros(2)

    def calc_acceleration_moon(self, parameters, time):
        """
        Calculating gravitational acceleration made by moon
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: global time
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        rad_moon_ka = parameters[:2] - self.calc_moon_position(time)

        return - self.constants.mu_moon * rad_moon_ka / (np.linalg.norm(rad_moon_ka)) ** 3

    def calc_acceleration(self, parameters, time):
        """
        Calculating final value of vehicle acceleration
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: global time
        :return: [ax, ay] array consisting of acceleration values for each axis
        """
        position_norm = np.linalg.norm(parameters[:2])

        acceleration_gravity = self.calc_acceleration_earth(parameters, position_norm)

        acceleration_engine = self.calc_acceleration_engine()

        acceleration_moon = self.calc_acceleration_moon(parameters, time)

        return acceleration_gravity + acceleration_engine + acceleration_moon

    def calc_differential(self, parameters, time):
        """
        Calculating Runge-Kutta method differential
        :param parameters: [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: global time
        :return: [vx, vy, ax, ay] array
        """
        total_acceleration = self.calc_acceleration(parameters, time)

        return np.array([parameters[2], parameters[3], total_acceleration[0], total_acceleration[1]])

    def calc_step(self):
        """
        Main function to calculate stage parameters for the next step
        :return: array [new_x, new_y, new_vx, new_vy] for the next step
        """
        k_1 = self.calc_differential(self.rocket_parameters.parameters, self.rocket_parameters.current_time)
        k_2 = self.calc_differential(self.rocket_parameters.parameters + 0.5 * self.constants.step * k_1,
                                     self.rocket_parameters.current_time + 0.5 * self.constants.step)
        k_3 = self.calc_differential(self.rocket_parameters.parameters + 0.5 * self.constants.step * k_2,
                                     self.rocket_parameters.current_time + 0.5 * self.constants.step)
        k_4 = self.calc_differential(self.rocket_parameters.parameters + self.constants.step * k_3,
                                     self.rocket_parameters.current_time + 0.5 * self.constants.step)

        self.reduce_mass()

        self.rocket_parameters.parameters += (k_1 + 2 * (k_2 + k_3) + k_4) * self.constants.step / 6
        self.rocket_parameters.current_time += self.constants.step

    def calc_differential_euler(self, predicative_parameters, time):
        """
        Function to calculate differential for predicative orbit parameters
        :param predicative_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: time used in predicative calculations
        :return: predicative [vx, vy, ax, ay] array
        """
        total_acceleration = self.calc_acceleration_earth(predicative_parameters, np.linalg.norm(
            predicative_parameters[:2])) + self.calc_acceleration_moon(predicative_parameters, time)

        return np.array([predicative_parameters[2], predicative_parameters[3], total_acceleration[0],
                         total_acceleration[1]])

    def calc_step_euler(self, predicative_parameters, time):
        """
        Function to process step using basic integration method
        :param predicative_parameters: predicative [x, y, vx, vy] array consisting of rocket stage parameters
        :param time: time used in predicative calculations
        :return: predicative [new_x, new_y, new_vx, new_vy] array
        """
        return \
            predicative_parameters + self.calc_differential_euler(predicative_parameters, time) * \
            self.constants.step * 20, time + self.constants.step * 5

    def calc_predicative_orbit(self):
        """
        Function to calculate predicative orbit
        :return: array [[x, y, vx, vy], ...] consisting of predicative orbit points
        """
        log_size = self.constants.log_size
        time_array = np.zeros(log_size)
        time_array[0] = self.rocket_parameters.current_time
        predicative_orbit = np.ndarray(shape=(log_size, 4), dtype=float)
        predicative_orbit[0] = self.rocket_parameters.parameters
        count = 0

        while count < log_size - 1 and not np.linalg.norm(predicative_orbit[count][:2]) < self.constants.rad_Earth:
            count += 1
            predicative_orbit[count], time_array[count] = self.calc_step_euler(predicative_orbit[count - 1],
                                                                               time_array[count - 1])

        predicative_orbit = np.resize(predicative_orbit, (count, 4))
        self.rocket_parameters.predictive_orbit = predicative_orbit

    def process_step(self):
        """
        Function to process step
        """
        self.calc_step()
        self.calc_predicative_orbit()
        self.detect_collision()
