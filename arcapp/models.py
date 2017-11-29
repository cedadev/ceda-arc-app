from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils import timezone
UTC = timezone.UTC()

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from jasmin_arc import JobStatuses

from arcapp.vocabs import VARIABLES, DATA_FILES


STATUS_CHOICES = [(s.value, s.value) for s in JobStatuses]


class Job(models.Model):

    user = models.ForeignKey(User, verbose_name="Username")
    job_id = models.AutoField(primary_key=True, verbose_name="Job ID")

    # Remote ID can be empty until we have submitted the job and got back id
    remote_id = models.CharField(max_length=200, verbose_name="Remote Job ID")
    status = models.CharField(max_length=20, verbose_name="Job Status",
                              choices=STATUS_CHOICES, default=JobStatuses.NOT_SUBMITTED.value)

    # Inputs
    date_time = models.DateTimeField(verbose_name="DateTime", default=datetime.datetime(1990, 1, 1, 0, tzinfo=UTC))
    variable = models.CharField(max_length=20, verbose_name="Variable",
                choices=VARIABLES.items(), default=VARIABLES.tas)

    # These two can be empty
    input_file_path = models.CharField(max_length=200, choices=DATA_FILES.items(), null=True, blank=True)
    output_file_path = models.CharField(max_length=200)

    def _check_date_time(self, dt):
        """
        Validate date time.
        """
        if dt > datetime.datetime(2001, 1, 1, tzinfo=UTC):
            raise ValidationError("Date time must be between 1990 and 2000")

        if dt < datetime.datetime(1990, 1, 1, tzinfo=UTC):
            raise ValidationError("Date time must be between 1990 and 2000")

        if dt.hour not in (0, 6, 12, 18):
            raise ValidationError("Hour must be 00, 06, 12 or 18.")


    def save(self, *args, **kwargs):
        """
        Override save method to add in a call to self.full_clean, which calls self.clean,
        to validate even when created programmatically rather than via the admin form.
        """
        self._check_date_time(self.date_time)

        # Finally, if all OK, save the object
        super(Job, self).save(*args, **kwargs)

