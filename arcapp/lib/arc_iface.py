"""
arc_iface.py
============

Interface functions to ARC CE python client.

"""

# Standard library imports
import os
import time

# Local imports
from arcapp.vocabs import STATUS_VALUES

# Import ARC CE library
from arcapp.lib import arclib


# Location of wrapper script
JOB_FILES_DIR = "/usr/local/arc-app/job_files"

if not os.path.isdir(JOB_FILES_DIR):
    os.makedirs(JOB_FILES_DIR)


def submit_job(job_id, executable, *arguments, **kwargs):
    """
    Submit a job to ARC CE.

    :param job_id: string (local job id)
    :param executable: path to executable
    :param *arguments: list of arguments (interpreted as strings) starting with main script path.
    :param **kwargs (can include input_file_path: path to an input file to provide as input to process.)

    :returns: tuple of (STATUS_VALUE, job_id|False)
    """
#    if kwargs.has_key("input_file_path"):
#        raise NotImplementedError

    job_file_path = os.path.join(JOB_FILES_DIR, "job_{0}.jsdl".format(job_id)) 

    arclib.write_job_file(job_file_path, executable, arguments)

    job_id = arclib.submit_job(job_file_path)

    if not job_id:
       return STATUS_VALUES.FAILED, False 

    return STATUS_VALUES.IN_PROGRESS, job_id


def _map_arc_status(status):
    "Maps ARC status to local app status."
    status == status.lower().strip()

    if not status or status == 'failed':
        return STATUS_VALUES.FAILED
    elif status != arclib.ARC_FINISHED_STATUS:
        return STATUS_VALUES.IN_PROGRESS
    else: 
        return STATUS_VALUES.COMPLETED
 

def get_arc_job_status(remote_job_id, job_id):
    """
    Get remote job details from ARC CE.

    :param remote_job_id (string): remote (ARC) job ID.
    :param job_id (string): local job ID.
    :return: tuple of (STATUS_VALUE, <dict_of_results>|None)
    """    
    job_status = arclib.get_job_status(remote_job_id)

    status = _map_arc_status(job_status)
    return status, {"output_path_uri": "http://me-dev.ceda.ac.uk/arc/outputs/%d/output.txt" % job_id}
