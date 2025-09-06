from Card import Card
class Hand:

    # Constructor
    def __init__(self) -> None:
        """Constructor for hand class, stores all cards as an list"""
        self.Cards = []
    
    def acceptCard(self, Card: Card) -> None:
        """Given a card object, that object will be appended to the list of cards that makes up the hand"""
        self.Cards.append(Card)

    def printHand(self) -> None:
        """Will iterate throught the cards list and print to terminal"""
        for card in self.Cards:
            print(card)

    def firstCard(self) -> Card:
        """Returns the first card in the hand"""
        return self.Cards[0]
    
    def secondCard(self) -> Card:
        """Returns the second card in the hand"""
        return self.Cards[1]

    def clearHand(self) -> None:
        """Will clear the hand of all cards"""
        self.Cards.clear()

    def getPair(self) -> tuple[bool,str]:
        """Returns two distict values held in a tuple type. The first is a boolean telling whether the hand
        has a pair (pair of 2's, Aces, kings, etc). Second value returns the rank of the pair. If there is no pair,
        second value will be None """
        if(self.Cards[0].getRank() == self.Cards[1].getRank()):
            return [True, self.Cards[0].getRank()]
        else:
            return[False, None]
        
    def getSuit(self) -> tuple[bool, str]:
        """Returns two distict values held in a tuple type. The first is a boolean telling whether suits 
        of the cards match (2 clubs or 2 hearts). Second value returns the suit of the pair. If there is no pair,
        second value will be None """
        if(self.Cards[0].getSuit() == self.Cards[1].getSuit()):
            print("Match")
            return [True, self.Cards[0].getSuit()]
        else:
            print("No Match")
            return[False, None]


    
