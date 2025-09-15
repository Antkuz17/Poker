from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils

class round:
    def __init__(self, minInitBet : int, playerList : list):
        self.minInitBet = minInitBet
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
        print("This round will be a 5/10 structure, meaning the small blind is 5 and the big blind is 10. The next person can only raise by double the minimum")

        # Clarifying who is small and big blind
        print(self.playerList[0].getName() + " is the small blind")
        print(self.playerList[1].getName() + " is the big blind")
        for i in range(2, len(self.playerList)):
            print(self.playerList[i].getName() + " is a regular player")

        # Start of preflop betting

        # This logic only runs if the first player is the is the user, otherwise AI logic will be used
        
        
        # Small blind logic, differs if the small blind is the AI or the user
        if not self.playerList[0].getIsAIPlayer():  # If the small blind is the user
            if(self.playerList[0].getChipStack() < self.minInitBet // 2): # Small blind is half minInitBet
                print("You dont have enough to post small blind, you must go all in.")
                self.playerList[0].setBet(self.playerList[0].getChipStack())
            else: 
                self.playerList[0].setBet(self.minInitBet // 2)  # Small blind is 5
                print("As small blind, " + self.playerList[0].getName() + " posts " + str(self.minInitBet // 2))
        else: # Logic for when the AI player is small blind
            if(self.playerList[0].getChipStack() < self.minInitBet // 2):
                print(self.playerList[0].getName() + " does not have enough to post small blind so they go all in")
                self.playerList[0].setBet(self.playerList[0].getChipStack())
            else:
                self.playerList[0].setBet(self.minInitBet // 2)
                print("As small blind, " + self.playerList[0].getName() + " posts " + str(self.minInitBet // 2))

        # Big blind logic, differs in the same way small blind does
        if not self.playerList[1].getIsAIPlayer():
            if(self.playerList[1].getChipStack() < self.minInitBet): # Big blind is minInitBet (10)
                print("You dont have enough to post big blind, you must go all in.")
                self.playerList[1].setBet(self.playerList[1].getChipStack())
            else: 
                self.playerList[1].setBet(self.minInitBet) # Big blind is 10
                print("As big blind, " + self.playerList[1].getName() + " posts " + str(self.minInitBet))
        else: # Logic for when the AI player is big blind
            if(self.playerList[1].getChipStack() < self.minInitBet):
                print(self.playerList[1].getName() + " does not have enough to post big blind so they go all in")
                self.playerList[1].setBet(self.playerList[1].getChipStack())
            else:
                self.playerList[1].setBet(self.minInitBet)
                print("As big blind, " + self.playerList[1].getName() + " posts " + str(self.minInitBet))

        # Add chips to pot from blinds
        self.pot += self.playerList[0].getBet() + self.playerList[1].getBet()

        # Now start the actual betting round
        currentBet = self.minInitBet  # Current bet to match (starts at big blind amount)
        activePlayers = list(range(len(self.playerList)))  # Track who's still in the hand
        playerToAct = 2  # Start with first player after big blind
        lastRaiser = 1   # Big blind was the last to "raise" (post blind)
        bettingComplete = False

        print(f"Preflop betting begins. Current bet to call: ${currentBet}")

        while not bettingComplete and len(activePlayers) > 1:
            # Skip players who folded
            if playerToAct not in activePlayers:
                playerToAct = (playerToAct + 1) % len(self.playerList)
                continue
                
            currentPlayer = self.playerList[playerToAct]
            
            # Skip if player already has matching bet (unless action hasn't reached them yet)
            if currentPlayer.getBet() == currentBet and playerToAct != lastRaiser:
                playerToAct = (playerToAct + 1) % len(self.playerList)
                continue

            print(f"Action to {currentPlayer.getName()}")
            print(f"Current bet: ${currentBet}, Your bet: ${currentPlayer.getBet()}")
            print(f"You need ${currentBet - currentPlayer.getBet()} to call")

            if not currentPlayer.getIsAIPlayer():  # Human player
                action = ""
                while action not in ["fold", "call", "raise"]:
                    if currentPlayer.getBet() == currentBet:
                        action = input("Options: fold, check, raise: ").lower()
                        if action == "check":
                            action = "call"  # Treat check as call when bet matches
                    else:
                        action = input("Options: fold, call, raise: ").lower()

                if action == "fold":
                    print(f"{currentPlayer.getName()} folds")
                    activePlayers.remove(playerToAct)
                    
                elif action == "call":
                    callAmount = currentBet - currentPlayer.getBet()
                    if currentPlayer.getChipStack() <= callAmount:
                        # All-in call
                        allInAmount = currentPlayer.getChipStack()
                        currentPlayer.setBet(currentPlayer.getBet() + allInAmount)
                        print(f"{currentPlayer.getName()} calls all-in for ${allInAmount}")
                    else:
                        currentPlayer.setBet(currentBet)
                        print(f"{currentPlayer.getName()} calls ${callAmount}")
                    
                elif action == "raise":
                    minRaise = currentBet * 2 - currentPlayer.getBet()  # Minimum raise
                    maxRaise = currentPlayer.getChipStack() + currentPlayer.getBet()  # All-in
                    
                    raiseAmount = utils.inputValidation(
                        input(f"Raise to (min ${minRaise}, max ${maxRaise}): "), int, "+"
                    )
                    
                    if raiseAmount >= maxRaise:
                        currentPlayer.setBet(maxRaise)
                        print(f"{currentPlayer.getName()} raises all-in to ${maxRaise}")
                    else:
                        currentPlayer.setBet(raiseAmount)
                        print(f"{currentPlayer.getName()} raises to ${raiseAmount}")
                    
                    currentBet = currentPlayer.getBet()
                    lastRaiser = playerToAct

            else:  # AI player - simple logic for now
                callAmount = currentBet - currentPlayer.getBet()
                
                if currentPlayer.getChipStack() <= callAmount:
                    # Must go all-in
                    allInAmount = currentPlayer.getChipStack()
                    currentPlayer.setBet(currentPlayer.getBet() + allInAmount)
                    print(f"{currentPlayer.getName()} calls all-in for ${allInAmount}")
                    
                elif callAmount == 0:
                    # Can check
                    print(f"{currentPlayer.getName()} checks")
                    
                else:
                    # Simple AI: call 70% of time, fold 30%
                    import random
                    if random.random() < 0.7:
                        currentPlayer.setBet(currentBet)
                        print(f"{currentPlayer.getName()} calls ${callAmount}")
                    else:
                        print(f"{currentPlayer.getName()} folds")
                        activePlayers.remove(playerToAct)

            # Move to next player
            playerToAct = (playerToAct + 1) % len(self.playerList)
            
            # Check if betting round is complete
            if playerToAct == lastRaiser or len(activePlayers) <= 1:
                bettingComplete = True

        # Calculate final pot
        for player in self.playerList:
            self.pot += player.getBet()
            player.subtractFromChipStack(player.getBet())  # Remove bet from their chip stack

        print(f"\nPreflop betting complete!")
        print(f"Total pot: ${self.pot}")
        print(f"Players remaining: {[self.playerList[i].getName() for i in activePlayers]}")
        
        # Store active players for next betting rounds
        self.activePlayers = activePlayers





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

    newRound = round(5, playerList)
    # while(True):
    #     playerList = kick(playerList)
    #     if len(playerList) < 2:
    #         print(f"{playerList[0].getName()} is the last player remaining and wins the game!")
    #         break
    #     print(f"This is round {roundCounter}, lets begin !!!!")
        
        

main()

