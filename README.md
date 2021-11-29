## 1. Setup for the workshop

To follow along with the session, you'll need access to a computer with an MPI installation, Python 3 and, the python packages mpi4py, numpy and matplotlib. This can be occur through your allocation on Topaz, Magnus or Nimbus. You can also install your software on your own laptop.

Below are instructions covering some of the ways that the nessecary software can be installed. It's OK to use a different installation method, just confirm that you can run the test program 'hello_world.py' as described in Section 1.2.

### Magnus Users

Python 3 and MPI4Py are available as modules.

### Topaz Users

Build the singularity container 'mpi4py_latest.sif'.

	mkdir $MYGROUP/mpi_workshop
	cd $MYGROUP/mpi_workshop
	module load singularity
	singularity pull docker://dhna/mpi4py

### MacOS 

With the homebrew package manager installed:

	brew install open-mpi
	brew install mpi4py
	pip3 install numpy matplotlib

### Windows

With the Window's Subsystem for Linux Installed and Ubuntu chosen as your Linux distribution, follow the instructions for Linux (Ubuntu) below.

### Linux (Ubuntu): 

Using the 'apt' package manager on which you have 'superuser' privileges (this will be the case if you are using your own laptop or an instance on Nimbus).

	sudo apt install libopenmpi-dev python3-pip
        python3 -m pip install setuptools cython 
        python3 -m pip install numpy mpi4py matplotlib

## 1.2. Testing Your Setup

### Magnus

	cd $MYGROUP
	git clone https://github.com/Edric-Matwiejew/mpi_and_python.git
	cd mpi_and_python
	salloc -N 1 -n 24 -p workq
	module load python mpi4py
	srun -N 1 -n 24 python test/hello_world.py
  
### Topaz
  
	cd $MYGROUP/mpi_workshop
	git clone https://github.com/Edric-Matwiejew/mpi_and_python.git
	cd mpi_and_python
	salloc -n 4 -p gpuq
	module load singularity
	srun -n 4 singularity exec ../mpi4py_latest.sif python3 test/hello_world.py
    
### Ubuntu (Windows Subsystem for Linux) or MacOS

	cd ~/
	git clone https://github.com/Edric-Matwiejew/mpi_and_python.git
	cd mpi_and_python
	mpirun -N 4 python3 test/hello_world.py
  
In each instance, the final command should output in multiple instance of "Hello world from MPI rank #!", where # is an integer. 

## 2. Workshop Exercises 

### 2.1 Send and Recieve

The program shown below contains two bugs, identify the errors and correct them so the code executes successfully.

The program is designed for two MPI processes and should print "[0,0]" from rank 1 on completion.

```python

from mpi4py import MPI
import numpy as np

COMM = MPI.COMM_WORLD
rank = COMM.Get_rank()

if rank == 0:
    send_array = np.array(2*[rank], dtype = np.int)

if rank == 0:
    COMM.Send([send_array, MPI.INT], dest = 1)
else:
    COMM.Recv([recv_array, MPI.INT], source = 1)

    print(recv_array)
```

### 2.2 Scatter

Starting with the following 2-dimensional array at rank 0:

```python
n = 3
COMM = MPI.COMM_WORLD

rank = COMM.Get_rank()
size = COMM.Get_size()

if rank == 0:
    A = np.zeros((size*n, size*n), dtype = np.float64)
    for i in range(n*size):
        A[i,:] = i
```

Write an MPI program that carries our the following steps:

1. At rank 0, partition a into `size` row-wise partitions with `n` rows each and store the partitions in a numpy array of dimensions `(size, n, size*n)`.

3. Use Scatter to send an `(n, size*n)` row partion from rank 0 to each process in the communicator. Recieve this partition into an `(n, size*n)` NumPy array `local_array`.

4. At each rank, compute `local_array  += rank`, and print the results using:

```python
print(local_array,'\n', flush = True)
```

With `n=3` and 3 MPI processes the expected output is:

Rank 0:

```
[[0 0 0 0 0 0 0 0 0]
[1 1 1 1 1 1 1 1 1]
[2 2 2 2 2 2 2 2 2]]
```

Rank 1:
```

[[4 4 4 4 4 4 4 4 4]
[5 5 5 5 5 5 5 5 5]
[6 6 6 6 6 6 6 6 6]]
```

Rank:2

```
[[ 8  8  8  8  8  8  8  8  8]
[ 9  9  9  9  9  9  9  9  9]
[10 10 10 10 10 10 10 10 10]]
```


### 2.3 Communication on a 2D Grid

Adding on to your code from 2, implement a single pass of the communication pattern:

IMAGE HERE

Store incoming values from the 'above' rank in an a NumPy array `upper`, and those coming from a 'below' rank in the NumPy array `lower`.

The code below defines `lower` and `upper`, and partitally implements communication of the `upper` values. Use this as a starting point.

```python
if rank > 0:
    upper = np.empty(size*n, dtype = np.float64)
    
if rank < size - 1:
    lower = np.empty(size*n, dtype = np.float64)
    
if rank == 0:
    COMM.Send([local_array[-1,:], MPI.DOUBLE], dest = 1)
    
if rank > 0 and rank < size - 1:
    COMM.Recv([upper, MPI.DOUBLE], source = rank - 1)
    COMM.Send([local_array[-1,:], MPI.DOUBLE], dest = rank + 1)
```

For each MPI process, at the values of `lower` and `upper` to the rows of `local_array`, as shown below.

```python

for i in range(local_array.shape[0]):
    local_array[i,:] += lower
    local_array[i,:] += upper
```

If only `lower` or `upper` were sent to the MPI process, add them only.

```python
print(local_array, '\n', flush = True)
```

For `n=3` and 3 MPI processes the expected output is:

Rank 0:

```
[[4 4 4 4 4 4 4 4 4]
[5 5 5 5 5 5 5 5 5]
[6 6 6 6 6 6 6 6 6]]
```

Rank 1:

```
[[14 14 14 14 14 14 14 14 14]
[15 15 15 15 15 15 15 15 15]
[16 16 16 16 16 16 16 16 16]]
```

Rank:2

```
[[14 14 14 14 14 14 14 14 14]
[15 15 15 15 15 15 15 15 15]
[16 16 16 16 16 16 16 16 16]]
```

### 2.4 Broadcast

Take the average of the all of the elements in the `local_array` and store the averages in an array of length `size` called `averages`. Use `Gather` to collect the averages to `rank=0`.

Use the code snippet below to calculate the sum of the averages and then broadcast the sum to each process in `COMM_WORLD`. 

```python
if rank == 0:
    average_sum = 0
    for av in averages:
        average_sum += av
else:
    average_sum = None

average_sum = COMM.bcast(average_sum, root = 0)

print(average_sum, flush = True)
```

### 2.5 Gather

Use `COMM.Gather` to gather `local_array` to the `rank = 0`. At rank = 0, reshape the the recieved array into a matrix of dimensions `(2, 2)` using the NumPy `reshape` function.

### 2.6 Putting it All Together: John Conway's Game of Life
