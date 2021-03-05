import socket
from bots import *
import argparse
import sys

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

clientSocket.send(bot.encode())
print("Introduced bot.")

print("Running...")

suggestion = "";
while True:
   suggestion = None;
   try:
    suggestion = clientSocket.recv(1024)
   except:
    print("Server ended connection.")
    sys.exit()
   if (suggestion != None):
       suggestion = suggestion.decode()
       print(suggestion)
       if ("Host:" in suggestion):
          verb = extract(suggestion)
          if (verb != None):
              response = formulate(bot, verb);
              clientSocket.send(response.encode())