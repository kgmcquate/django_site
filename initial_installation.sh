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

sudo apt-get install python3.6 python3-pip

wget http://gmsh.info/bin/Linux/gmsh-4.5.1-Linux64.tgz

tar -xvzf gmsh-4.5.1-Linux64.tgz

echo 'export PATH="/home/kevin/gmsh-4.5.1-Linux64/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="/home/$USER/milonga:$PATH"' >> ~/.bashrc

export PATH="/home/kevin/gmsh-4.5.1-Linux64/bin:$PATH"
export PATH="/home/$USER/milonga:$PATH"

pip3 install virtualenv

# Now create virtualenv
# virtualenv venv

# source ~/reactor_sim/venv/bin/activate

# pip install django

#Generate cronjobs with crontab -e
# Deletes plots every hour
#* * * * * find /home/kevin//home/kevin/reactor_sim/milonga_diffusion/static/plots -mmin +1 -exec rm {} \;

# Ensures deletion of temp files
#0 * * * * find /home/kevin/reactor_sim/milonga_diffusion | grep temp_ | xargs rm -fr

sudo apt-get update
sudo apt-get install apache2 libapache2-mod-wsgi-py3


# Add to /etc/apache2/sites-available/000-default.conf
#<< 'MULTILINE-COMMENT'
#	Alias /static /home/kevin/reactor_sim/milonga_diffusion/static
#       <Directory /home/kevin/reactor_sim/milonga_diffusion/static>
#                Require all granted
#        </Directory>

#        <Directory /home/user/reactor_sim/reactor_sim>
#                <Files wsgi.py>
#                        Require all granted
#                </Files>
#        </Directory>

#	WSGIDaemonProcess myproject python-path=/home/kevin/reactor_sim python-home=/home/ke$
#	WSGIProcessGroup reactor_sim
#	WSGIScriptAlias / /home/kevin/reactor_sim/reactor_sim/wsgi.py
#MULTILINE-COMMENT
