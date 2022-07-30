from .hittable import Hittable, HitRecord
import math

class Sphere(Hittable):
    def __init__(self, center, radius, mat):
        self.center = center
        self.radius = radius
        self.material = mat

    def hit(self, r, t_min, t_max, rec):
        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = r.direction().dot(oc)
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False
        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if(root < t_min or root > t_max):
            root = (-half_b + sqrtd) / a
            if(root < t_min or root > t_max):
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material

        return True

