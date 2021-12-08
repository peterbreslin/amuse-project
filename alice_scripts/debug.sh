#!/bin/bash
#SBATCH --job-name=debug
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --mail-user="pbreslin@tcd.ie"
#SBATCH --mail-type="ALL"
#SBATCH --time=1:00:00
#SBATCH --partition=testing
#SBATCH -N 1 -n 1

# load modules (assuming you start from the default environment)
# we explicitly call the modules to improve reproducibility
# in case the default settings change
module load AMUSE/13.1.0-foss-2018a-Python-3.6.4
export OMPI_MCA_rmaps_base_oversubscribe=yes

echo "[$SHELL] #### Starting Python test"
echo "[$SHELL] ## This is $SLURM_JOB_USER and this job has the ID $SLURM_JOB_ID"
# get the current working directory
export CWD=$(pwd)
echo "[$SHELL] ## current working directory: "$CWD

# Run the file
echo "[$SHELL] ## Run script"
python3 debug_test.py
echo "[$SHELL] ## Script finished"
