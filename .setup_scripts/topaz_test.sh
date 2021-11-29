#!/bin/bash
#salloc -n 8 -p gpuq
module load singularity
srun -n 8 singularity exec ../../mpi4py_latest.sif python3 ../test/hello_world.py
