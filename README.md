ultra-mqtt

# Introduction

A test project w/ Python MQTT client connecting to Losant.

The basis of this code came from the 
[Losant Python MQTT Client](https://docs.losant.com/mqtt/python/) page. 
I fleshed it out a bit, added a secondary timer, and accepted 
push-button commands from the Losant dashboard.

This example sends a status of hard drive free space and used space
as attributes to Losant. I added push-buttons to generate and 
remove a 1GB file, which I can then see on my dashboard.

# Coding Details

This is all pretty simple. I didn't even write unit tests, which
is rare for me. Unit test all the things!

The RepeatTimer is used such that I can send data when I want to 
send it despite the event loop running every second to keep the
connection alive.

I threw all the "commands" (on_command) into a single file under 
a switcher.

# The Dashboard

Note the push-buttons towards the bottom, which were wired up and
work.

The change in the graph occurred when I removed the 1GB file that
was lying around.

![](docs/dashboard.png)