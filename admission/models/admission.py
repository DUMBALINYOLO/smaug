# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from basedata.constants import ONLINE_ADMISSION_STATUS_CHOICES
from basedata.models import SoftDeletionModel




class OnlineAdmission(SoftDeletionModel):
	""" A model for online admission, it represents a database table, each variable below represents a field in the database table. """
	
	#Applicant Information
	date = models.DateField(auto_now_add=True)
	applicant = models.ForeignKey(
							'persons.Student',
							blank=True,
							null=True,
							related_name = 'applications'
						)
	status = models.CharField(max_length=100, choices=ONLINE_ADMISSION_STATUS_CHOICES, default='pending')
	class_  = models.ForeignKey(
							'setup.StudentClass',
							blank=True,
							null=True,
							related_name = 'applicants'
						)
	school = models.ForeignKey(
							'setup.School',
							blank=True,
							null=True,
							related_name = 'incomingapplications'
						)

	def __str__(self):
		return self.applicant.__str__()

		




