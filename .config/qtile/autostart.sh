#!/bin/bash

################################
### Autostart file for qtile ###
################################

### Compositor ###
picom -b &

### Background session utilities ###

#clipman is started only if it was not running already
pgrep xfce4-clipman || xfce4-clipman &
lxpolkit &
dunst &
rclone mount Drive: ~/Drive &

### System tray ###
blueman-applet &
nm-applet &
