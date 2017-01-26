# Forms

from django.forms import ModelForm
from arcapp.models import Job


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['variable', 'date_time', 'input_file_path']


