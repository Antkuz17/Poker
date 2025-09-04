class Card:

    # Constructor for card
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # Dunder method used to represent a card when a card is printed
    def __str__(self):
        return(f"{self.rank} of {self.suit}")
    
    
    
