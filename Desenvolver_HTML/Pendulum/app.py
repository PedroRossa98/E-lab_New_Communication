import json
from time import sleep
import random
import math 
import time
import logging
from flask import Flask, request, jsonify, session, Response, render_template
# from flask_session import Session
# from flask_csv import send_csv
from flask_cors import CORS

FORMAT = 'utf-8'
NAME_EXP = "Monte Carlo"
serial_port = None
Delta_x = None
n_points = None
frist = 1
i = 1
total_in = 0
error_x = 0.005

app = Flask(__name__, template_folder='html', static_folder='html/')
app.secret_key = '*}6Ttt)G7X_T}3VF:ygc'


app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_TYPE'] = 'memcached'
#sess = Session(app)
    

app.debug = False
#app.logger.disabled = False


logging.basicConfig(level=logging.DEBUG) # CRITICAL, ERROR, WARNING, INFO, and DEBUG 

log = logging.getLogger('werkzeug')
log.disabled = True

CORS(app,automatic_options=False)


def receive_data_from_exp():
    global serial_port
    global frist 
    global i 
    global total_in
    if frist == 1:
        frist =0
        return "DATA_START"
    if int(i) > int(n_points):
        sleep(0.01)
        return "DATA_END"
    else:

        x = 5.0 + float((random.randrange(-10,10)*3.0*float(error_x)))
        vel = Delta_x/x
        e_vel = math.sqrt((float(Delta_x)/(float(x)**2))**2*float(error_x)**2+(1/x)**2*0.005**2)
        temp = 28.00+ float(random.randrange(-1,1))
        sleep(x)
        pic_message =   {"Sample_number":str(i),
                        "period":str(x),
                        "e_period":str(error_x),
                        "velocity":str(vel),
                        "e_velocity":str(e_vel),
                        "temp":str(temp)}
        print (pic_message)
        i=i+1
    return pic_message

def do_config(config_json) :
    global serial_port

    global Delta_x
    global n_points
    

    print(config_json)
    n_points = config_json["config_experiment"]["Samples"]
    Delta_x = config_json["config_experiment"]["DeltaX"]

    print("Number of samples: ")
    print(n_points)
    print("\n")
    print("Inicial X displacement: ")
    print(Delta_x)


    return  config_json,True

def ConfigureStartExperiment(user_json):
    
    do_config(user_json)
    return ''

@app.route('/',methods=['GET'])
def HTML_exe():
    return render_template("index-elab.html")

@app.route('/user', methods=['POST','OPTIONS'])
def Flask_f1():
    global i
    global frist
    frist =1
    i = 1
    if request.method == 'POST':
        #origin = request.headers.get('Origin')	
        print(request.data)
        user_json = json.loads(request.data.decode(FORMAT))
        ConfigureStartExperiment(user_json)
        return '' #jsonify({'JSON Enviado' : request.args.get('JSON'), 'result': 'OK!'})
    elif request.method == 'OPTIONS':
        return ''



@app.route('/resultpoint', methods=['GET'])
def getPoint():
    global end
    exp_data = receive_data_from_exp()
    send_data = {"msg_id" : "11",
                 "timestamp" : str(time.time_ns()),
                 "status" : "waiting", 
                 "Data" : " "}

    if exp_data == "DATA_END": #and end == 0:
        send_data =     {"msg_id":"11",
                        "timestamp": str(time.time_ns()),
                        "status":"Experiment Ended",
                        "Data":" "}
    else :
        send_data =     {"msg_id" : "11",
                        "timestamp" : str(time.time_ns()),
                        "status" : "running", 
                        "Data" : exp_data}
    print(send_data)
    return send_data


if __name__ == "__main__":
    app.run('127.0.0.1',8001,debug=False)