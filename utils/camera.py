from .vec3 import Point3, Vec3
from .ray import Ray
from math import radians, tan

class Camera:
	def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_dist):
		self.theta = radians(vfov)
		self.h = tan(self.theta / 2)
		self.viewport_height = 2 * self.h
		self.viewport_width = aspect_ratio * self.viewport_height

		self.w = (lookfrom - lookat).unit_vector()
		self.u = vup.cross(self.w).unit_vector()
		self.v = self.w.cross(self.u)

		self.origin = lookfrom
		self.horizontal = self.viewport_width * self.u * focus_dist
		self.vertical = self.viewport_height * self.v * focus_dist
		self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - focus_dist * self.w
		self.lens_radius = aperture / 2

	def get_ray(self, s, t):
		rd = self.lens_radius * Vec3().random_in_unit_disk()
		offset = self.u * rd.x() + self.v * rd.y()
		return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset)