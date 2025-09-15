from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils

class round:
    def __init__(self, minInitBet : int, playerList : list):

        previousBet = 0
        """This constructor will initilize the game by creating a deck and shuffling the cards"""

        self.playerList = playerList
        self.pot = 0 # Before betting begins, the pot is set to 0
        self.deck = Deck() # Creating the Deck object that belongs to the game class
        self.deck.shuffleCards() # Shuffling all the cards in said deck

        drawCards(self.playerList, self.deck) # Drawing 2 cards for each player and appending them to their hand
        
        print("Your hand is: ")
        playerList[0].hand.printHand() # Printing the users hand to the terminal for testing purposes

        print("Starting round")

        # Clarifying who is small and big blind
        print(self.playerList[0].getName() + " is the small blind")
        print(self.playerList[1].getName() + " is the big blind")
        for i in range(2, len(self.playerList)):
            print(self.playerList[i].getName() + " is a regular player")

        # Start of preflop betting

        # This logic only runs if the first player is the is the user, otherwise AI logic will be used
        if not self.playerList[0].getIsAIPlayer():  # If the small blind is the user
            if(self.playerList[0].getChipStack() < minInitBet // 2): # If the user cant match the minimum bet, they must go all in
                print("You dont have enough to be reach required bet, you must go all in.")
                self.playerList[0].setBet(self.playerList[0].getChipStack())
            attemptedBet = utils.inputValidation(
            input(f"Your minimum bet is {minInitBet//2}, how much would you like to bet?: "), int
            )   
            while attemptedBet < minInitBet // 2:
                print(f"Your bet must be at least {minInitBet//2}")
                attemptedBet = utils.inputValidation(
                input(f"Your minimum bet is {minInitBet//2}, how much would you like to bet?: "), int
                )
        # If the first player is the AI, the following code runs
        # else:

        self.playerList[0].setBet(minInitBet // 2) # Small blind posts half the minimum bet

        # # Positions on the table will be based on the index of the player in the playerList list (e.g index 0 = position 1)
        


        

        
        

"""
******LATER RANDOMIZE THE AGGRESSION LEVEL OF THE AI PLAYERS******
"""

def createAIPlayers(playerList: list, numPlayers : int) -> list:
    """This method will create 3 AI players and append them to the playerList, it will then return the new list
    
    The AI players will have a random amount of money between 100-500 and an aggression level of 5
    """
    for(i) in range(numPlayers):
        playerList.append(AIPlayer("Bot" + str(i+1), utils.genRandNum(100, 500), 5))
    return playerList

def newRoundRotation(list: list) -> list:
    """This method is used to "rotate" the index of the playerList order. This means that whatever player was in position
    1 will be in position 2 and position 4 will now be 1"""
    P4 = list.pop()
    list.insert(0, P4)
    return list

def drawCards(playerList: list, deck : Deck) -> None:
    """Will draw 2 cards per player and will append those to each players hand, no return value since the playerList is passed by reference"""
    for i in range(len(playerList)): # For each player
        playerList[i].hand.acceptCard(deck.draw())
        playerList[i].hand.acceptCard(deck.draw())

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

    # Counts the number of rounds played
    roundCounter = 1

    print("***WELCOME TO POKER***")

    userName = input("What is your name?: ")
    money = input("How much money do you have?: ")

    money = utils.inputValidation(money, int, "+") # Validating that the input is an integer and is of proper sign, keeps reprompting till the input is valid

    print(f"Hello, your name is {userName} and you are starting out with ${money}, goodluck!")

    # Initializing the list that will hold all players in the game
    playerList = []

    playerList.append(Player(userName, money)) # For simplicity/testing purposes the player will start as the first player/small blind

    # Validating and getting the number of players from the AI
    numAIPlayers = utils.inputValidation(input("How many players would you like to play against?: "), int, "+")

    # For that will create the AI players and add them to the player list (default money will generate between 200 and 600 and default aggresion is 5)
    for i in range(numAIPlayers):
        playerList.append(AIPlayer(f"Bot {i+1}", utils.genRandNum(200, 600), 5))
        print(playerList[i+1].getName() + f" has joined the game with ${playerList[i+1].getChipStack()}")


    while(True):
        playerList = kick(playerList)
        if len(playerList) < 2:
            print(f"{playerList[0].getName()} is the last player remaining and wins the game!")
            break
        print(f"This is round {roundCounter}, lets begin !!!!")
        
        newRound = round(5, playerList)



    # Creating the AIplayers and appending them to the playerList
    playerList = utils.inputValidation(numAIPlayers, int)






    








    while(True):
        newRound = round(100, 10, playerList)

main()

