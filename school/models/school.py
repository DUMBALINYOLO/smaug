from django.db import models
from basedata.models import SoftDeletionModel
from basedata.constants  SCHOOL_STATUS_CHOICES, SCHOOL_TYPE_CHOICES


class School(SoftDeletionModel):

	name = models.CharField(max_length=68)
	type = models.CharField(max_length=68, choices=SCHOOL_TYPE_CHOICES)
	status = models.CharField(max_length=68, choices=SCHOOL_STATUS_CHOICES)
	address = models.TextField(max_length=68)
	head_office = models.ForeignKey(
							'school.SchoolHeadOffice',
							on_delete=models.SET_NULL,
							null=True,
							blank=True
						)


	def __str__(self):
		return self.name

		







