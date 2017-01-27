from django.shortcuts import render, redirect
from django.http import HttpResponse
###from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from arcapp.models import *
from arcapp.forms import *


def view_logout(request):
    logout(request)
    return redirect('/')


def view_submit(request):

    if not request.user.is_authenticated() or not request.user.has_perm('arcapp.arc_ce'):
        return redirect('/login/?next=/submit/')
 
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = JobForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            # process the data in form.cleaned_data as required
            data = form.cleaned_data
            job = Job.objects.create(variable=data['variable'], date_time=data['date_time'],
                                     input_file_path=data['input_file_path'], user=request.user)
            job.save()

#            raise Exception("%s, %s" % (dir(job), job.variable))
            # redirect to a new URL:
            return redirect('/job/%s/?new=true' % job.job_id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = JobForm()

    return render(request, 'submit.html', {'form': form, 'page_title': 'Submit job'})


def view_jobs(request):
    jobs = Job.objects.all().order_by('job_id').reverse()
    return render(request, 'jobs.html', {'jobs': jobs, 'page_title': 'Jobs'})


def view_job(request, job_id):
    is_new = request.GET.get("new", False)

    job = Job.objects.get(job_id=int(job_id))
    return render(request, 'job.html', {'job': job, 'is_new': is_new, 'page_title': 'Job'})


def view_home(request):
    return render(request, 'index.html', {'page_title': 'Home'})

