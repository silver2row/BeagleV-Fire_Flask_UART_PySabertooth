#!/usr/bin/python3

from PySabertooth import Sabertooth
from flask import Flask, render_template

from time import sleep

saber = Sabertooth("/dev/bone/uart/4", baudrate=9600, address=128, timeout=0.1)

app = Flask(__name__)
@app.route("/")
@app.route("/<state>")

def gar(state=None):
    sleep(0.4)
    if state == "F":
        print ("Robot Moving Forward")
        saber.drive(1, 100)
        saber.drive(2, 100)

    if state == "R":
        print ("Robot Turning Right")
        saber.drive(1, 75)
        saber.drive(2, 25)

    if state == "L":
        print ("Robot Turning Left")
        saber.drive(1, 25)
        saber.drive(2, 75)

    if state == "S":
        print ("Robot Stopped")
        saber.drive(1, 0)
        saber.drive(2, 0)
        saber.stop()

    if state == "REV":
        print ("Robot Reverses")
        saber.drive(1, -70)
        saber.drive(2, -70)

    template_data = {
        "title" : state,
    }
    return render_template("flat_bot.html", **template_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
