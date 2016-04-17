#!/bin/sh
set -ev
sudo apt-get update

# Pi should already have Python3
#sudo apt-get install python3

# We need to build the pyinstaller from source, probably better by hand
# git clone http://github.com/pyinstaller/pyinstaller.git
# cd pyinstaller/bootloader
# python3 waf configure --no-lsb build install
# python3 ./waf distclean all --no-lsb

sudo apt-get install python3-pyqt5 -y
sudo apt-get install python3-pyqt5.qsci -y
sudo apt-get install python3-pyqt5.qtserialport -y

# Required for the Twitter python script
sudo pip install twython

