# Calculating the trajectory of a rocket


import numpy as np
import matplotlib.pyplot as plt

""" блок констант """
height_max = 9000  # высота в метрах, на которой плотность воздуха падает в е раз
rho_max = 1.2  # плотность воздуха на высоте уровня моря
area = 2.  # площадь КА с открытым парусом
C_coeff = 0.4  # коэффициент аэродинамического сопротивления
g_0 = 9.8  # ускорение свободного падения на уровне моря
rad_Earth = 6.37e6  # радиус Земли (средний)
WCS = 5.1e-4  # произведение солнечной постоянной W = 1367 Вт/м, скорости света с = 3.e8 м/с, площади S
mu_moon = 4.91e12  # гравитационный параметр Луны (гравитационная постоянная * масса)
moon_rad = 3.85e8  # радиус орбиты Луны
moon_period = 27.3 * 24 * 3600 / 2 / np.pi  # период обращения Луны вокруг Земли в с/рад
sun_period = 24 * 3600

fas_0 = 99 / 180 * np.pi  # начальная фаза Луны (которую нужно подогнать)


class Stage:
    """
    класс ступени ракеты
    """

    def __init__(self, pn, mass, speed, consumption):
        self.pn_ = pn  # полезная нагрузка
        self.mass_ = mass  # масса ступени текущая
        self.speed_ = speed  # скорость истечения топлива
        self.consumption_ = consumption  # расход топлива


def calc_rho(height):
    """ вычисляет плотность воздуха на высоте height от Земли """
    return rho_max * np.exp(-height / height_max)


def where_moon(time):
    return moon_rad * np.array(
        [np.cos(fas_0 + time / moon_period), np.sin(fas_0 + time / moon_period)])


def accel(pos_vel, stage, isOn, light):
    """
    считает ускорение КА
    :param pos_vel: массив (x, y, Vx, Vy)
    :param stage: параметры ступени
    :param isOn: включен ли двигатель
    :param light: учитывать ли солнечное давление
    :return: массив (ax, ay)
    """
    pos_norm = np.linalg.norm(pos_vel[:2])
    vel_norm = np.linalg.norm(pos_vel[2:])

    if pos_norm - rad_Earth < 10 * height_max:
        accel_air = -0.5 * C_coeff * calc_rho(pos_norm - rad_Earth) * area * vel_norm * pos_vel[2:] / stage.mass_
    else:
        accel_air = np.zeros(2)

    accel_g = -g_0 / pos_norm / pos_norm * rad_Earth * rad_Earth * pos_vel[:2] / pos_norm

    if isOn:
        if vel_norm > 1e-8:
            accel_fuel = stage.consumption_ * stage.speed_ / stage.mass_ * pos_vel[2:] / vel_norm
        else:
            accel_fuel = np.array([stage.consumption_ * stage.speed_ / stage.mass_, 0])
    else:
        accel_fuel = np.zeros(2)

    accel_light = np.zeros(2)
    if light and pos_vel[1] < 0:
        accel_light = np.array([2 * WCS, 0])

    rad_moon_ka = pos_vel[:2] - where_moon(time[counter])

    accel_moon = - mu_moon * rad_moon_ka / (np.linalg.norm(rad_moon_ka)) ** 3

    return accel_air + accel_g + accel_fuel + accel_light + accel_moon


def df(q, stage, flag, light):
    """ вычисляет дифференциал функции (промежутчная функция метода Рунге-Кутта) """
    acc = accel(q, stage, flag, light)
    return np.array([q[2], q[3], acc[0], acc[1]])


def calc_step(q, step, stage, isOn, light):
    """
    основная функция расчета шага
    :param q: массив (x, y, Vx, Vy) на предыдущем шаге
    :param step: время одного шага
    :param stage: параметры ступени
    :param isOn: включен ли двигатель
    :return: массив (x, y, Vx, Vy) на текущем шаге
    """
    k_1 = df(q, stage, isOn, light)
    k_2 = df(q + 0.5 * step * k_1, stage, isOn, light)
    k_3 = df(q + 0.5 * step * k_2, stage, isOn, light)
    k_4 = df(q + step * k_3, stage, isOn, light)

    """ уменьшение массы ступени """
    stage.mass_ -= stage.consumption_ * step

    return q + (k_1 + 2 * (k_2 + k_3) + k_4) * step / 6


size = 500000

pos_vel = np.ndarray(shape=(size, 4), dtype=float)
pos_vel[0] = np.array([rad_Earth, 0, 0, 0])  # основной массив (x, y, Vx, Vy)
time = np.ndarray(shape=(size,), dtype=float)  # текущее время расчета
dtime = 5  # шаг расчета
counter = 0  # счетчик
alpha = 75 / 180 * np.pi  # угол, на который отклонится аппарат после отделения первой ступени (нужно подогнать)

