from mpi4py import MPI

print(f"Hello world from MPI rank {MPI.COMM_WORLD.rank}!")
