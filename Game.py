from Card import Card
from Deck import Deck
from Hand import Hand

class game:

    def __init__(self, numPlayers, buyIn, minBet):
        deck = Deck() # Creating the Deck
        deck.ShuffleCards() # Shuffling all the cards

        for player in numPlayers:
            player


        p1Hand = Hand()
        p1Hand.acceptCard(deck.PullCard())

        p1Hand.printHand()




def main():
    newGame = game(5, 100, 2)

main()

