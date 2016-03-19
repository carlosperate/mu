#!/bin/sh
sudo pip3 install -r requirements.txt
python3 ../pyinstaller/pyinstaller.py package/pyinstaller.spec
du -sk dist/
mv dist/mu dist/mu-$(date '+%Y-%m-%d_%H_%M_%S')
