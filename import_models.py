import django
django.setup()

from arcapp.models import *
print "Counts..."
print "Jobs:", Job.objects.count()
print "JobInputs:", JobInput.objects.count()
