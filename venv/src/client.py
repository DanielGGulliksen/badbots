import socket
from bots import *
import argparse
import sys
import random
import time

cmdParser = argparse.ArgumentParser(description="This script takes in three arguments, namely the client IP,"
                                             " the client port, and the bot to be used.")

cmdParser.add_argument("-ip", help="The provided IP is used to define the (remote) socket to be connected to.")
cmdParser.add_argument("-port", help="The provided port number is used to define the (remote) socket "
                                     "to be connected to.")
cmdParser.add_argument("-bot", help="The provided bot name is used to select which bot to use in this instance."
                                    " There are four available bots, 'thinker', 'complainer', 'talker', and 'guesser'."
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
    if (bot == "talker"): return True;
    return False;

while (validateBot(bot) == False):
    bot = input("Provide valid bot name (no caps-lock):")

print("Connecting to '" + bot + "' at socket " + str(ip) + ":" + str(port) + " ....")
clientSocket.connect((ip,int(port)))

#clientSocket.send(bot.encode())
print("Introduced bot.")

print("Running...")

message = "";
rememberedVerb = "";
alt2 = "";
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

       if ("Host:" in message):
          verb = extract(message)
          if (verb != None):
              rememberedVerb = verb;
              response = formulate(bot, verb);
              if (bot != "talker"):
                 time.sleep(random.randint(2,7))
              else:
                 time.sleep(random.randint(7,9))
              try:
               clientSocket.send(response.encode())
              except:
               print("Server ended connection.")
               sys.exit()

       # The portion of code below, as well as any lines relevant to the "talker" bot, the
       # 'rememberedVerb' and 'alt2' are not necessary for client.py to function. They
       # exist solely because of how I interpreted questions 2aii and 2b. I'm aware of
       # how these questions were optional, but I still found them unclear.
       elif (message != "" and rememberedVerb != ""):
           temp = alt2;
           alt2 = extract(message);
           if (alt2 == ""):
               alt2 = temp;
           if (alt2 != "" and alt2 != rememberedVerb):
               if (bot == "talker"):
                   answer = talker(rememberedVerb, alt2)
                   try:
                    clientSocket.send(answer.encode())
                   except:
                    print("Server ended connection.")
                    sys.exit()
                   rememberedVerb = "";
                   alt2 = "";
