
from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD

rank = COMM.Get_rank()


if rank == 0:
    x = 10
else:
    x = 0
    print("x = {}".format(x))

y = COMM.bcast(x, root = 0)     # Sends to all other processes

if rank != 0:
    print("Rank {}: y = {}".format(rank, y))
