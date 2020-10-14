from django.db import models
from basedata.models import SoftDeletionModel
from basedata.constants import STUDY_NOTES_STATUS_CHOICES, STUDY_NOTES_APPROVAL_STATUS_CHOICES


class StudyNotesFile(SoftDeletionModel):

	title = models.CharField(max_length=300)
	file = models.FileField(upload_to='filee/%Y/%m/%d/', null=True, blank=True)


	def __str__(self):
		return self.title


class StudyNotesImage(SoftDeletionModel):

	title = models.CharField(max_length=300)
	image = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)


	def __str__(self):
		return self.title


class StudyNotesGlossary(SoftDeletionModel):

	word = models.CharField(max_length=300)
	definition = models.TextField()


	def __str__(self):
		return self.word



class StudyNotesVideo(SoftDeletionModel):

	title = models.CharField(max_length=300)
	image = models.FileField(upload_to='videos/%Y/%m/%d/', null=True, blank=True)


	def __str__(self):
		return self.title



class StudyNote(SoftDeletionModel):
	title = models.CharField(max_length=300)
	topic = models.ForeignKey(
						'curriculum.SubTopic',
						null=True,
						on_delete=models.SET_NULL,
						related_name='notes'
					)
	
	status = models.CharField(max_length=300, choices=STUDY_NOTES_STATUS_CHOICES)
	approval_status = models.CharField(max_length=300, choices=STUDY_NOTES_APPROVAL_STATUS_CHOICES)
	images = models.ManyToManyField('StudyNotesImage')
	videos = models.ManyToManyField('StudyNotesVideo')
	files = models.ManyToManyField('StudyNotesVideo')
	glossary = models.ManyToManyField('StudyNotesGlossary')
	note = models.TextField()


	def __str__(self):
		return self.title
