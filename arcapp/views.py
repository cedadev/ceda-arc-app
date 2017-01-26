from django.shortcuts import render
from django.http import HttpResponse

from arcapp.models import *
import random

def _reset_data():
    for objcls in (User, Job, JobInput):
        objcls.objects.all().delete()

    User.objects.get_or_create(username="ag")
    User.objects.get_or_create(username="fatima")

    for i in range(5):
        Job.objects.create(user=User.objects.get(username="ag"))
        job = Job.objects.last()

        JobInput.objects.create(input_name="variable", input_value="tas", job=Job.objects.first())
        JobInput.objects.create(input_name="number", input_value="%.2f" % random.randint(1,100), job=job)


def test(request):
    _reset_data()
    resp = JobInput.objects.first().job_id

    return HttpResponse("I am a test %s." % resp)


def view_jobs(request):
    _reset_data()
    jobs = Job.objects.all()
    return render(request, 'jobs.html', {'jobs': jobs, 'page_title': 'Jobs'})


def view_test2(request):
    return render(request, 'base.html', {'page_title': 'BASE'})

def view_test3(request):
    return render(request, 'test3.html', {'page_title': 'TEST3'})

