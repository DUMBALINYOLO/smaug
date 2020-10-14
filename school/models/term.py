from django.db import models
from basedata.models import SoftDeletionModel


class Term(SoftDeletionModel):
	name = models.CharField(max_length=68)
	opening_date = models.DateField()
	closing_date = models.DateField()
	year = models.IntegerField()

	
