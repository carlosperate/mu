#!/bin/sh

# We reinstall requirements in case they change
sudo pip3 install -r requirements.txt

# Create the timestamp
DATE_=$(date '+%Y-%m-%d_%H_%M_%S')

# Generate .deb package
DEB_BUILD_DIR="../deb-build-area"
if [ -d "$DEB_BUILD_DIR" ]; then
    rm -r "$DEB_BUILD_DIR" 
fi

git-buildpackage --git-upstream-tree="$GIT_COMMIT" --git-ignore-branch --git-export-dir="$DEB_BUILD_DIR" --git-force-create --git-purge  -uc -us

for f in "$DEB_BUILD_DIR/"*; do
    if [ ${f: -4} == ".deb" ]; then
        DEB_FILE_NAME="mu-$DATE_.deb"
        mkdir dist
        mv "$f" "dist/$DEB_FILE_NAME"
        echo "$f moved to $DEB_FILE_NAME"
    fi
done

# Generate self-contained executable
python3 ../pyinstaller/pyinstaller.py package/pyinstaller.spec
du -sk dist/
if [ -f dist/mu ]; then
    exec_name="mu-$DATE_"
    mv "dist/mu" "dist/$exec_name"
    echo "EXECUTABLE_NAME=$exec_name"
fi

