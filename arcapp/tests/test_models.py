from django.test import TestCase

from arcapp.models import *


class ModelsTestCase(TestCase):

    def setUp(self):
        User.objects.create(username='testuser1')

    def test_create_job_input(self):
        Job.objects.create(user=User.objects.first())
        job = Job.objects.first()
        inp = JobInput.objects.create(input_name='input1', input_value='value1', job=job)
        self.assertEqual(JobInput.objects.first().input_name, 'input1')

    def test_create_job_simple(self):
        Job.objects.create(user=User.objects.first())
        job = Job.objects.first()

        self.assertEqual(User.objects.first().username, job.user.username)

    def test_create_job_complex(self):
        Job.objects.create(user=User.objects.first(),
                  remote_id='32342-34324324-2324',
                  input_file_path='/files/1',
                  output_file_path='/files/2')

        job = Job.objects.first()

        inp1 = JobInput.objects.create(input_name='input1', input_value='value1', job=job)
        inp2 = JobInput.objects.create(input_name='input2', input_value='value2', job=job)

        self.assertEqual(job.jobinput_set.first(), inp1)
        self.assertEqual(job.output_file_path, '/files/2')

