from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

from arcapp.models import *
from arcapp.forms import *
from arcapp.lib import arc_iface
from arcapp.vocabs import STATUS_VALUES


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

            # Submit job to ARC CE
            executable = "/group_workspaces/jasmin/cedaproc/arc_ce_test/ceda-arc-app/scripts/wrap_diff_nc_era.sh"
            remote_args = [job.variable, job.date_time.isoformat()]

            status, remote_id = arc_iface.submit_job(job.job_id, executable, *remote_args, 
                                                     input_file_path=job.input_file_path)

            job.status = status

            if status != STATUS_VALUES.FAILED:
                job.remote_id = remote_id
            
            job.save()

            # Capture submit status
            submit_status = job.status

            # redirect to a new URL:
            return redirect('/job/%s/?submit_status=%s' % (job.job_id, submit_status.lower()))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = JobForm()

    return render(request, 'submit.html', {'form': form, 'page_title': 'Submit job'})


def view_jobs(request):
    jobs = Job.objects.all().order_by('job_id').reverse()
    return render(request, 'jobs.html', {'jobs': jobs, 'page_title': 'Jobs'})


def view_job(request, job_id):
    job_id = int(job_id)
    job = Job.objects.get(job_id=job_id)

    # Provide extra info if job completed
    status, resp = arc_iface.get_arc_job_status(job.remote_id, job_id)
    job.status = status

    if status == STATUS_VALUES.COMPLETED:
        download_url = resp["output_path_uri"]
        job.output_file_path = download_url
    else:
        download_url = None
 
    job.save()
  
    # Check GET args to update messages to user 
    submitted = just_failed = failed = False 

    submit_status = request.GET.get("submit_status", False) 
    if submit_status == STATUS_VALUES.FAILED:
        just_failed = True

    failed = status == STATUS_VALUES.FAILED 

    if not failed and submit_status == STATUS_VALUES.IN_PROGRESS: 
        submitted = True 

    return render(request, 'job.html', {'job': job, 'failed': failed, 'submitted': submitted, 'just_failed': just_failed,
                             'download_url': download_url, 'page_title': 'Job'}) 


def view_home(request): 
    return render(request, 'index.html', {'page_title': 'Home'}) 
