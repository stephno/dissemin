#!/bin/bash
find -maxdepth 1 -type d | grep -vP "^.($|/dissemin|/notification|/src|/\..*)" | xargs pyflakes3 > pyflakes.out
cat pyflakes.out
test \! -s pyflakes.out
