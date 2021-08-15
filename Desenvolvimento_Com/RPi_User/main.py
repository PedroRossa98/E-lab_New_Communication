import socket
import json

HEADER = 64
PORT = 5050
BINARY_DATA_PORT = 5051
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.101"
ADDR = (SERVER, PORT)

CONFIG_OF_EXP = []
MY_IP = "192.168.1.7"
SEGREDO = "estou bem"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive():
    msg_length = client.recv(HEADER)
    if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            myjson = json.loads(msg)
            check_msg(myjson)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)



def check_msg(myjson):
    if 'msg_id' in myjson:
        msg_id = int( myjson['msg_id'] )
        if ( msg_id == 1): #CONFIG MESSAGE
            global CONFIG_OF_EXP
            CONFIG_OF_EXP = myjson['config_file']
            
            #LIGAR A DISPOSITIVO EXP


            send('{"reply_id": "1", "status":"Config received"}')
        
        elif( msg_id == 2): #CONFIGURESTART MESSAGE
            #DO CONFIG
            
            #CHECK EFFECTIVE CONFIG
            pass
            #REPLY TO SERVER WITH EFFECTIVE CONFIG


        elif( msg_id == 3): #STOP MESSAGE
            #DO STOP
            pass
            #REPLY WITH STATUS
        
        else:
            pass


def IStarted():
    send_msg = '{"msg_id": "6","id_RP":"'+str(MY_IP)+'","segredo":"'+str(SEGREDO)+'"}'
    send(send_msg)

def ExperimentResults(Resulte):
    send_msg = '{"msg_id":"7", "results":"'+Resulte+'"}'
    send(send_msg)
    #Não estou a entender de como fazer a pate do erro nesta função preciso de preceber o que o rpi recebe dos PIC's


def SendFile(bin_data) :
    bin_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bin_data_socket.connect((SERVER, BINARY_DATA_PORT)) #APANHAR ERROS

    bin_data_socket.send(len(bin_data))
    bin_data_socket.send(bin_data)

    reply_size = bin_data_socket.recv(HEADER)
    msg = bin_data_socket.recv(reply_size)

    #Reply message received, comunication is done, close socket
    bin_data_socket.shutdown(socket.SHUT_RDWR)
    bin_data_socket.close()

    #CHECK MESSAGE
    #SEND STATUS TO SERVER

def SendStatus(type_data,timestamp, experiment_status,current_config):
    if type_data == 9:
        send_msg = '{"msg_id":"9", " timestamp":"'+timestamp+'", "experiment_status":"'+ experiment_status +'","current_config":"'+current_config+'"}'
    if type_data == 10:
        send_msg = '{"msg_id":"10", " timestamp":"'+timestamp+'", "id_dados_bin":'+ experiment_status+'"}'
    send(send_msg)

dados_conf = {"strat":"0","stop":"100","step":"0.1"}

#IStarted()
send_msg = '{"msg_id": "2","experiment_name":"Pendulo","config_experiment":"'+str(dados_conf)+'"}'
send(send_msg)
#receive()

input()

#print(CONFIG_OF_EXP['id'])

send(DISCONNECT_MESSAGE)