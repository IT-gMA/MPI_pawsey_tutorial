#!/bin/bash
convert -delay 20 -loop 0 $(ls *.png | sort -n) animation.gif

