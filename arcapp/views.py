import os.path
import string
import random
import shutil

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.conf import settings

from jasmin_arc import ArcInterface, JobStatuses

from arcapp.models import Job
from arcapp.forms import JobForm


arc_api = ArcInterface(settings.JASMIN_ARC_CONFIG)


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
            input_files = []
            if job.input_file_path:
                input_files.append(job.input_file_path)

            remote_id = arc_api.submit_job(executable, args=remote_args, input_files=input_files)
            job.status = arc_api.get_job_status(remote_id).value

            if job.status != JobStatuses.FAILED.value:
                job.remote_id = remote_id

            job.save()

            # redirect to a new URL:
            return redirect('/job/%s/?submit_status=%s' % (job.job_id, job.status))

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
    job.status = arc_api.get_job_status(job.remote_id).value

    if job.status in (JobStatuses.COMPLETED.value, JobStatuses.FAILED.value):
        download_url = "/download/{0}/".format(job_id)
        job.output_file_path = download_url
    else:
        download_url = None

    job.save()

    # Check GET args to update messages to user
    submit_status = request.GET.get("submit_status", False)
    failed = (job.status == JobStatuses.FAILED.value)
    just_failed = (submit_status == JobStatuses.FAILED.value)
    submitted = (not failed and submit_status == JobStatuses.IN_PROGRESS.value)
    return render(request, 'job.html', {'job': job, 'failed': failed, 'submitted': submitted,
                                        'just_failed': just_failed, 'download_url': download_url,
                                        'page_title': 'Job'})


def view_home(request):
    return render(request, 'index.html', {'page_title': 'Home'})


def download(request, job_id):
    remote_id = Job.objects.get(job_id=job_id).remote_id
    output_dir = arc_api.save_job_outputs(remote_id)

    # Package all outputs into a zip
    r = "".join(random.choice(string.letters) for _ in range(16))
    zip_filename = shutil.make_archive("/tmp/outputs_{}".format(r), "zip",
                                       os.path.join(output_dir, os.path.pardir),
                                       os.path.basename(output_dir))

    response = None
    with open(zip_filename) as zipfile:
        response = HttpResponse(zipfile, content_type="application/force-download")

    response["Content-Disposition"] = "attachment; filename='{}'".format(os.path.basename(zip_filename))

    # Delete output directory and zip file
    os.unlink(zip_filename)
    shutil.rmtree(output_dir)

    return response
