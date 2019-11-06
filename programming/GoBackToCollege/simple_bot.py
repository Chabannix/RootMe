#!/usr/bin/python3

import socket

# useful links :
# http://abcdrfc.free.fr/rfc-vf/rfc1459.html
# https://docs.python.org/3/library/socket.html
# https://www.youtube.com/watch?v=QNNvNU4CCp8


# send() and recv() from socket module works with bytes objets, not strings
# here : all processes are done with strings, and at the end, send_command() 
# is used for encoding strings in bytes objects and sending it to the socket


def send_command(socket, command):
    print('\033[91m' + command +'\033[0m')
    socket.send(command.encode())

          
server_name  = "irc.debian.org"
port         = 6667
channel_name = "#test_bot"
bot_name     = "chabannix"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_name,port))

send_command(s, "NICK " + bot_name + "\r\n")
send_command(s, "USER " + bot_name + " " + bot_name + " " + bot_name + ": " + bot_name + "\r\n")
send_command(s, "JOIN " + channel_name + "\r\n")

buffer = ""
while 1:
    buffer += s.recv(4096).decode()
    print(buffer)
    
    lines = buffer.splitlines()

    for line in lines:

        # private msg for the bot received -> reply to this user
        if line.find("PRIVMSG "+bot_name) >-1 :
            user_name = ""
            for c in line.split()[0]:
                if c == '!':
                    break
                if c != ':':
                    user_name += c

            command = "PRIVMSG "+user_name+" :Hi "+user_name+", i'm chabannix\r\n"
            send_command(s, command)

        # private msg for the channel received -> reply to the entire channel
        if line.find("PRIVMSG "+channel_name) >-1 :
            command = "PRIVMSG "+channel_name+" :Hi guys, i'm chabannix\r\n"
            send_command(s, command)
       
    buffer = ""