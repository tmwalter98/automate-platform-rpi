sudo apt-get install python3-pip
pip3 install gpiozero pigpio rpi.gpio python-decouple paho-mqtt

sudo timedatectl set-ntp True
sudo timedatectl set-local-rtc true
sudo timedatectl set-timezone America/New_York
