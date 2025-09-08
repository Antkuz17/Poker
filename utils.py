import random
from Hand import Hand
from CommunityCards import CommunityCards
from Card import Card

def genRandNum(min, max) -> int:
    """This will return an random integer between min and max inclusive"""
    return (random.randint(min, max))

def inputValidation(attemptedInput, requiredType: type):
    """Uses a validation loop to continue reprompting the user until their input matches the type provided"""
    while True:
            try:
                value =requiredType(attemptedInput) # Tries to cast the input to the type required
                return value # If it works, return the value
            except ValueError:
                attemptedInput = input("Invalid input, try again: ") # If it throws a value error, reprompt


def evaluateHands(self, hand1 : Hand, hand2 : Hand, comCards: CommunityCards) -> int:
     """Given two hands, the method will evalute which hand wins. The return value will differ based on the higher hand. If
     hand1 is higher, 1 is returned, if hand 2 is higher, 2 is returned. If the hands tie, then 0 is returned"""

    
     
