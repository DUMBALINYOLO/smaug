import datetime
import hashlib
import json
import random
import time
import uuid
import xml.etree.ElementTree as ET
from datetime import timedelta
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.signals import (post_delete, post_save, pre_delete,
                                      pre_save)
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from persons.models import CustomUser, StudentData, Subject, TutorData
from django.contrib.contenttypes.fields import GenericRelation


class Report(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 to_field='uuid', related_name='provided_reports')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 to_field='uuid', related_name='received_reports')

    message = models.TextField()

    meeting = models.ForeignKey(
        'match.Meeting', on_delete=models.CASCADE, null=True)

    created = models.DateTimeField( auto_now_add=True, editable=False)

    class Meta:
        


class Feedback(models.Model):
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='uuid', related_name='provided_feedback')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, to_field='uuid', related_name='received_feedback')

    message = models.TextField( blank=True)

    meeting = models.ForeignKey(
        'Meeting', on_delete=models.CASCADE, null=True)

    rating = models.PositiveSmallIntegerField( validators=[
        MinValueValidator(0), MaxValueValidator(5)])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['receiver', 'provider', 'meeting']]


class Request(models.Model):
    """superclass for request of a Meeting, either on Student or on Teacher side

    A User can only have one active request at a time. Also adding a created field, that makes it possible to prune old requests
    We also keep track of a list of failed_matches that should make sure the same Match isn't tried more than once
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='uuid')

    # Setting related_name to '+' --> no reverse relation from User necessary (for now)
    failed_matches = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                            related_name='+', blank=True)

    created = models.DateTimeField(auto_now_add=True)

    is_manual_deleted = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    deactivated = models.DateTimeField(null=True)

    last_poll = models.DateTimeField(default=timezone.now)

    notifications = GenericRelation('messaging.Notification')

    meeting = models.OneToOneField(
        "Meeting", on_delete=models.SET_NULL, null=True, default=None, related_name='+')

    def _successful(self):
        if self.meeting:
            return self.meeting.duration >= timedelta(minutes=5)
        return False
    _successful.boolean = True
    successful = property(_successful)

    @property
    def duration(self):
        if self.deactivated is not None:
            return self.deactivated - self.created
        else:
            return timezone.now() - self.created

    def manual_delete(self):
        self.is_manual_deleted = True
        self.save()
        self.delete()

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.deactivated = timezone.now()
            if isinstance(self, TutorRequest):
                Match.objects.filter(tutor_request__id=self.id).delete()
            if isinstance(self, StudentRequest):
                Match.objects.filter(student_request__id=self.id).delete()
            self.save()

    class Meta:
        abstract = True


class StudentRequest(Request):
    """student request always additionally includes a Subject representing the subject he/she needs help with"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class TutorRequest(Request):
    """tutorrequest can store additional data"""
    pass


class Match(models.Model):
    """Represents a Match between two requests StudentRequest, TutorRequest, or Student and Tutor

    If two matching requests StudentRequest <-> TutorRequest are found, a Match is created. Both sides have to agree to complete the Match
    Only one Match can be assigned to a request at any time. (OneToOneField)
    If the match is not successfull, the corresponding user is added to both failed_matches lists
    We keep track of the created_time and the changed_time to be able to set upper reaction time-limits on matches
    """

    student_request = models.OneToOneField(
        StudentRequest, on_delete=models.CASCADE, null=True)
    tutor_request = models.OneToOneField(
        TutorRequest, on_delete=models.CASCADE, null=True)

    student = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_match")
    tutor = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tutor_match")

    student_agree = models.BooleanField(default=False)
    tutor_agree = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)


@receiver(pre_save, sender=Match)
def on_match_change(sender, instance, **kwargs):
    if instance.student_agree and instance.tutor_agree and not hasattr(instance, 'meeting'):
        meeting = Meeting.objects.create(match=instance, name="naklar.io - Meeting")
        meeting.users.add(instance.student,
                          instance.tutor)
        meeting.tutor = instance.tutor
        meeting.student = instance.student

        # Add meeting to corresponding requests
        instance.tutor_request.meeting = meeting
        instance.student_request.meeting = meeting
        instance.tutor_request.save(update_fields=('meeting', ))
        instance.student_request.save(update_fields=('meeting', ))

        meeting.save()
        meeting.create_meeting()



@receiver(post_delete, sender=Match)
def on_match_delete(sender, instance: Match, **kwargs):
    if instance.student_agree and instance.tutor_agree:
        # TODO: do nothing? request feedback?
        pass
    else:
        # add to both requests failed matches and save --> should re-start matching
        if instance.tutor_request and not instance.tutor_request.is_manual_deleted:
            instance.tutor_request.failed_matches.add(instance.student)
            instance.tutor_request.save()
        if instance.student_request and not instance.student_request.is_manual_deleted:
            instance.student_request.failed_matches.add(instance.tutor)
            instance.student_request.save()


class Meeting(models.Model):
    """
    Meeting model represents a Meeting in BigBlueButton, using the available functions result in API calls
    """
    meeting_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    match = models.OneToOneField(Match, to_field='uuid',
                                 on_delete=models.SET_NULL, null=True, blank=True)

    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='tutor_meetings', to_field='uuid')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='student_meetings', to_field='uuid')

    name = models.CharField(_("Meeting-Name"), max_length=254)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    attendee_pw = models.CharField(max_length=120, null=True)
    moderator_pw = models.CharField(max_length=120, null=True)

    established = models.BooleanField(default=False)
    is_establishing = models.BooleanField(default=False)
    time_established = models.DateTimeField(
        , null=True, blank=True)

    ended = models.BooleanField(default=False)
    time_ended = models.DateTimeField( null=True, blank=True)

    class Meta:
        ordering = ['-time_established']

    @property
    def duration(self):
        if self.time_established:
            if self.time_ended:
                return self.time_ended - self.time_established
            else:
                return timezone.now() - self.time_established
        else:
            return None

    def build_api_request(self, call, parameters):
        pass

    def create_meeting(self):
        pass

    def _add_webhook(self):
        # TODO: Add ability to receive data from this webhook
       pass

    def end_meeting(self, close_session=True):
       pass

    def create_join_link(self, user, moderator=False):
        pass

    def get_meeting_info(self):
        pass



