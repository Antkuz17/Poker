from Card import Card
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
    
    def __iter__(self):
        return iter(self.Cards)

