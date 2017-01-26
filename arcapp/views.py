from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from arcapp.models import *
from arcapp.forms import *

import random


def view_submit(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JobForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            most_recent_job = Job.objects.last()
            return HttpResponseRedirect('/job/%s/?new=true' % most_recent_job.job_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = JobForm()

    return render(request, 'submit.html', {'form': form, 'page_title': 'Submit job'})

def _reset_data():
    for objcls in (Job,):
        objcls.objects.all().delete()

    User.objects.get_or_create(username="ag")
    User.objects.get_or_create(username="fatima")

    for i in range(5):
        Job.objects.create(user=User.objects.get(username="ag"))


def test(request):
    _reset_data()
    resp = Job.objects.first().job_id
    return HttpResponse("I am a test %s." % resp)


def view_jobs(request):
    _reset_data()
    jobs = Job.objects.all().order_by('job_id').reverse()
    return render(request, 'jobs.html', {'jobs': jobs, 'page_title': 'Jobs'})

def view_job(request, job_id):
    _reset_data()
    is_new = request.GET.get("new", False)

    job = Job.objects.get(job_id=int(job_id))
    return render(request, 'job.html', {'job': job, 'is_new': is_new, 'page_title': 'Job'})


def view_home(request):
    return render(request, 'index.html', {'page_title': 'Home'})

