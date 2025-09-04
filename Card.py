class Card:

    # Constructor for card
    def __init__(self, rank, suit):
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
    
    
