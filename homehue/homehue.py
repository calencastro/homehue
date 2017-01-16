#!/usr/bin/env python
import time
import json
from os import path
from qhue import Bridge, QhueException, create_new_username


#coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)


# the IP address of your bridge
BRIDGE_IP = "172.15.30.100"

# the path for the username credentials file
CRED_FILE_PATH = "qhue_username.txt"

msleep = lambda x: time.sleep(x / 1000.0)

Color = 0

global bridge


def next_colour():
    global Color
    
    Color += 1000
    if (Color > 65535):
        Color = Color - 65535

def main():
    global bridge
    
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
    print lights()

    # query the API and print the results
    #while True:
    #    bridge.lights[3].state(bri=254, hue=Color)
    #    print Color
    #    msleep(100)
    #    next_colour()



@app.route('/')
def index():

    lamp2 = []
    #lights = bridge.lights
    y = 0
    for i in bridge.lights():
        lights = bridge.lights[y+1]()
        lampada = []
        lampada.append(lights["name"])
        lampada.append(lights["state"]["reachable"])
        lampada.append(lights["state"]["on"])
        lamp2.append(lampada)
        y = y + 1

    return render_template('index.html', lamphtml = lamp2)

@app.route('/light/<int:light_id>/<int:onoff>')
def readMenu(light_id, onoff):
    global bridge
    if (onoff == 1):
        bridge.lights[light_id].state(on = True)
    else:
        bridge.lights[light_id].state(on = False)
    return render_template('index.html')

    
if __name__ == '__main__':
    main()
    app.secret_key = 'SuperSecretKey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 80) 
