#!/bin/sh

# We reinstall requirements in case they change
sudo pip3 install -r requirements.txt
python3 ../pyinstaller/pyinstaller.py package/pyinstaller.spec
du -sk dist/
if [ -f dist/mu ]; then
    date_=$(date '+%Y-%m-%d_%H_%M_%S')
    exec_name="mu-$date_"
    mv "dist/mu" "dist/$exec_name"
    echo "EXECUTABLE_NAME=$exec_name"
fi
