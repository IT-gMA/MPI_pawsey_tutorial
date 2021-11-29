from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np

size=MPI.COMM_WORLD.size
rank=MPI.COMM_WORLD.rank
num_points=60
sendbuf=[]
root=0
dx=1.0/(num_points-1)
from numpy import r_
j=np.complex(0,1)
rows_per_process=int(num_points/size)
max_iter=1000000
num_iter=0
total_err=1
err_list = np.empty(size, dtype = np.float64)
target_err = 1e-6

def numpyTimeStep(u,dx,dy):
    dx2, dy2 = dx**2, dy**2
    dnr_inv = 0.5/(dx2 + dy2)
    u_old=u.copy()
    # The actual iteration
    u[1:-1, 1:-1] = ((u[0:-2, 1:-1] + u[2:, 1:-1])*dy2 +
                     (u[1:-1,0:-2] + u[1:-1, 2:])*dx2)*dnr_inv
    v = (u - u_old).flat
    return u,np.sqrt(np.dot(v,v))


if rank==0:
    m=np.zeros((num_points,num_points),dtype=float)
    pi_c=np.pi
    x=r_[0:2*pi_c:num_points*j]
    m[0,:]=np.sin(x)
    m[num_points-1,:]=np.sin(x)
    m[:,0]=np.sin(x)
    m[:,-1]=np.sin(x)
    l=np.array([ m[i*rows_per_process:(i+1)*rows_per_process,:] for i in range(size)])
    sendbuf=l

my_grid = np.empty((rows_per_process, num_points), dtype = np.float64)

# caps un caps
MPI.COMM_WORLD.Scatter(
        [sendbuf, MPI.DOUBLE],
        [my_grid, MPI.DOUBLE],
        root = 0)

if rank > 0:
    row_above = np.empty((1, num_points), dtype = np.float64)
if rank < size - 1:
    row_below = np.empty((1, num_points), dtype = np.float64)


# tags
# row_above: rank of sender * 2
# row_below: rank of sender * 2 + 1

total_err = np.inf
while num_iter <  max_iter:

    if total_err < target_err:
        break



    if rank == 0:


        MPI.COMM_WORLD.Isend(
                [my_grid[-1,:], MPI.DOUBLE],
                dest = 1,
                tag = rank * 2)

    if rank > 0 and rank< size-1:

        #print(rank, my_grid[-1,:], flush = True)


        MPI.COMM_WORLD.Irecv(
                [row_above, MPI.DOUBLE],
                source = rank - 1,
                tag = (rank - 1) * 2)

        MPI.COMM_WORLD.Isend(
                [my_grid[-1,:], MPI.DOUBLE],
                dest = rank + 1,
                tag = rank * 2)

    if rank==size-1:
        #print(rank, my_grid[0,:], flush = True)

        MPI.COMM_WORLD.Irecv(
                [row_above, MPI.DOUBLE],
                source = rank - 1,
                tag = (rank - 1)* 2)

        MPI.COMM_WORLD.Isend(
                [my_grid[0,:], MPI.DOUBLE],
                dest = rank - 1,
                tag = rank * 2 + 1)

    #print(rank, flush = True)
    if rank > 0 and rank< size-1:

        MPI.COMM_WORLD.Irecv(
                [row_below, MPI.DOUBLE],
                source = rank + 1,
                tag = (rank + 1) * 2 + 1)

        MPI.COMM_WORLD.Isend(
                [my_grid[0,:], MPI.DOUBLE],
                dest = rank - 1,
                tag = rank * 2 + 1)

    if rank==0:

        MPI.COMM_WORLD.Irecv(
                [row_below, MPI.DOUBLE],
                source = 1,
                tag = 3)



    MPI.COMM_WORLD.Barrier()
    #print(rank, flush = True)

    if rank >0 and rank < size-1:

        row_below.shape=(1,num_points)
        row_above.shape=(1,num_points)

        u,err =numpyTimeStep(r_[row_above,my_grid,row_below],dx,dx)

        my_grid=u[1:-1,:]


    #print(rank, flush = True)
    if rank==0:

        row_below.shape=(1,num_points)
        u,err=numpyTimeStep(r_[my_grid,row_below],dx,dx)
        my_grid=u[0:-1,:]


    #print(rank, flush = True)
    if rank==size-1:

        row_above.shape=(1,num_points)
        u,err=numpyTimeStep(r_[row_above,my_grid],dx,dx)
        my_grid=u[1:,:]


    #print(rank, '153', flush = True)

    if num_iter%500==0:

        MPI.COMM_WORLD.Gather(
                [err, MPI.DOUBLE],
                [err_list, MPI.DOUBLE],
                root)

        if rank==0:
            total_err = 0
            for a in err_list:
                total_err=total_err+np.math.sqrt( a**2)
            total_err=np.math.sqrt(total_err)
            print("iterations: %i"%num_iter, "error: %f"%total_err, flush= True)

        total_err = MPI.COMM_WORLD.bcast(
                total_err,
                root)
    #print(num_iter, rank, total_err)

    MPI.COMM_WORLD.Barrier()
    num_iter=num_iter+1

MPI.COMM_WORLD.Barrier()
#print(my_grid.shape, rank)

recvbuf=MPI.COMM_WORLD.gather(my_grid,root)
if rank==0:
    sol=np.array(recvbuf)
    sol=sol.reshape([num_points,num_points])
    print(num_iter)
    #print(sol)
    plt.matshow(sol)
    plt.savefig('show')
