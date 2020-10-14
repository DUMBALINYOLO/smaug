from django.db import models
from basedata.models import SoftDeletionModel
from basedata.constants import COURSES_STATUS_CHOICES


class Course(SoftDeletionModel):
    title = models.CharField(max_length=300)
    subject = models.ForeignKey(
    					'curriculum.Subject', 
    					on_delete=models.CASCADE, 
    					related_name='courses'
    				)
    level  = models.ForeignKey(
                            'setup.Level',
                            blank=True,
                            null=True,
                            related_name = 'attendances'
                        ) 
    status = CharField(max_length=300, choices=COURSES_STATUS_CHOICES)
    overview= models.TextField(blank=False)
    student_exit_profile = models.TextField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



    def __str__(self):
		return self.title

class TopicObjectives(SoftDeletionModel):
	name = models.CharField(max_length=300)
	description = models.TextField(blank=False)


	def __str__(self):
		return self.name


class TopicGuideLine(SoftDeletionModel):
	name = models.CharField(max_length=300)
	description = models.TextField(blank=False)


	def __str__(self):
		return self.name


class Topic(SoftDeletionModel):
    title = models.CharField(max_length=300)
    course = models.ForeignKey(
    					'Course', 
    					on_delete=models.SET_NULL, 
    					related_name='topics',
    					null=True
    				)
    aims = models.ManyToManyField('TopicObjectives')
    content_overview= models.TextField(blank=False)
    assessment_overview= models.TextField(blank=False)
    assessment_objectives = models.ManyToManyField('TopicObjectives', related_name='topics_assesment')
    guidelines = models.ManyToManyField('TopicGuideLine')


    def __str__(self):
		return self.title

	@property
	def subtopics(self):
		return self.subtopics.all()

	@property
	def subtopics_count(self):
		return self.subtopics.count()
	


#nested
class SubTopic(SoftDeletionModel):

	title = models.CharField(max_length=300)
    topic = models.ForeignKey(
    					'Topic', 
    					on_delete=models.SET_NULL, 
    					related_name='subtopics',
    					null=True
    				)
    bibliography = models.ManyToManyField('ReferrenceSource')

    def __str__(self):
		return self.title


	@property
	def notes(self):
		return self.notes.prefetch_related(
									'images',
									'videos',
									'files',
									'glossary',
								)


	@property
	def assignments(self):
		return self.assignments.prefetch_related(
									'',
									'',
								)

	@property
	def practices(self):
		return self.practices.prefetch_related(
									'',
									'',
								)

	@property
	def tests(self):
		return self.tests.prefetch_related(
									'',
									'',
								)



    	topic
		guidelines
		objectives
		subtopic
			notes
				glosarry
				title
				sources(ManyToManyField(Bibliography))
				media that is video, pictures, diagrams, graphs
			test
				question
				choices
				answer
				score
				corrections
			asignment
				question
				choices
				answer
				score
				corrections
			excercises
				question
				choices
				answer
				score
				corrections

			Practice
				question
				choices
				answer
				score
				corrections
