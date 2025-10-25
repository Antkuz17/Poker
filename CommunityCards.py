from Card import Card
from Deck import Deck

class CommunityCards:
    def __init__(self) -> None:
        """Constructor for community cards class which stores cards as an list"""
        self.Cards = []

    def printCommunityCards(self) -> None:
        """Prints all of the current community cards to the terminal"""
        for Card in self.Cards:
            print(Card)
    
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
        



