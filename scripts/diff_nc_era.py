"""
diff_nc_era.py
==============

Simple processing function to demonstrate ARC CE interactions:

NAME: diff_nc_era

FUNCTIONALITY: Difference an ERA-Interim file ("open" data in the CEDA archive) from a 
               reference file (in the GWS) and write a text file (to the GWS) summarising the differences.

Inputs: 
    variable:         one of 'tas', 'u-wind', 'v-wind'
    date_time:        a date/time between 1990 and 2000, the time of day must be 00:00, 06:00, 12:00 or 18:00.
    input_file:       an uploaded text file that will contain a constant (number) to be added to the input data
                      before differencing. 

Reads: 
    archive_file:     a file in the ERA-Interim dataset (based on the inputs given) GWS file
    reference_file:   a reference file to be subtracted from the archive_file (this is actually just the 1980-01-01 00:00 
                      data from ERA-Interim).
    input_file:       to get a single number (if uploaded/provided by the user).

Outputs:
    output_file:      Path to output file containing three lines of text:
                        1. User inputs
                        2. File paths used
                        3. Minimum and Maximum values of the diff.

Usage:
------

    diff_nc_era.py <variable> <date_time> <output_file> [<input_file>]

Where:
    variable:         one of 'tas', 'u-wind', 'v-wind'
    date_time:        a date/time between 1990 and 2000, the time of day must be 00:00, 06:00, 12:00 or 18:00.
    output_file:      path to write output to.
    input_file:       an uploaded text file that will contain a constant (number) to be added to the input data
                      before differencing.

""" 

# Imports
import os
import sys
import re
import shutil
import datetime
from dateutil import parser

import cf

REF_TIME = parser.parse("1980-01-01T00:00:00")
PATH_TMPL = "/badc/ecmwf-era-interim/data/gg/as/%(year)04d/%(month)02d/%(day)02d/ggas%(year)04d%(month)02d%(day)02d%(hour)02d00.nc"
NUM_REGEX = re.compile("^\d+\.?\d*$")


# Get ARC_PROC_BASEDIR environment variable or fail
try:
    BASEDIR = os.environ["ARC_PROC_BASEDIR"]
except:
    raise Exception("Must set $ARC_PROC_BASEDIR environment variable before running.")


def validate_inputs(variable, date_time, input_file):
    errs = []

    KNOWN_VARS = {"tas": "T2", "u-wind": "U10", "v-wind": "V10"}
    if variable not in KNOWN_VARS:
        errs.append("Variable not known, must be one of: %s" % sorted(KNOWN_VARS.keys()))
  
    try:
        dt = parser.parse(date_time)
    except:
        errs.append("Could not parse date/time from string: %s" % date_time)

    constant = 0
    if input_file:
        if not os.path.isfile(input_file) or not NUM_REGEX.match(open(input_file).read()):
            errs.append("Could not read number from input file: %s" % input_file)
        else:
            constant = float(open(input_file).read())

    if errs:
        raise Exception("Errors validating inputs: %s" % "; ".join(errs))

    return KNOWN_VARS[variable], dt, constant


def get_nc_path(date_time):
    keys = ("year", "month", "day", "hour")
    d = dict([(key, getattr(date_time, key)) for key in keys])
    return PATH_TMPL % d


def get_var(path, varid):
    f = cf.read(path, select='ncvar%%%s' % varid, squeeze=True)
    return f


def _package_outputs(*output_files):
    """
    Packages up all outputs into `outputs.zip` and copies them to the 
    LSF job directory (if the $LSB_OUTDIR environment variable exists).

    :param output_files [a list of file paths to zip up]
    :return: boolean (True if output zip file copied to external directory).
    """
    # Check if directory is known, if not return False
    job_dir = os.environ.get("LSB_OUTDIR", None)
    if not job_dir:
        return False
            
    # Get common directory to zip from
    if len(output_files) == 1:
        common_dir = os.path.dirname(output_files[0])
    else:
        common_dir = os.path.commonprefix(output_files)

    rel_paths = [fpath.replace(common_dir + "/", "") for fpath in output_files]    
    out_zip = "outputs.zip"

    # Zip up outputs
    os.system("cd {} ; zip -r {} {}".format(common_dir, out_zip, " ".join(rel_paths)))
    
    # Copy outputs to job dir
    shutil.copy(os.path.join(common_dir, out_zip), job_dir)

    return True  

    
def run_diff_nc_era(variable, date_time, output_file, input_file=None):
    """
    Run the 'diff_nc_era' process.
    """
    varid, date_time, constant = validate_inputs(variable, date_time, input_file)

    ref_file = get_nc_path(REF_TIME)
    ref_var = get_var(ref_file, varid)

    test_file = get_nc_path(date_time)
    test_var = get_var(test_file, varid)

    result = test_var + constant - ref_var

    mn = float(result.min().squeeze())
    mx = float(result.max().squeeze())

    output = """INPUTS: variable: %s; date_time: %s; constant: %s; 
FILE PATHS: Reference file: %s; User-selected file: %s; User-input file: %s; 
RESULTS: Min: %.6f; Max: %.6f; 
""" % (variable, date_time, constant, ref_file, test_file, input_file, mn, mx)

    print "OUTPUTS:\n{0}".format(output)

    with open(output_file, "w") as writer:
        writer.write(output)
 
    print "Wrote output to: %s" % output_file

    _package_outputs(output_file)
    return output_file


def test():
    output_dir = "%s/jobs/0000/outputs" % BASEDIR
    output_file = os.path.join(output_dir, "output.txt")

    if not os.path.isdir(output_dir): os.makedirs(output_dir)

    output_file = run_diff_nc_era(variable="tas", date_time="1999-09-09T00:00:00", 
                        output_file=output_file,
                        input_file="%s/jobs/0000/uploads/input.txt" % BASEDIR)
    print open(output_file).read()


if __name__ == "__main__":

    TEST = False
#    TEST = True

    if TEST:
        test()
    else:
        args = sys.argv[1:]

        if len(args) < 3:
            print "Please provide arguments: <variable> <date_time> <output_file> [<input_file>]"
        else:
            variable, date_time, output_file = args[:3]
            input_file = None

            if len(args) > 3: 
                input_file = args[3] 
 
            print run_diff_nc_era(variable, date_time, output_file, input_file)
