#!/usr/bin/env python3
import serial
from flask import Flask, request, render_template_string, jsonify
import datetime
import time
import threading

app = Flask(_name_)

running = False # to control loop in thread
value = 65
dis=1750
action="No action Required"
percentage_filled=0

def arduino_sensor():
    global distanceCm,percentage_filled
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()
    while True:
        if ser.in_waiting > 0:
            duration = ser.readline().rstrip();
            distanceCm = int(ser.readline().rstrip())
            distanceInch = ser.readline().rstrip()
	    percentage_filled=float((17-distanceCm)*100/17)
	    if percentage_filled<0:
		percentage_filled=0
            print("distanceCm:",distanceCm)
            

def rpi_function():
    global value,dis

    print('start of thread')
    while running: # global variable to stop loop  
        value += 1
        dis+=1
        time.sleep(1)
    print('stop of thread')


@app.route('/')
@app.route('/<device>/<action>')
def index(device=None, action=None):
    global running
    global value,dis
    global percentage_filled
  
    threading.Thread(target=arduino_sensor).start()
    if device:
        if action == 'on':
            if not running:
                print('start')
                running = True
                threading.Thread(target=rpi_function).start()
            else:
                print('already running')
        elif action == 'off':
            if running:
                print('stop')
                running = False  # it should stop thread
            else:
                print('not running')
    return render_template_string('''<!DOCTYPE html>
   <head>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
   </head>
   <style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
    th, td {
    padding: 5px;
    text-align: left;
    }
   </style>
   <body>
        <h2>Smart Garbage collector Readings</h2>
            <table style="width:80%">
            <tr>
                <th>Time</th>
                <th>Distance(cm)</th>
                <th>Percentage_Filled</th>
                <th>Action</th>
            </tr>
            <tr>
                <td id="time"></td>
                <td id="distance"></td>
                <td id="num"></td>
                <td id="action"></td>
            </tr>
            </table>


        <br>
        <a href="/bioR/on">TURN ON</a>  
        <a href="/bioR/off">TURN OFF</a>
        <script>
            setInterval(function(){$.ajax({
                url: '/update',
                type: 'POST',
                success: function(response) {
                    console.log(response);
                    $("#num").html(response["value"]);
                    $("#time").html(response["time"]);
                    $("#distance").html(response["distance"]);
                    $("#action").html(response["action"]);
                },
                error: function(error) {
                    console.log(error);
                }
            })}, 1000);
        </script>
   </body>
</html>
''')
@app.route('/update', methods=['POST'])
def update():
    global action
    if percentage_filled>=50 and percentage_filled<75:
        action="Collect Garbage"
    elif percentage_filled>=75:
        action="Urgent Action Required"
    else:
	action="No action Required"
    return jsonify({
        'value': percentage_filled,
        'time': datetime.datetime.now().strftime("%H:%M:%S"),
        'distance': distanceCm,
        "action":action
    })

app.run() #debug=True