first_stage = Stage(30000, 80000, 4000, 300)  # параметры первой ступени
second_stage = Stage(2000, first_stage.pn_, 3000, 200)  # параметры второй ступени
third_stage = Stage(5, second_stage.pn_, 265, 50)  # параметры третьей ступени

while first_stage.mass_ * 0.95 > first_stage.pn_:
    counter += 1
    pos_vel[counter] = (calc_step(pos_vel[counter - 1], dtime, first_stage, True, False))
    time[counter] = time[counter - 1] + dtime

fig, ax = plt.subplots()
plt.axis('equal')
ax.add_patch(plt.Circle((0, 0), rad_Earth))

ax.plot(pos_vel[:counter, 0], pos_vel[:counter, 1], color="black", linewidth=4)
# plt.scatter(time[:counter], [np.linalg.norm(q) for q in pos_vel[:counter, :2]])

# """ здесь происходит поворот РН """
# pos_vel_norm = np.linalg.norm(pos_vel[counter][2:])
# pos_vel[counter][2:] = [pos_vel_norm * np.cos(alpha), pos_vel_norm * np.sin(alpha)]
#
# while second_stage.mass_ * 0.95 > second_stage.pn_:
#     counter += 1
#     pos_vel[counter] = (calc_step(pos_vel[counter - 1], dtime, second_stage, True, False))
#     time[counter] = time[counter - 1] + dtime
#
# ax.plot(pos_vel[:counter, 0], pos_vel[:counter, 1], color="blue", linewidth=3)
# # plt.scatter(time[:counter], [np.linalg.norm(q) for q in pos_vel[:counter, :2]])
#
# while third_stage.mass_ * 0.95 > third_stage.pn_:
#     counter += 1
#     pos_vel[counter] = (calc_step(pos_vel[counter - 1], dtime, third_stage, True, False))
#     time[counter] = time[counter - 1] + dtime
#
# ax.plot(pos_vel[:counter, 0], pos_vel[:counter, 1], color="green", linewidth=2)
# # plt.scatter(time[:counter], [np.linalg.norm(q) for q in pos_vel[:counter, :2]])
# #
# per_time = time[counter]
# per_tan = pos_vel[counter, 1] / pos_vel[counter, 0]  # условие на поиск противоположной перицентру точки
#
# while time[counter] < 30000:  # ступени отработали, просто летим
#     if np.linalg.norm(pos_vel[counter, :2]) < np.linalg.norm(pos_vel[counter - 1, :2]):
#         if time[counter] - 10 * dtime > per_time and abs(pos_vel[counter, 1] / pos_vel[counter, 0] - per_tan) < 0.08 \
#                 and pos_vel[counter, 0] < 0:
#             break
#     counter += 1
#     pos_vel[counter] = (calc_step(pos_vel[counter - 1], dtime, third_stage, False, False))
#     time[counter] = time[counter - 1] + dtime
#
# ax.plot(pos_vel[:counter, 0], pos_vel[:counter, 1], color="red", linewidth=1)
# # plt.scatter(time[:counter], [np.linalg.norm(q) for q in pos_vel[:counter, :2]])
#
# pos_vel[counter][2:] *= 1.93  # в апоцентре даем импульс и выходим на круговую орбиту (нужно подогнать)
# third_stage.mass_ /= 1.93
#
# dtime = 30  # увеличиваем шаг интегрирования
#
# while pos_vel[counter, 0] > -42164e3 and time[counter] < 1e5:
#     counter += 1
#     pos_vel[counter] = (calc_step(pos_vel[counter - 1], dtime, third_stage, False, False))
#     time[counter] = time[counter - 1] + dtime
#
# ax.plot(pos_vel[:counter, 0], pos_vel[:counter, 1], color="orange", linewidth=0.5)
# # plt.plot(time[:counter], [np.linalg.norm(q) for q in pos_vel[:counter, :2]])
# # plt.plot([0, time[counter]], [42164e3] * 2, color='red')
#
# ax.add_patch(plt.Circle((0, 0), radius=moon_rad, fill=False))
# ax.add_patch(
#     plt.Circle(where_moon(time[counter]), radius=10 * 1.7e6, fill=True))
#
# dtime = 100
# min_moon_dist = np.linalg.norm(where_moon(time[counter]) - pos_vel[counter, :2])
#
# while np.linalg.norm(pos_vel[counter][:2]) < 1.05 * 3.85e8 and time[counter] < 1e7:
#     counter += 1
#     pos_vel[counter] = (calc_step(pos_vel[counter - 1], dtime, third_stage, False, True))
#     time[counter] = time[counter - 1] + dtime
#     min_moon_dist = min(min_moon_dist, np.linalg.norm(where_moon(time[counter]) - pos_vel[counter, :2]))
#
# ax.plot(pos_vel[:counter, 0], pos_vel[:counter, 1], color="pink", linewidth=0.3)
#
# print("the flight took", time[counter] / 3600 / 24, "days")
# print("min distance between satellite and moon", round(min_moon_dist / 1.e3), "km")

plt.show()
