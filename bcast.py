import numpy as np
from mpi4py import MPI

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()

if rank == 0:
    value = 10
else:
    value = None

value = COMM.bcast(value, root=0)   # broadcast this value to every member of our communicator
print(f"value: {value} at rank {rank}.")