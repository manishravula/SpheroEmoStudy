#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/src/sphero_ros/sphero_driver"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/install/lib/python2.7/dist-packages:/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/build" \
    "/usr/bin/python" \
    "/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/src/sphero_ros/sphero_driver/setup.py" \
    build --build-base "/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/build/sphero_ros/sphero_driver" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/install" --install-scripts="/home/manish/Awesomestuff/classes/HRI-F-2k17/projectws/install/bin"
