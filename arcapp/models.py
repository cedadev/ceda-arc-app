from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from arcapp.vocabs import STATUS_VALUES



class Job(models.Model):

    user = models.ForeignKey(User)
    job_id=models.IntegerField(primary_key=True)

    # Remote ID can be empty until we have submitted the job and got back id
    remote_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_VALUES.items(), default=STATUS_VALUES.NOT_SUBMITTED)

#    job_input = models.ManyToManyField(JobInput, verbose_name='Job Input')
    # jobInput_set - managed by FK relationship

    # These two can be empty
    input_file_path = models.CharField(max_length=200) 
    output_file_path = models.CharField(max_length=200)
    

class JobInput(models.Model):

    input_name = models.CharField(max_length=30, blank=False, null=False)
    input_value = models.CharField(max_length=200, blank=False, null=False)

    # Point to Job that this relates to
    job = models.ForeignKey(Job)
