# Works on Ubuntu 18.04
# The version pf gmsh will likely have to change
# The gmsh in standard repo is old
cd

sudo apt-get install m4 make autoconf automake gcc g++ git findutils

sudo apt-get install libgsl-dev petsc-dev slepc-dev

git clone https://github.com/seamplex/milonga/
cd milonga
./autogen.sh
./configure
make
make check
sudo make install

sudo apt-get install gnuplot paraview pandoc



sudo apt-get remove python*

sudo apt-get install python3.6 python-pip3

wget http://gmsh.info/bin/Linux/gmsh-4.5.1-Linux64.tgz

tar -xvzf gmsh-4.5.1-Linux64.tgz

echo 'export PATH="/home/kevin/gmsh-4.5.1-Linux64/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="/home/$USER/milonga:$PATH"' >> ~/.bashrc

export PATH="/home/kevin/gmsh-4.5.1-Linux64/bin:$PATH"
export PATH="/home/$USER/milonga:$PATH"

pip3 install virtualenv

# Now create virtualenv
