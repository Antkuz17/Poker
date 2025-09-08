from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils

class game:
    def __init__(self, buyIn, minBet):
        """This constructor will initilize the game by creating a deck, shuffling the cards, and creating players"""

        print("***WELCOME TO POKER***")

        self.pot = 0 # Before betting begins, the pot is set to 0

        self.deck = Deck() # Creating the Deck object that belongs to the game class
        self.deck.shuffleCards() # Shuffling all the cards in said deck

        self.playerList = []

        userName = input("What is your name?: ")
        money = input("How much money do you have?: ")

        money = utils.inputValidation(money, int) # Validating that the input is an integer keeps reprompting till the input is valid

        print(f"Hello, your name is {userName} and you are starting out with ${money}, goodluck!") # Delete this later

        self.playerList.append(Player(userName, money)) # For texting purposes the player will start as the first player/small blind

        self.playerList = createAIPlayers(self.playerList) # Creating 3 AI players and appending them to the playerList

        self.playerList = kick(self.playerList)

        print("The following players are in the game:") # Mostly for testing purposes but this introduces the players
        for i in range(len(self.playerList)):
            print(f"{self.playerList[i].getName()} has a chipstack of {self.playerList[i].getChipStack()}")

        self.playerList = drawCards(self.playerList, self.deck) # Drawing 2 cards for each player and appending them to their hand
        
        print("Your hand is: ")
        self.playerList[0].hand.printHand() # Printing the users hand to the terminal for testing purposes

        print("Starting round")

        # Clarifying who is small and big blind
        print(self.playerList[0].getName() + " is the small blind")
        print(self.playerList[1].getName() + " is the big blind")
        print(self.playerList[2].getName() + " is a regular player")
        print(self.playerList[3].getName() + " is a regular player")

        attemptedBet = 0
        # Start of preflop betting

        # This logic only runs if the first player is the is the user, otherwise AI logic will be used
        if not self.playerList[0].getIsAIPlayer():  # If the small blind is the user
            if(self.playerList[0].getChipStack() < minBet // 2): # If the user cant match the minimum bet, they must go all in
                print("You dont have enough to be reach required bet, you must go all in.")
                self.playerList[0].setBet(self.playerList[0].getChipStack())
            attemptedBet = utils.inputValidation(
            input(f"Your minimum bet is {minBet//2}, how much would you like to bet?: "), int
            )   
            while attemptedBet < minBet // 2:
                print(f"Your bet must be at least {minBet//2}")
                attemptedBet = utils.inputValidation(
                input(f"Your minimum bet is {minBet//2}, how much would you like to bet?: "), int
                )
        # If the first player is the AI, the follwing code runs
        # else:
            
            

        

        




        self.playerList[0].setBet(minBet // 2) # Small blind posts half the minimum bet




        



        

        # # Positions on the table will be based on the index of the player in the playerList list (e.g index 0 = position 1)
        


        

        
        



def createAIPlayers(playerList: list) -> list:
    """This method will create 3 AI players and append them to the playerList"""
    AI1 = AIPlayer("Bot1", utils.genRandNum(100, 500), 5)
    playerList.append(AI1)
    AI2 = AIPlayer("Bot2", utils.genRandNum(100, 500), 5)
    playerList.append(AI2)
    AI3 = AIPlayer("Bot3", utils.genRandNum(100, 500), 5)
    playerList.append(AI3)
    return playerList

def newRoundRotation(list: list) -> list:
    """This method is used to "rotate" the index of the playerList order. This means that whatever player was in position
    1 will be in position 2 and position 4 will now be 1"""
    P4 = list.pop()
    list.insert(0, P4)
    return list

def drawCards(playerList: list, deck : Deck) -> list:
    """Will draw 2 cards per player and will append those to each players hand"""
    for i in range(len(playerList)): # For each player
        playerList[i].hand.acceptCard(deck.draw())
        playerList[i].hand.acceptCard(deck.draw())

    return playerList

def kick(playerList: list) -> list:
    """Remove players with 0 chips from the game by going though the player list and checking their chipstack.
    Function will return a new list with only players that have money"""
    remainingPlayers = []
    for player in playerList:
        if player.getChipStack() == 0:
            print(f"{player.getName()} has no money and is kicked from the game")
        else:
            remainingPlayers.append(player)
    return remainingPlayers


    





def main():
    newGame = game(100, 10)

main()

