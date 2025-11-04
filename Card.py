"""
card.py

This module contains the 'Card' class which represents one playing card

Each playing card has a rank ('A', '2', '3', 'K', '4') and a suit ('Hearts', 'Spades', 'Diamonds', 'Clubs')

This class includes methods for
- Displaying you the card using the default python print 
- Getting the rank and suit of a given card

"""


class Card:

    # Constructor for card
    def __init__(self, rank : str, suit : str):
        self.rank = rank
        self.suit = suit

    # Dunder method used to represent a card when a card is printed
    def __str__(self):
        return(f"{self.rank} of {self.suit}")
    
    # Getters and Setters
    def getSuit(self) -> str:
        """Returns the suit of the card as a string"""
        return self.suit
    
    def getRank(self) -> str:
        """Returns the rank of the card as a string (2, 5, J, A, etc)"""
        return self.rank
    
    
