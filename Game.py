from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
from HumanPlayer import HumanPlayer
import utils

class game:
    def __init__(self, buyIn, minBet):
        """This constructor will initilize the game by creating a deck, shuffling the cards, and creating players"""

        print("***WELCOME TO POKER***")

        self.pot = 0 # Before betting begins, the pot is set to 0

        self.deck = Deck() # Creating the Deck object that belongs to the game class
        self.deck.shuffleCards() # Shuffling all the cards in said deck

        playerList = []

        userName = input("What is your name?: ")
        money = input("How much money do you have?: ")
        
        utils.inputValidation(money, int)

        

        playerList.append(HumanPlayer(userName, money, 0)) # Players name is buster, starts with 1000 dollars

        
        playerList = createAIPlayers(playerList)

        # # Generating random values of chips for each player
        # for i in range(len(playerList)):
        #     playerList[i].setChipStack(utils.genRandNum(100, 500)) # Generating a random chipstack for each player between 100-500 dollars
        #     print(f"{playerList[i].getName()} has a chipstack of {playerList[i].getChipStack()}")

        # playerList = drawCards(playerList)

        # playerList[0].printHand()

        # # Positions on the table will be based on the index of the player in the playerList list (e.g index 0 = position 1)
        


        

        
        



def createAIPlayers(list: list) -> list:

    AI1 = AIPlayer("Bot1", 0, 0, 5)
    list.append(AI1)
    AI2 = AIPlayer("Bot2", 0, 0, 5)
    list.append(AI2)
    AI3 = AIPlayer("Bot3", 0, 0, 5)
    list.append(AI3)
    return list

def newRoundRotation(list: list) -> list:
    """This method is used to "rotate" the index of the playerList order. This means that whatever player was in position
    1 will be in position 2 and position 4 will now be 1"""
    P4 = list.pop()
    return(list.insert(0, P4))

def drawCards(playerList: list) -> list:
    """Will draw 2 cards per player and will append those to each players hand"""
    for i in range(len(list)): # For each player
        list[i].acceptHand(game.deck.draw())
        list[i].acceptHand(game.deck.draw())

    return playerList
    





def main():
    newGame = game(100, 2)

main()

