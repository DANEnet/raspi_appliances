#apt-get --purge remove sonic-pi
#apt-get --purge remove minecraft
apt-get update && sudo apt-get upgrade
apt-get autoremove

apt-get install apache2
apt-get install python-matplotlib
apt-get install python-rpi.gpio
apt-get install owfs ow-shell i2c-tools  # includes w1-therm

#do not  forget  localisations and timezone
#
