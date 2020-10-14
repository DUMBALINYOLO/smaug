from django.db import models
from decimal import Decimal as D
from basedata.models import SoftDeletionModel


class Level(SoftDeletionModel):

	grade = models.CharField(max_length=68)

	def __str__(self):
		return self.grade

	@property
	def classes(self):
		return self.classes.all()


	@property
	def classes_count(self):
		return self.classes.count()
	
	@property
	def student_population(self):
		return sum([klaus.population, for klaus in self.classes])
	


class StudentClass(SoftDeletionModel):

	name = models.CharField(max_length=68)
	school = models.ForeignKey(
							'school.School',
							on_delete=models.SET_NULL,
							null=True,
							related_name='curriculums'
						)
	level = models.ForeignKey(
					'Level', 
					related_name='classes',
					on_delete=models.SET_NULL, 
					null=True
				)
	max_population = models.IntegerField(default=0)
	population = models.IntegerField(default=0)
	class_teacher = models.ForeignKey('persons.Teacher', on_delete=models.SET_NULL, null=True)
	creation_date  =   models.DateTimeField(auto_now=False, auto_now_add=True)
	no_subjects = models.PositiveIntegerField('Number of subjects offered', default=0)



	def __str__(self):
		return self.name

	def increment_student_number(self, amount):
        self.population += D(amount)
        self.save()
        return self.population


    def decrement_student_number(self, amount):
        self.population -= D(amount)
        self.save()
        return self.population

    
    @property
    def is_full(self):
    	pass

    @property
    def has_place(self):
    	pass

    @property
    def has_place(self):
    	pass
    	








