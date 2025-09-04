from Card import Card
from Deck import Deck

# Main game loop for each poker round
def main():
    deck = Deck() #Creating the Deck
    deck.ShuffleCards() # Shuffling all the cards
    for card in deck:
        print(card)


main()

