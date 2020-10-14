from django.db import models
from basedata.models import SoftDeletionModel


class SchoolHeadOffice(SoftDeletionModel):

	name = models.CharField(max_length=68)
	location = models.CharField(max_length=68)


	def __str__(self):
		return self.name


	def schools(self):
		return self.schools.all()


		