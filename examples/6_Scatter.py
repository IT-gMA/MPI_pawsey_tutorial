from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD

rank = COMM.Get_rank()
size = COMM.Get_size()

array_local = np.empty(2, dtype = np.float64)

if rank == 0:
    array_global = np.linspace(0,25,2*size)
    print(array_global,flush = True)
else:
    array_global = None

COMM.Scatter(
        [array_global, MPI.DOUBLE],     # data to be distributed
        [array_local, MPI.DOUBLE],      # received buffer/msg/data
        root = 0)                       # the rank/process it receives the data from

print("Rank {} receives {}".format(rank, array_local))



