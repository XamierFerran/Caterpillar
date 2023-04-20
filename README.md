# Caterpillar

Hello! This is the README for our ME35 robotics project. Please remember to create your own branch and work on any changes to code there. I don't anticipate us having to work on the same coding files, but it's useful to keep these around for versioning.

## Vision
The OpenMV cam currently has yet to be tested, but there is currently a program within the Vision folder that should be able to detect the color of an apple and track it. This code was pulled from an arduino tutorial: https://docs.arduino.cc/tutorials/nicla-vision/blob-detection. Since the assignment only asks to detect "something" and then the dog stops, I will record color data for an easy to detect solid color. This information is sent through the serial terminal as a 1 or a 0. Now, there are two ways to get this data to the rest of the dog. 

### Sent through ESP
Using previous ME35 code, I can read the necessary information from serial on an ESP32 and then send using an MQTT script.
+ MQTT script already written.
- May be difficult to read in serial since that was a problem I had in previous projects. However, it is possible and I have done it so I could reference old code.
- A little harder to fabricate since I'd be dealing with two boards instead of one. Not a big issue though.

### Sent through Nicla
Since the Nicla has wifi capabilities, I could just publish MQTT from the board.
+ Super streamlined process for coding
+ No extra wires, less complex head design
- I'd have to learn how to connect to wifi, and I know connecting to Tufts Wireless from a microcontroller is annoying.
- Figure out how to setup MQTT on Nicla.

### Enclosure Ideas
https://thangs.com/search/arduino%20nicla%20vision?scope=all
https://www.thingiverse.com/thing:5359047
https://www.thingiverse.com/thing:5759796

Trouble Shooting: 
- I've been messing around with the UART connection for sometime but it doesn't seem to like to actually get the data over. Not sure what to do since I know each side can receive and transmit as needed, but not to each other. 
- The Nicla can definitely send and receive serial. I can't fully tell through my esp because of the fact that the micro usb shorts the uart connections.
- Two approaches
1. continue debugging esp (possibly with Chris or other eye folk)
2. try using a raspberry pi (pico or reg but try reg first). Connect vision to pico through micro usb. Use Rose's code to send through serial. Look up serial documentation for raspberry pi. try to recieve serial. Setup MQTT

Communicating through serial to the ESP coninued to be a painful process. I confirmed that the OpenMV is not the problem by connecting its rx to tx and seeing that the serial signal was indeed being passed. The ESP was unable to receive the serial data, so started focusing on the wifi connection. Previously, I used a wifi example program to test both the new and old anntena, but both failed to work. With the help of Rose, I decided to use an entirely different wifi connection (tufts_eecs) and I got a new error! My code is able to detect nearby wifi signals, and possibly even connects, but I get tons of errors:
- [CYW43] error: hdr mismatch 80fe ^ 0000
with random numbers/letters for those last eight characters. Next up, I'll try implementing mqtt using some example code. Only problem is I forgot how to start up mqtt on my local machine... 

I managed to setup sub and pub on my local mqtt server. After adjusting the code I got a new error! This is actually a sensical error, it seems that I did something wrong in setting up my mqtt code. That means the code got passed all of the wifi stuff and even returned "Wifi connected" in the serial monitor. 

Nextup, I need to understand more about mqtt library without using Chris's library.

also, here's how to setup the MQTT server locally:
- type services in search bar of windows
- start mqtt server
- go to mqtt location "Program Files"
- type in example code

It turns out to run MQTT the broker and the board need to be on the same wifi. The board needs to use the ip address of the broker.