echo "Building site..." &&
    python build.py build &&
    echo "Uploading site..." &&
    rsync -r --progress deploy/ bendoan.me:/home/public
