from django.db import models
from django.conf import settings
from basedata.constants import PYSCHOMOTOR_CHOICES, TERM_CHOICES
from basedata.models import SoftDeletionModel



class ReportBatch(SoftDeletionModel):
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, null=True)
    term = models.CharField(choices=TERM_CHOICES, max_length=100 )
    session = models.CharField(max_length=15, null=True, blank=True)
    school_resume_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return 'Batch/%s/%s' % (self.session, self.term)

    def get_term(self):
        terms = {1:'First Term', 2:'Second Term', 3:'Third Term'}
        return terms[self.term].upper()
    
    class Meta:
        verbose_name = u'Report Batch'
        verbose_name_plural = u'Report Batches'


class Report(SoftDeletionModel):
    batch = models.ForeignKey(ReportBatch, on_delete=models.SET_NULL, null=True)
    # student = models.ForeignKey('students.Student', on_delete=models.CASCADE, null=True)
    # student_class = models.ForeignKey('institutions.StudentClass', on_delete=models.CASCADE, null=True)
    form_teacher_remark = models.TextField(null=True, blank=True)
    head_remark = models.TextField('Principal/Headmaster Remark', null=True, blank=True)
    attentiveness = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    attendance = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    hardworking = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    neatness = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    reliability = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    games = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    craft = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    punctuality = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    relationship_with_others = models.PositiveIntegerField(choices=PYSCHOMOTOR_CHOICES, null=True, blank=True)
    verified = models.BooleanField(default=False)
    promoted_to = models.ForeignKey('setup.StudentClass', on_delete=models.CASCADE, related_name='promoted_class', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # modified_by = models.ForeignKey('staff.Teacher', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Report of %s in batch: %s" % (self.student,self.batch)

    def verification(self):
        verification = {1: 'Verified', 0: 'Unverified'}
        return verification[self.verified]

    class Meta:
        ordering = ('-date_created', '-date_modified')
    
    def save(self, **kwargs):
        if self.promoted_to:
            self.student.student_class = self.promoted_to
            self.student.save()
        super(Report, self).save(**kwargs)


class BroadSheet(models.Model):
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(ReportBatch, on_delete=models.CASCADE, null=True)
    student_class = models.ForeignKey('setup.StudentClass', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    # modified_by = models.ForeignKey('staff.Teacher', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Broadsheet for %s in %s" % (self.student_class, self.batch)
    
    


