from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils

class round:
    def __init__(self, buyIn : int, minInitBet : int, playerList : list):
        """This constructor will initilize the game by creating a deck and shuffling the cards"""

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
        # If the first player is the AI, the follwing code runs
        # else:
            
            

        

        




        self.playerList[0].setBet(minInitBet // 2) # Small blind posts half the minimum bet




        



        

        # # Positions on the table will be based on the index of the player in the playerList list (e.g index 0 = position 1)
        


        

        
        

"""
******LATER RANDOMIZE THE AGGRESSION LEVEL OF THE AI PLAYERS******
"""

def createAIPlayers(playerList: list, numPlayers : int) -> list:
    """This method will create 3 AI players and append them to the playerList"""
    for(i) in range(numPlayers):
        playerList.append(AIPlayer("Bot" + str(i+1), utils.genRandNum(100, 500), 5))
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

    # Counts the number of rounds played
    roundCounter = 1

    print("***WELCOME TO POKER***")
    print("This is round " + str(roundCounter))

    # Validating that the input is an integer and is positive
    while(True):
        numAIPlayers = utils.inputValidation(input("How many players would you like to play against?: "), int)
        if(numAIPlayers > 0):
            break
        else:
            print("Invalid input, cant have negative")

    # Initializing the list that will hold all players in the game
    playerList = []

    # Creating the AIplayers and appending them to the playerList
    playerList = utils.inputValidation(numPlayers, int) 



    








    while(True):
        newRound = round(100, 10, playerList)

main()

