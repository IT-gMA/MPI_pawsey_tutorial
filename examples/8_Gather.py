from mpi4py import MPI
import numpy as np

'''The reverse of a SCATTER is a gather, which takes subsets of an array that are DISTRIBUTED across the ranks, 
and GATHERS them back into the full array, here, all the process gather their np arrays to the root process-0'''
COMM = MPI.COMM_WORLD

rank = COMM.Get_rank()
size = COMM.Get_size()

array_local = np.empty(2, dtype = np.float64)

array_local[:] = rank   # change every element of this array into the rank number

if rank == 0:
    array_global = np.empty(2*size, dtype = np.float64)     # rank 0's receiving buffer
else:
    array_global = None

# Must be a multiple

COMM.Gather(
        [array_local, MPI.DOUBLE],          # data/msg/buffer to be sent by the contributing process/rank
        [array_global, MPI.DOUBLE],         # data/msg/buffer to be received by the centre rank/process
        root = 0)                           # every rank/process contributes to this source rank

if rank == 0:
    # at the beginning rank 0 already has the array [.0., 0.]
    print("Rank {} receives {}".format(rank, array_global))
else:
    print("Rank {} contributes {}".format(rank, array_local))
