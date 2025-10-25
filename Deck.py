from Card import Card
import random

"""
deck.py

This module contains the 'deck' class which represents one full deck of cards

Each deck has 52 card objects and holds the cards in an 'Cards[]' array

This class includes methods for
- Drawing a card from the deck 
- Shuffling the deck
- Removing a specific card from the deck
- Iterator method that returns the array of cards when iteration attempted
"""

class Deck:
    # Constructor
    def __init__(self):
        # Holds the empty cards
        self.Cards = []

        suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        for x in suits:
            for y in ranks:
                self.Cards.append(Card(y, x))
    
    def __iter__(self) -> None:
        """Iterator method (magic method) that allows for iteration throught the deck, returns an itererable type when called"""
        return iter(self.Cards)
    
    def draw(self) -> Card:
        """Returns a card from the top of the deck"""
        return self.Cards.pop()
    
    def shuffleCards(self) -> None:
        """Shuffles the cards within the deck"""
        return random.shuffle(self.Cards)
    
    def removeCard(self, card: Card) -> None:
        """Remove the given card from the deck if it exists."""
        if card in self.Cards:
            self.Cards.remove(card)


