from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD

rank = COMM.Get_rank()

array = np.empty(5, dtype = np.float64)

if rank == 0:
    array[:] = np.linspace(0,1,5)
    # Note how comm.Send and comm.Recv used to send and receive the numpy array have upper case S and R.
    COMM.Send([array, MPI.DOUBLE], dest = 1)

if rank == 1:
    # Note how comm.Send and comm.Recv used to send and receive the numpy array have upper case S and R.
    COMM.Recv([array, MPI.DOUBLE], source = 0)
    print("Array received at rank {}: {}".format(rank, array))
