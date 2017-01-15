#!/usr/bin/env python
import time
from os import path
from qhue import Bridge, QhueException, create_new_username

# the IP address of your bridge
BRIDGE_IP = "172.15.30.100"

# the path for the username credentials file
CRED_FILE_PATH = "qhue_username.txt"

msleep = lambda x: time.sleep(x / 1000.0)

Color = 0

def next_colour():
    global Color
    
    Color += 1000
    if (Color > 65535):
        Color = Color - 65535

def main():

    # check for a credential file
    if not path.exists(CRED_FILE_PATH):

        while True:
            try:
                username = create_new_username(BRIDGE_IP)
                break
            except QhueException as err:
                print "Error occurred while creating a new username: {}".format(err)

        # store the username in a credential file
        with open(CRED_FILE_PATH, "w") as cred_file:
            cred_file.write(username)

    else:
        with open(CRED_FILE_PATH, "r") as cred_file:
            username = cred_file.read()

    # create the bridge resource, passing the captured username
    bridge = Bridge(BRIDGE_IP, username)

    # create a lights resource
    lights = bridge.lights

    # query the API and print the results
    while True:
        bridge.lights[3].state(bri=254, hue=Color)
        print Color
        msleep(100)
        next_colour()

    
if __name__ == "__main__":
    main()
