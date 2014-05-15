python build.py build &&
    rsync -r --progress deploy/ bendoan:/home/public
