ultra-mqtt

# Introduction

A test project w/ Python MQTT client connecting to Losant broker.

A typical use case of an MQTT client is a sensor that sends 
temperature or humidity data to the broker. In this case, I send
hard drive "free space" and "used space" as attributes to Losant. 

Communication can be a two-way street, so I added push-buttons on 
the Losant dashboard to generate and remove a 1GB file on the 
client machine.

The basis of this code came from the 
[Losant Python MQTT Client](https://docs.losant.com/mqtt/python/) page. 
I fleshed it out a bit, added a secondary timer, and accepted 
push-button commands from the Losant dashboard.


# Coding Details

This is all pretty simple. I didn't even write unit tests, which
is rare for me. Unit test all the things!

The RepeatTimer is used such that I can send data when I want to 
send it despite the event loop running every second to keep the
connection alive.

I threw all the "commands" (on_command) into a single file under 
a switcher.

I've included a sh script that I used to test what happens when a
network connection goes south. From this I was able to trap and 
test the connection without unplugging cables.

# The Dashboard

## The layout

Regarding the dashboard layout below, note the push-buttons towards 
the bottom, which were wired-up and do work.

The blip in the graph occurred when I removed the 1GB file that
was lying around.

![](docs/dashboard.png)

# Workflows

Losant provides "workflows," which allow you to do specific actions
based upon triggers from the data. For example, if a device connects,
I have an Email sent to me. (See figure below, left column) You will
note the Conditional node that only has a "yes" connection. This was
so that I could turn off the emails while I was testing the client
python code.

The second column shows a Virtual Button, which lets me do some
testing right from the workflow canvas instead of from the MQTT
client itself. In this case, I simply use the Debug node, which 
shows me the resultant payload through the workflow.

Note that I can have two wholly separate workflows on the same canvas.
Not sure that's worth anything, but it is possible.

![](docs/workflow.png)

# The Losant Broker

Losant acts as an MQTT broker to an MQTT client, which is what this
repo provides. This section describes various features on the Losant
side relative to this communication.

## On the Dashboard

The "Pause" button on the Losant dashboard seems to only pause
the dashboard. It doesn't sever the connection with the MQTT client.

## Under Devices

Under Devices there are some "Device Actions." Although you can force
a connection status of Connected or Disconnected, neither of these
affect a connected MQTT Client. I'm not sure what value these have
then.

## Deleting cruft data

While you can clear the Device Log, you cannot clear the Connection
Log nor the Recent Device States log directly. However, there is a 
pull-down option in the Device Actions button called "Delete Data," 
but note that it won't work if you have a connected MQTT Client. 
And Losant doesn't give you a warning or nuthin'. Hmmm.

Using the "Delete Data" option, when successful, deletes not only
the connection log but the saved state data. That's nice for "resetting"
the graph on the dashboard.
