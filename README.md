## 1. Setup for the workshop

To follow along with the session, you'll need access to a computer with an MPI installation, Python 3 and, the python package MPI4Py. This can be occur through your allocation on Topaz, Magnus or Nimbus. You can also install your software on your own laptop.

Below are instructions covering some of the ways that the nessecary software can be installed. It's OK to use a different installation method, just confirm that you can run the test program 'hello_world.py' as described in Section 2.

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

### Windows

With the Window's Subsystem for Linux Installed and Ubuntu chosen as your Linux distribution, follow the instructions for Linux (Ubuntu) below.

### Linux (Ubuntu): 

Using the 'apt' package manager on which you have 'superuser' privileges (this will be the case if you are using your own laptop or an instance on Nimbus).

	sudo apt install libopenmpi-dev python3-pip
	python3 -m pip install mpi4py

## 2. Testing Your Setup

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
