from Card import Card
from Deck import Deck
from Hand import Hand

class game:

    def __init__(self, numPlayers, buyIn, minBet, pot):
        self.pot = 0 # Before betting begins, the pot is set to 0
        deck = Deck() # Creating the Deck
        deck.ShuffleCards() # Shuffling all the cards



        p1Hand = Hand()
        p1Hand.acceptCard(deck.PullCard())
        p1Hand.acceptCard(deck.PullCard())

        p1Hand.printHand()

        p1Hand.getSuit()
        
        




def main():
    newGame = game(5, 100, 2, 0)

main()

