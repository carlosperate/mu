#!/bin/bash

# Controls the state of 3 LEDs connected to the Raspberry Pi
# GPIO based on the first command line argument.
# Usage: ./traffic.sh on
#        ./traffic.sh off
#        ./traffic.sh green
#        ./traffic.sh yellow
#        ./traffic.sh red
#        ./traffic.sh unexport

# Set up the 3 lights Pi GPIO values here
green_light=16
yellow_light=20
red_light=21


all_off() {
    echo "0" > "/sys/class/gpio/gpio$green_light/value"
    echo "0" > "/sys/class/gpio/gpio$yellow_light/value"
    echo "0" > "/sys/class/gpio/gpio$red_light/value"
}

green_on() {
    echo "1" > "/sys/class/gpio/gpio$green_light/value"
}

yellow_on() {
    echo "1" > "/sys/class/gpio/gpio$yellow_light/value"
}

red_on() {
    echo "1" > "/sys/class/gpio/gpio$red_light/value"
}

all_on() {
    green_on
    yellow_on
    red_on
}

unexport() {
    echo "$green_light" > /sys/class/gpio/unexport
    echo "$yellow_light" > /sys/class/gpio/unexport
    echo "$red_light" > /sys/class/gpio/unexport
}


if [ ! -d "/sys/class/gpio/gpio$green_light/" ]; then
    echo "$green_light" > /sys/class/gpio/export
fi
echo "out" > "/sys/class/gpio/gpio$green_light/direction"

if [ ! -d "/sys/class/gpio/gpio$yellow_light/" ]; then
    echo "$yellow_light" > /sys/class/gpio/export
fi
echo "out" > "/sys/class/gpio/gpio$yellow_light/direction"

if [ ! -d "/sys/class/gpio/gpio$red_light/" ]; then
    echo "$red_light" > /sys/class/gpio/export
fi
echo "out" > "/sys/class/gpio/gpio$red_light/direction"


if [ $# -eq 0 ]; then
    echo -e "This script requires an argument. Options are:
    on
    off
    green
    yellow
    red
    unexport"
elif [ $1 = "on" ]; then
    all_on
elif [ $1 = "off" ]; then
    all_off
elif [ $1 = "green" ]; then
    all_off
    green_on
elif [ $1 = "yellow" ]; then
    all_off
    yellow_on
elif [ $1 = "red" ]; then
    all_off
    red_on
elif [ $1 = "unexport" ]; then
    unexport
else
    echo "argument not understood: $1"
fi
