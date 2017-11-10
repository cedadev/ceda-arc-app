import os.path

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout

from jasmin_arc import ArcInterface, JOB_STATUSES

from arcapp.models import *
from arcapp.forms import *

from arcproj.settings import OUTPUTS_DIR

arc_api = ArcInterface()

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

            remote_id = arc_api.submit_job(executable, *remote_args,
                                           input_file_path=job.input_file_path)

            job.status = arc_api.get_job_status(remote_id)

            if job.status != JOB_STATUSES.FAILED:
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
    status = arc_api.get_job_status(job.remote_id)
    job.status = status

    if status == JOB_STATUSES.COMPLETED:
        download_url = "/download/{0}/".format(job_id)
        job.output_file_path = download_url
    else:
        download_url = None

    job.save()

    # Check GET args to update messages to user
    submitted = just_failed = failed = False

    submit_status = request.GET.get("submit_status", False)
    if submit_status == JOB_STATUSES.FAILED:
        just_failed = True

    failed = status == JOB_STATUSES.FAILED

    if not failed and submit_status == JOB_STATUSES.IN_PROGRESS:
        submitted = True

    return render(request, 'job.html', {'job': job, 'failed': failed, 'submitted': submitted, 'just_failed': just_failed,
                             'download_url': download_url, 'page_title': 'Job'})


def view_home(request):
    return render(request, 'index.html', {'page_title': 'Home'})


def download(request, job_id):
    remote_id = Job.objects.get(job_id=job_id).remote_id
    path_to_file = '{0}/{1}/outputs.zip'.format(OUTPUTS_DIR, remote_id)

    if os.path.isfile(path_to_file):
        arc_api.save_job_outputs(remote_id, path_to_file)

    zip_file = open(path_to_file, 'r')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'outputs.zip'
    return response
