from django.db import models
from basedata.models import SoftDeletionModel




class PracticeChoice(SoftDeletionModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class PracticeQuestion(SoftDeletionModel):
    question = models.CharField(max_length=200)
    choices = models.ManyToManyField('PracticeChoice')
    answer = models.ForeignKey(
        					'PracticeChoice', 
        					on_delete=models.SET_NULL, 
        					related_name='answer', 
        					blank=True, 
        					null=True
        				)
    practice = models.ForeignKey(
        					'StudyPractice',
        					on_delete=models.SET_NULL, 
        					related_name='questions', 
        					blank=True, 
        					null=True
        				)
    order = models.SmallIntegerField()

    def __str__(self):
        return self.question





class StudyPractice(SoftDeletionModel):

	title =
	topic =
	total_mark = 
	date = 




class StudyPractice(SoftDeletionModel):

	title =
	topic =
	total_mark = 
	date = 




