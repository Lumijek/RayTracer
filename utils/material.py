from abc import ABC, abstractmethod
from .vec3 import Vec3
from .ray import Ray
from math import sqrt
from random import uniform

class Material(ABC):

	@abstractmethod
	def scatter(self, r_in, rec, attenuation, scattered):
		pass

class Lambertian(Material):
	def __init__(self, albedo):
		self.albedo = albedo

	def scatter(self, r_in, rec, attenuation, scattered):
		scatter_direction = rec.normal + Vec3().random_unit_vector()
		if scatter_direction.near_zero():
			scatter_direction = rec.normal
		scattered.orig = rec.p
		scattered.dir = scatter_direction
		attenuation.e[0] = self.albedo.x()
		attenuation.e[1] = self.albedo.y()
		attenuation.e[2] = self.albedo.z()
		return True

class Metal(Material):
	def __init__(self, albedo, f=0):
		self.albedo = albedo
		if f < 1:
			self.fuzz = f
		else:
			self.fuzz = 1

	def scatter(self, r_in, rec, attenuation, scattered):
		reflected = r_in.direction().unit_vector().reflect(rec.normal)
		scattered.orig = rec.p
		scattered.dir = reflected + self.fuzz * Vec3().random_in_unit_sphere()
		attenuation.e[0] = self.albedo.x()
		attenuation.e[1] = self.albedo.y()
		attenuation.e[2] = self.albedo.z()
		return scattered.direction().dot(rec.normal) > 0

class Dielectric(Material):
	def __init__(self, index_of_refraction):
		self.ir = index_of_refraction

	def scatter(self, r_in, rec, attenuation, scattered):
		attenuation.e[0] = 1
		attenuation.e[1] = 1
		attenuation.e[2] = 1
		refraction_ratio = 1 / self.ir if rec.front_face else self.ir

		unit_direction = r_in.direction().unit_vector()
		cos_theta = min(-unit_direction.dot(rec.normal), 1)
		sin_theta = sqrt(1 - cos_theta * cos_theta)

		cannot_refract = refraction_ratio * sin_theta > 1
		if (cannot_refract or self.reflectance(cos_theta, refraction_ratio) > uniform(0, 1)):
			direction = unit_direction.reflect(rec.normal)
		else:
			direction = unit_direction.refract(rec.normal, refraction_ratio)

		scattered.orig = rec.p
		scattered.dir = direction
		return True

	def reflectance(self, cosine, ref_idx):
		r0 = (1 - ref_idx) / (1 + ref_idx)
		r0 = r0 * r0
		return r0 + (1 - r0) * pow((1-cosine), 5)