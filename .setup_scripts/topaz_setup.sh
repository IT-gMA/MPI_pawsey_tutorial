#!/bin/bash

mkdir $MYGROUP/mpi_workshop
cd $MYGROUP/mpi_workshop
module load singularity
singularity pull docker://dhna/mpi4py
cd $MYGROUP/mpi_workshop
git clone https://github.com/Edric-Matwiejew/mpi_and_python.git
cd mpi_and_python
salloc -n 2 -p gpuq
