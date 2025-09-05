from Card import Card
import random

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
    

    # Iterator method that allows for iteration throught the deck
    # Returns an itererable type when called
    # When called in a loop, this method will return each card in the deck
    def __iter__(self) -> None:
        """Iterator method that allows for iteration throught the deck, returns an itererable type when called"""
        return iter(self.Cards)
    
    def draw(self) -> Card:
        """Returns a card from the top of the deck"""
        return self.Cards.pop()
    
    def shuffleCards(self) -> None:
        """Shuffles the cards within the deck"""
        return random.shuffle(self.Cards)


