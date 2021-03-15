import socket
from bots import *
import argparse
import sys

# These imports were used strictly for "realism"
import random
import time

cmdParser = argparse.ArgumentParser(description="This script takes in three arguments, namely the client IP,"
                                             " the client port, and the bot to be used.")

cmdParser.add_argument("-ip", help="The provided IP is used to define the (remote) socket to be connected to.")
cmdParser.add_argument("-port", help="The provided port number is used to define the (remote) socket "
                                     "to be connected to.")
cmdParser.add_argument("-bot", help="The provided bot name is used to select which bot to use in this instance."
                                    " There are three available bots, 'thinker', 'complainer', and 'guesser'."
                                    " **Please provide the bot name without quotation marks and without capital"
                                    " letters.**")

arguments = cmdParser.parse_args();

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

ip = str(arguments.ip);
port = int(arguments.port);
bot = str(arguments.bot);

def validateBot(bot):
    if (bot == "thinker"): return True;
    if (bot == "complainer"): return True;
    if (bot == "guesser"): return True;
    return False;

while (validateBot(bot) == False):
    bot = input("Provide valid bot name (no caps-lock):")

print("Connecting to '" + bot + "' at socket " + str(ip) + ":" + str(port) + " ....")
clientSocket.connect((ip,int(port)))

print("Successfully connected to {} at port {}".format(ip,port))

print("Running...")

message = "";
rememberedVerb = "";

# Infinite loop: server.py decides when the running client.py instances will stop.
while True:
   message = None;

   try:
    message = clientSocket.recv(1024)
   except:
    print("Server ended connection.")
    sys.exit()

   if (message != None):
       message = message.decode()
       print(message)
       verb = extract(message)

       if (verb != None):
           response = "";
           if ("Host:" in message):
              rememberedVerb = verb;

                         # formulate(...) is responsible for calling the "bot" the user chose
              response = formulate(bot, verb)
           elif (message != "" and rememberedVerb != ""):

                # 'verb' becomes the second alternative if message is not from server.
              if (verb != rememberedVerb):
                  response = formulate(bot, rememberedVerb, verb);
                  rememberedVerb = "";

           time.sleep(random.randint(1,4))

           try:
               if (response != ""):
                   clientSocket.send(response.encode())
           except:
              print("Server ended connection.")
              sys.exit()