import django
django.setup()

from arcapp.models import *
print "Counts..."
print "Jobs:", Job.objects.count()

print "Users:", User.objects.count()
user = User.objects.get(username="eguser2")
print "User: %s" % user.username
print "Is active, is staff, has permissions for arc ce?", user.is_active, user.is_staff, user.has_perm("arcapp.arc_ce")

for job in Job.objects.all():
    print "JOB", job.job_id, job.user.username, job.variable, job.date_time
