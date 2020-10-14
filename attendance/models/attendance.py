from django.db import models
from basedata.constants import ATTENDANCE_STATUS_CHOICES
from basedata.models import SoftDeletionModel


class StudentTimeSheet(SoftDeletionModel):
    date = models.DateField()
    recorded_by = models.ForeignKey(
                            'persons.Teacher', 
                            on_delete=models.SET_NULL, 
                            related_name='registers', 
                            null=True
                        )
    class_  = models.ForeignKey(
                            'setup.StudentClass',
                            blank=True,
                            null=True,
                            related_name = 'attendances'
                        )
    school = models.ForeignKey(
                            'setup.School',
                            blank=True,
                            null=True,
                            related_name = 'timesheets'
                        )

    def save(self, *args, **kwargs):
        if not self.recorded_by:
            self.recorded_by = self.class_.class_teacher
        if not self.school:
            self.school = self.class_.school
        super(StudentTimeSheet, self).save(*args, **kwargs)


    @property
    def attendances(self):
        return self.lines.prefetch_related(
                                    'student'
                                )
    



class AttendanceLine(SoftDeletionModel):
    timesheet = models.ForeignKey(
                    'StudentTimeSheet', 
                    on_delete=models.SET_NULL, 
                    null=True,
                    related_name= 'lines'
                )
    student = models.ForeignKey(
                            'persons.Student',
                            blank=True,
                            null=True,
                            related_name = 'attendances'
                        )
    status = models.CharField(max_length=50, choices=ATTENDANCE_STATUS_CHOICES)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)



