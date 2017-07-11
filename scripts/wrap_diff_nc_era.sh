#!/bin/bash

WD=/group_workspaces/jasmin/cedaproc/arc_ce_test
export ARC_PROC_BASEDIR=$WD/outputs

variable=$1
datetime=$2

last_job_number=$(ls $WD/outputs/jobs | tail -1)
next_job_number=`expr $(echo $last_job_number | sed 's/^0*//') + 1`

output_dir=$WD/outputs/jobs/$(printf "%04d" $next_job_number)/outputs
mkdir -p $output_dir
output_file=${output_dir}/output.txt

cmd="/usr/bin/python2.7 $WD/ceda-arc-app/scripts/diff_nc_era.py $variable $datetime $output_file"

echo "Running job: $cmd"
$cmd

echo "Done"
