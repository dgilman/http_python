#!/usr/bin/env sh

curl -v http://localhost:5000/the_room.txt > /dev/null
curl --compressed -v http://localhost:5000/the_room.txt > /dev/null
