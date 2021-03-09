# Raspberry Pi EdgeDevice
### This is a system for home automation using low-cost Raspberry Pi sensor modules. The project consists of two main components—A collection of Raspberry Pi units with sensors and a program that uses that data to automate the lights. The communication between the two are facilitated using an MQTT broker.  Each Pi publishes live motion events and also samples environmental data like temperature, humidity, and ambient light. The backend is currently a Dockerized Python script that uses the motion data for presence detection along with astronomical data to control the lights through their API


## Experiments
 - ### Explore use of using mDNS for service discovery to assist in server discovery
    - ### Analyze potential security risks
 - ### Explore C based implementation for controlling LED indicator using PWM
 - ### Assist in i2c hardware discovery through address scan, followed by lookup, and subsequent attemt to communicate with potentially desired components

## Recent Changes
 - ### Introduced a reduction in thread could by removing unneccessarily threaded components
 - ### Centralized configuration
    - ### Eliminated accessing the same environmental variable in multiple locations
    - ### Eliminated need for external module