from Card import Card
class CommunityCards:
    def __init__(self) -> None:
        """Constructor for community cards class which stores cards as an list"""
        self.Cards = []

    def acceptCard(self, Card: Card) -> None:
        self.Cards.append(Card)

    def printCommunityCards(self) -> None:
        """Prints all of the current community cards to the terminal"""
        for Card in self.Cards:
            print(Card)
    
    



