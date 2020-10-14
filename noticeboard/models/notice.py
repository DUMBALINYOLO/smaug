from django.db import models
from basedata.models import SoftDeletionModel
from basedata.constants import SCHOOL_NOTICE_TYPE_CHOICES, SCHOOL_NOTICE_BOARD_STATUS_CHOICES


class Notice(SoftDeletionModel):

	title = models.CharField(max_length=68)
	school = models.ForeignKey(
							'school.School',
							on_delete=models.SET_NULL,
							null=True,
							related_name='curriculums'
						)
	type = models.CharField(max_length=200, choices=SCHOOL_NOTICE_TYPE_CHOICES)
	status = models.CharField(max_length=200, choices=SCHOOL_NOTICE_BOARD_STATUS_CHOICES)
	date_created = models.DateField()
	expiry_date = models.DateField()
	content = models.TextField()



	def __str__(self):
		return self.title

		



