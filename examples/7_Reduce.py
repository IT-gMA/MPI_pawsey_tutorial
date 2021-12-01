from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD

rank = COMM.Get_rank()
size = COMM.Get_size()

# create an array of length equal to the nºprocesses w every element being the process number
array_local = np.array(size*[rank], dtype = np.float64)

if rank == 0:
    array_reduced = np.empty(size, dtype = np.float64)  # Assign this to the root
else:
    array_reduced= None

# Must be a multiple

COMM.Reduce(
        [array_local, MPI.DOUBLE],      # all the component data
        [array_reduced, MPI.DOUBLE],    # display result at the root
        op = MPI.SUM,                   # chosen operations
        root = 0)                       # where the result resides

if rank == 0:
    print("Reduced array at root = {}".format(array_reduced))
else:
    print("Rank {}, data {}".format(rank, array_local))



