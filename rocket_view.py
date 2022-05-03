# rocket point of view
import pygame
import trajectory_calculation as tr
import sandbox as sb

SKY = [0, 42, 255]
GREEN = [0, 255, 0]
GREY = [109, 114, 135]

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

w, h = pygame.display.get_surface().get_size()
rocket_view = pygame.Surface((w / 2, h))
rocket_view.fill(SKY)


im_height = 0
for part in sb.rocket.parts:
    im_height += sb.rocket.parts[0].texture.get_rect().size[1]

im_size = sb.rocket.parts[0].texture.get_rect().size
print(im_size)
# pygame.draw.rect(rocket_view, GREEN, (0, h - 50, w / 2, 50))
# pygame.draw.rect(rocket_view, GREY, (100, h - 100, w / 2 - 200, 50))
# pygame.draw.line(rocket_view, [0, 0, 0], (w / 4, 0), (w / 4, h))
# rocket_view.blit(sb.r.get_surface(), (w / 4 - im_size[0] / 2, h - 100 - im_height))

scale = 5

def rocket_position(arr):
    x = arr[0]
    y = arr[1]
    height = (x ** 2 + y ** 2) ** 0.5 - tr.const.rad_Earth
    if int(255 * (1 - height / (3 * 10 ** 5))) > 30:
        SKY[2] = int(255 * (1 - height / (3 * 10 ** 5)))
    else:
        SKY[2] = 30
    if int(42 * (1 - height / (3 * 10 ** 5))) > 5:
        SKY[1] = int(42 * (1 - height / (3 * 10 ** 5)))
    else:
        SKY[1] = 5


    #print(SKY, height)
    rocket_view.fill(SKY)

    if height * scale <= 50:
        pygame.draw.rect(rocket_view, GREEN, (0, h - 50 + height * scale, w / 2, 50))
    if height * scale <= 100:
        pygame.draw.rect(rocket_view, GREY, (100, h - 100 + height * scale, w / 2 - 200, 50))
    rocket_view.blit(sb.rocket.get_surface(), (w / 4 - im_size[0] / 2, h - 100 - im_height))
