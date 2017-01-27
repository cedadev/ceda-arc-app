"""
arc_iface.py
============

Interface functions to ARC CE python client.

"""

from arcapp.vocabs import STATUS_VALUES

# Import ARC CE library


# Temporary pretend interface
import time
import random


def rndint():
    "Random wait and return 1 or 0 - i.e. True or False."
    time.sleep(1)
    x = [1,1,1,1,1,1,1,1,1,0,0,0,2,2,2,2,2]
    random.shuffle(x)
    return x[0]


def submit_job(process_id, **kwargs):
    """
    Submit a job to ARC CE.

    Return a STATUS_VALUE status.
    """
    if rndint():
        return STATUS_VALUES.IN_PROGRESS       
    else:
        return STATUS_VALUES.FAILED


def get_job_status(remote_job_id, job_id):
    """
    Get remote job details from ARC CE.

    Returns tuple:  (STATUS_VALUE, <dict_of_results>|None)
    """    
    rnd = rndint()

    if rnd == 1:
        return STATUS_VALUES.COMPLETED, {"output_path_uri": "http://me-dev.ceda.ac.uk/arc/outputs/%d/output.txt" % job_id}

    elif rnd == 2:
        return STATUS_VALUES.IN_PROGRESS, None

    else:
        return STATUS_VALUES.FAILED, None
        

