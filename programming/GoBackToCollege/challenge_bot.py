#!/usr/bin/python3

import socket
import time
import math

# send() and recv() from socket module works with bytes objets, not strings
# here : all processes are done with strings, and at the end, send_command() 
# is used for encoding strings in bytes objects and sending it to the socket


def send_command(socket, command):
    print('\033[91m' + command +'\033[0m')
    socket.send(command.encode())

          
server_name     = "irc.root-me.org"
port            = 6667
channel_name    = "#root-me_challenge"
bot_name        = "chabannix"
bot_name_rootme = "Candy"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_name,port))

send_command(s, "NICK " + bot_name + "\r\n")
send_command(s, "USER " + bot_name + " " + bot_name + " " + bot_name + ": " + bot_name + "\r\n")
send_command(s, "JOIN " + channel_name + "\r\n")

buffer = s.recv(4096).decode()
print(buffer)

time.sleep(3) # seems necessary for the server to be ready
send_command(s, "PRIVMSG " + bot_name_rootme + " :!ep1\r\n")

buffer = ""
while 1:

    buffer += s.recv(4096).decode()
    print(buffer)
    
    lines = buffer.splitlines()

    for line in lines:

        # check if this is a Candy msg :
        if line.find("PRIVMSG "+bot_name) >-1 :
            user_name = ""
            for c in line.split()[0]:
                if c == '!':
                    break
                if c != ':':
                    user_name += c
            
            if user_name == bot_name_rootme and line.find("/") > -1:
                index = line.split().index("/")

                op1 = line.split()[index-1]
                op1 = int(op1[1:]) # we remove the ':' before the first number

                op2 = line.split()[index+1]
                op2 = int(op2)

                result = math.sqrt(op1) * op2
                result = round(result, 2)

                command = "PRIVMSG " + bot_name_rootme + " :!ep1 -rep " + str(result) + "\r\n"
                send_command(s, command)

        # PING received -> reply PONG
        if line.split()[0] == "PING":
            command = "PONG "+line.split()[1]+"\r\n"
            send_command(s, command)
       
    buffer = ""