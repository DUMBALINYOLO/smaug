from django.db import models
from config.utils import decimal_add
from django.utils.translation import ugettext_lazy as _
# from students.models import Student
from django.conf import settings
from functools import reduce
from decimal import Decimal
from basedata.models import SoftDeletionModel
from basedata.constants import TEST_TYPE_CHOICES


class Grading(SoftDeletionModel):
    institution = models.ForeignKey('school.School', on_delete=models.PROTECT, null=True)
    caption = models.CharField(max_length=15, null=True, unique=True)
    grade_points = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    start = models.IntegerField(null=True, default=0)
    end = models.PositiveIntegerField(null=True, default=100)

    class Meta:
        verbose_name = _(u'Grading')
        verbose_name_plural = _(u'Gradings')
        ordering = ('caption',)

    def __str__(self):
        return self.caption


class Test(SoftDeletionModel):
    name = models.CharField(max_length=100 )
    # student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey('school.School', on_delete=models.PROTECT, null=True)
    subject = models.ForeignKey('curriculum.Subject',on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey('setup.StudentClass', on_delete=models.CASCADE, null=True)
    type = models.CharField(choices=TEST_TYPE_CHOICES, max_length=100 )
    score = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    # term = models.PositiveIntegerField(choices=settings.TERM_CHOICES, null=True)
    session = models.CharField(max_length=10, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    # modified_by = models.ForeignKey('staff.Teacher', on_delete=models.CASCADE, null=True, blank=True)
    overall_mark = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    score = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)


