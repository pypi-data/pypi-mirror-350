#/usr/bin/sh
docker build -t midas --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .