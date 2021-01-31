xhost +
docker build -t labelling_app .
docker run --rm -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${PWD}/media:/media \
    -e DISPLAY=$DISPLAY \
    labelling_app
