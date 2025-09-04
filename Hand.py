
class Hand:

    # Constructor
    def __init__(self):
        self.Cards = []
    
    # Given a card will place it into the deck
    def acceptCard(self, Card):
        self.Cards.append(Card)

    # Will iterate through the hand and print each card to terminal
    def printHand(self):
        for card in self.Cards:
            print(card)

