from Card import Card
from Deck import Deck
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
        
    def suited(self) -> tuple[bool, str]:
        """Returns two distict values held in a tuple type. The first is a boolean telling whether suits 
        of the cards match (2 clubs or 2 hearts). Second value returns the suit of the pair. If there is no pair,
        second value will be None """
        if(self.Cards[0].getSuit() == self.Cards[1].getSuit()):
            print("Match")
            return [True, self.Cards[0].getSuit()]
        else:
            print("No Match")
            return[False, None]

    # The following methods are the calculation methods used to determine the strength of a hand and win percentages

    def preFlopCalc(self, numTrials: int, numOpponenets: int) -> float:
        """Using monte carlo simulation, will estimate the strength of the hand and output a decimal between 0-1 
        with 1 being the a very strong hand and 0 being a very weak hand
        
        The pre flop calculation is simple: hand strength = number of wins / total trials"""

        wins = 0 # Tracks number of times the players hand beats others

        for i in range(numTrials): # For loop that simulates each trial
            deck = Deck()

            wins = 0 # This variable will track the number of wins occur, a win just means that round you finish with the best hand

            #Removes the cards in the hand from the deck since no other person can now have those cards
            deck.removeCard(self.firstCard)
            deck.removeCard(self.secondCard)

            deck.shuffleCards() 

            # For loop that will create i number of hands by using list slicing
            # Works by taking the existing list and creating a new one using syntax list[start:end] (inclusive and exclusive)
            opponent_hands = [deck[i*2:(i+1)*2] for i in range(numOpponenets)]

            # Rough psedocode, if yourname > opponenthand for in i in opponent hands
            
            if ()













    
