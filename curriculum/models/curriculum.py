from django.db import models
from basedata.models import SoftDeletionModel
from basedata.constants import STUDY_MODE_CHOICES


class Curriculum(SoftDeletionModel):

	name = models.CharField(max_length=68)
	code = models.CharField(max_length=68)


	def __str__(self):
		return self.name

	@property
	def subjects(self):
		return self.subjects.all()

	@property
	def subjects_number(self):
		return self.subjects.count()





class Subject(SoftDeletionModel):
	name = models.CharField(max_length=68)
	curriculum = models.ForeignKey(
							'curriculum.Curriculum',
							on_delete=models.SET_NULL,
							null=True,
							related_name='subjects',
						)
	mode = models.CharField(max_length=200, choices=STUDY_MODE_CHOICES)
	subject_code = models.CharField( max_length=10)


	def __str__(self):
		return self.name



