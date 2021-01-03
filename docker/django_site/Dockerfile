FROM ubuntu:20.04
RUN sudo apt-get install m4 make autoconf automake gcc g++ git findutils && \
    sudo apt-get install libgsl-dev petsc-dev slepc-dev && \
    sudo apt-get install gnuplot paraview pandoc && \
    sudo apt-get install python3.7 python3-pip && \
    git clone https://github.com/seamplex/milonga/ && \
    cd milonga && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make check && \
    sudo make install && \
    wget http://gmsh.info/bin/Linux/gmsh-4.5.1-Linux64.tgz && \
    tar -xvzf gmsh-4.5.1-Linux64.tgz && \
    export PATH=$(pwd) + "/gmsh-4.5.1-Linux64/bin:$PATH" && \
    export PATH=$(pwd) + "./milonga:$PATH" && \
    git clone https://github.com/kgmcquate/django_site.git && \
    