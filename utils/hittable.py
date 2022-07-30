from dataclasses import dataclass
from .ray import Ray
from .vec3 import Vec3, Point3
from .material import Material
from abc import ABC, abstractmethod

@dataclass
class HitRecord:
	p: Point3 = Point3()
	normal: Vec3 = Vec3(0, 0, 0)
	t: float = 0
	front_face: bool = False
	mat: Material = None

	def set_face_normal(self, r, outward_normal):
		self.front_face = (r.direction().dot(outward_normal) < 0)
		self.normal = outward_normal if self.front_face else -outward_normal

class Hittable(ABC):

	@abstractmethod
	def hit(self, r, t_min, t_max, rec):
		pass
