from Card import Card
from Deck import Deck

"""
communityCards.py

This module contains the 'CommunityCards' class which represents the community cards in a poker game
Each community cards object has a list of card objects that make up the community cards which is stored in the 'Cards[]' array

This module includes methods for
- Printing the community cards to terminal
- Dealing the flop, turn, and river from a given deck
"""

class CommunityCards:
    def __init__(self) -> None:
        """Constructor for community cards class which stores cards as an list"""
        self.Cards = []

    def printCommunityCards(self) -> None:
        """Prints all of the current community cards to the terminal"""
        for Card in self.Cards:
            print(Card)

    def getCommunityCards(self) -> list:
        """Returns the list of all community cards"""
        return self.Cards

    def clearCards(self) -> None:
        """Clears all community cards for a new round"""
        self.Cards = []
    
    def dealFlop(self, deck: Deck) -> None:
        """Given a deck, this method will append the top three cards to the community cards.
        In other words, this method "deals" the flop"""
        for i in range (3):
            self.Cards.append(deck.draw())

    def dealTurn(self, deck: Deck) -> None:
        """Given a deck, this method will append the top card to the community cards.
        In other words, this method "deals" the turn"""
        self.Cards.append(deck.draw())

    def dealRiver(self, deck: Deck) -> None:
        """Given a deck, this method will append the top card to the community cards.
        In other words, this method "deals" the river"""
        self.Cards.append(deck.draw())
        



