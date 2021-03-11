verbs = ["eat", "sleep", "study", "read", "cry", "think", "meet", "overthrow", "play", "work"]
import random

def extract(suggestion):
    for verb in verbs:
        if (verb in suggestion):
            return verb


def formulate(bot, verb, altverb = None):
   if (bot == "thinker"): return thinker(verb, altverb)
   if (bot == "complainer"): return complainer(verb, altverb)
   if (bot == "guesser"): return guesser(verb, altverb)
   return "Invalid bot parameter";


thinkersList = [];
def thinker (suggestion, altsuggestion = None):
  if (altsuggestion != None):
      return "";

  length = len(thinkersList)
  thinkersList.append(suggestion)

  if (length < 2):
   return "Thinker: hmmm...";

  likes = ["cook", "eat", "overthrow", "cry"];
  uncertainties = ["meet", "play", "work"]
  dislikes = ["sleep", "study", "read", "think"]

  answer = "Thinker: ";
  for verb in thinkersList:
      if verb in likes:
          answer += "I say {} is a good idea. ".format(verb + "ing")
      elif verb in uncertainties:
          answer += "Not too sure about {}. ".format(verb + "ing")
      elif verb in dislikes:
          answer += "I'm not to keen on {}. ".format(verb + "ing")

  thinkersList.clear()


  return answer;

"""
def talker(suggestion, altsuggestion = None):
    if (altsuggestion == None):
        return "Talker: hey";
    return "Talker: I feel {} and {} are tempting.".format(suggestion + "ing", altsuggestion + "ing")
"""

complainersList = [];
def complainer (suggestion, altsuggestion = None):
  ret = "Complainer: ...";
  if (altsuggestion == None):
      if suggestion in complainersList:
          ret = "Complainer: Suggesting {} again? Really?".format(suggestion + "ing")
      complainersList.append(suggestion)

  else:
      if altsuggestion in complainersList:
          if suggestion in complainersList:
             return "Complainer: I'm tired of people saying {}.".format(altsuggestion + "ing")
          else:
             return "Complainer: I didn't hear {} before, but I had to hear {} again...".format(suggestion + "ing", altsuggestion + "ing")
      else:
        return "";

  return ret;

guesserLikes = ["play", "think", "read", "meet", "overthrow", "eat", "work", "eat"];
guesses = [];
def guesser (suggestion, altsuggestion = None):

    guess1 = random.choice(verbs)
    guess2 = random.choice(verbs)
    while (guess1 == guess2):
        guess1 = random.choice(verbs)

    correct = (suggestion in guesses);
    guesses.clear()

    if (altsuggestion != None):
        if altsuggestion in guesserLikes:
            return "Guesser: By the way, I'm totally down for {}.".format(altsuggestion + "ing")
        else:
            return "";

    if (not correct):
        guesses.append(guess1)
        guesses.append(guess2)
        return "Guesser: Next time it'll suggest either '{}' or '{}'.".format(guess1 + "ing", guess2 + "ing")
    else:
        return "Guesser: Yes! I was right."