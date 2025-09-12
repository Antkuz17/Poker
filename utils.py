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


def evaluateHands(self, hand1: Hand, hand2: Hand, comCards: CommunityCards) -> int:
    """
    Given two hands, the method evaluates which hand wins.
    Return values:
        1 if hand1 wins
        2 if hand2 wins
        0 if tie
    """

    # Combining the hands with the community cards to better evaluate hand strength
    full_hand1 = hand1.Cards + comCards.getCards()
    full_hand2 = hand2.Cards + comCards.getCards()

def isRoyalFlush(Cards: list) -> bool:
    """Only returns whether there was a royal flush or not, no need to return any other values since RF is the best possible hand.
    Royal Flush: From the 7 cards, there is a 10, J, Q, K, A all of the same suit (e.g. 10♥, J♥, Q♥, K♥, A♥)."""


    

def isStraightFlush(Cards: list) -> tuple[bool, int]:
    """Returns a boolean depending on whether there was a straight flush or not, and if there was, returns the highest card in the straight flush.
    Straight Flush: From the 7 cards, there are 5 cards in sequence all of the same suit (e.g. 4♠, 5♠, 6♠, 7♠, 8♠). In this case, the high card is 8♠."""

    


def isFourofKind(Cards: list) -> tuple[bool, int]:
    """Returns a boolean depending on whether there was a four of a kind or not, and if there was, returns the rank of the four cards."""


def isFullHouse(Cards: list) -> tuple[bool, tuple[int, int]]:
    """Returns a boolean depending on whether there was a full house or not, and if there was, returns the ranks of the three-of-a-kind and the pair."""


def isFlush(Cards: list) -> tuple[bool, list]:
    """Returns a boolean depending on whether there was a flush or not, and if there was, returns the top 5 ranks in the flush."""


def isStraight(Cards: list) -> tuple[bool, int]:
    """Returns a boolean depending on whether there was a straight or not, and if there was, returns the highest card in the straight."""


def isThreeofKind(Cards: list) -> tuple[bool, int]:
    """Returns a boolean depending on whether there was a three of a kind or not, and if there was, returns the rank."""


def isTwoPair(Cards: list) -> tuple[bool, tuple[int, int]]:
    """Returns a boolean depending on whether there was a two pair or not, and if there was, returns the ranks of both pairs."""



def isPair(Cards: list) -> tuple[bool, int]:
    """
    Returns a tuple:
        - First element: True if there is a pair, False otherwise.
        - Second element: The rank of the pair if found, or -1 if no pair.
    
    Args:
        Cards (list): A list of card objects. Each card must have a getRank() method.
    
    Returns:
        tuple: (bool, int)
    """
    rank_counts = {}

    # Count the occurrences of each rank
    for card in Cards:
        rank = card.getRank()
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

    # Check if any rank occurs exactly twice
    for rank, count in rank_counts.items():
        if count == 2:
            return True, rank

    return False, -1

def getHighCard(Cards: list) -> int:
    """Returns the highest card rank from the list of cards."""

    



     
    



     
