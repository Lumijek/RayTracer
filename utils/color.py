from math import sqrt

def clamp(x, a, b):
    return a if x < a else b if x > b else x

def write_color(f, pixel_color, samples_per_pixel):
    r = pixel_color.x()
    g = pixel_color.y()
    b = pixel_color.z()

    scale = 1 / samples_per_pixel
    r = sqrt(scale * r)
    g = sqrt(scale * g)
    b = sqrt(scale * b)
    f.write(
        f"{int(256 * clamp(r, 0, 0.999))} {int(256 * clamp(g, 0, 0.999))} {int(256 * clamp(b, 0, 0.999))}\n"
    )