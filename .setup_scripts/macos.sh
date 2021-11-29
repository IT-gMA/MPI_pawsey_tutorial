#!/bin/bash
brew install open-mpi
brew install mpi4py
cd ~/
git clone https://github.com/Edric-Matwiejew/mpi_and_python.git
cd mpi_and_python
mpirun -N 4 python3 ../test/hello_world.py
