from django.test import TestCase
from django.core.exceptions import ValidationError
import datetime

from arcapp.models import *

from arcapp.vocabs import VARIABLES


class ModelsTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='testuser1')

    def test_create_job_simple(self):
        Job.objects.create(user=User.objects.first())
        job = Job.objects.first()

        self.assertEqual(User.objects.first().username, job.user.username)

    def test_create_job_complex(self):
        Job.objects.create(user=User.objects.first(),
                  remote_id='32342-34324324-2324',
                  variable=VARIABLES.tas,
                  date_time=datetime.datetime(1990, 1, 1),
                  input_file_path='/files/1',
                  output_file_path='/files/2')

        job = Job.objects.first()

        self.assertEqual(job.variable, VARIABLES.tas)
        self.assertEqual(job.output_file_path, '/files/2')

    def test_create_job_fail_bad_datetime(self):
        with self.assertRaises(ValidationError) as ar:
            Job.objects.create(user=User.objects.first(), date_time=datetime.datetime.now())
