verbs = ["cook", "eat", "sleep", "study", "read", "cry", "think", "meet", "overthrow", "play", "work"]
import random

def extract(suggestion):
    for verb in verbs:
        if (verb in suggestion):
            return verb


def formulate(bot, verb):
   if (bot == "thinker"): return thinker(verb)
   if (bot == "complainer"): return complainer(verb)
   if (bot == "guesser"): return guesser(verb)
   return "Invalid bot parameter";


thinkersList = [];
def thinker (suggestion):
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
          answer += "I think {} is a good idea. ".format(verb + "ing")
      elif verb in uncertainties:
          answer += "Not too sure about {}. ".format(verb + "ing")
      elif verb in dislikes:
          answer += "I'm not to keen on {}. ".format(verb + "ing")

  thinkersList.clear()
  return answer;


complainersList = [];
def complainer (suggestion):
  if suggestion in complainersList:
      return "Complainer: Suggesting {} again? Really?".format(suggestion + "ing")
  complainersList.append(suggestion)
  return "Complainer: ..."

guesses = [];
def guesser (suggestion):

    guess1 = random.choice(verbs)
    guess2 = random.choice(verbs)
    while (guess1 == guess2):
        guess1 = random.choice(verbs)

    correct = (suggestion in guesses);
    guesses.clear()

    if (not correct):
        guesses.append(guess1)
        guesses.append(guess2)
        return "Guesser: Next time, it'll suggest either '{}' or '{}'.".format(guess1 + "ing", guess2 + "ing")
    else:
        return "Guesser: Yes! I was right."