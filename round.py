from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils
import random 
from CommunityCards import CommunityCards

"""
round.py

This module contains the 'Hand' class which represents a poker hand
Each hand has a list of card objects that make up the hand which is stored in the 'Cards[]' array

This module includes methods for
- Accepting a card into the hand
- Printing the hand to terminal 
- Getting the first and second card in the hand
- Clearing the hand of all cards
- Getting the list of cards that make up the hand
- Checking if the hand is a pair
- Checking if the hand is suited
"""

class round:
    
    def __init__(self, playerList : list, bb: int, sb: int, userPosition: int) -> None:
        """This constructor will initilize the round by creating a deck and shuffling the cards"""
        self.previousBet = 0
        self.playerList = playerList 
        self.pot = 0 # Before betting begins, the pot is set to 0
        self.deck = Deck() # Creating the Deck object that belongs to the game class
        self.bb = bb # Big blind
        self.sb = sb # Small blind
        self.deck.shuffleCards() # Shuffling all the cards in said deck
        self.userPosition = userPosition # The position of the user in the table
        self.communityCards = CommunityCards() # List that will hold the community cards



    def playPreFlop(self) -> None:
        """Handles the pre-flop betting round logic"""

        print("======================================")
        print("Starting Preflop Logic")
        print("======================================\n")

        # Drawing 2 cards for each player and appending them to their hand
        drawCards(self.playerList, self.deck)

        # Showing the human player their cards
        print(f"Your hand is: {self.playerList[0].hand.firstCard()} and {self.playerList[0].hand.secondCard()}")

        print("\nStarting round")
        print("This round will be a 1/0.5 structure, meaning the small blind is $0.5 and the big blind is $1.")
        print("The minimum raise is double the previous bet\n")

        # Clarifying who is small and big blind
        print(self.playerList[0].getName() + " is the small blind")
        print(self.playerList[1].getName() + " is the big blind")
        for i in range(2, len(self.playerList)):
            print(self.playerList[i].getName() + " is a regular player")
        
        print()

        # Start of preflop betting - posting blinds
        # Small blind posts their forced bet
        self.playerList[0].setBet(self.sb)
        print(self.playerList[0].getName() + " posts small blind: $" + str(self.sb))

        # Big blind posts their forced bet
        self.playerList[1].setBet(self.bb)
        print(self.playerList[1].getName() + " posts big blind: $" + str(self.bb))

        # Adding blinds to the pot
        self.pot += self.playerList[0].getBet() + self.playerList[1].getBet()
        print("Pot: $" + str(self.pot) + "\n")

        # The current bet to match is the big blind
        self.previousBet = self.bb
        
        # Track the last player to raise (used to know when betting round is complete)
        lastRaiserIndex = 1  # Start with big blind as last raiser
        
        # Keep track of who has acted this round
        playersActed = [False] * len(self.playerList)
        playersActed[0] = False  # Small blind needs to act again if there's a raise
        playersActed[1] = False  # Big blind needs to act again if there's a raise
        
        # Betting continues until all active players have matched the current bet
        currentPlayerIndex = 2  # Start with player after big blind
        
        # Continue betting until we circle back to the last raiser
        while True:
            # Get the current player
            player = self.playerList[currentPlayerIndex]
            
            # Skip if player has folded
            if player.getFoldStatus():
                currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
                # Check if we've completed the round (back to last raiser)
                if currentPlayerIndex == (lastRaiserIndex + 1) % len(self.playerList):
                    break
                continue
            
            # Skip if player has already matched the current bet and no one raised after them
            if playersActed[currentPlayerIndex] and player.getBet() == self.previousBet:
                currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
                # Check if we've completed the round
                if currentPlayerIndex == (lastRaiserIndex + 1) % len(self.playerList):
                    break
                continue
            
            # Calculate how much the player needs to call
            amountToCall = self.previousBet - player.getBet()
            
            print(f"\n{player.getName()}'s turn (current bet: ${player.getBet()}, needs ${amountToCall} to call)")
            
            # Handle AI player action
            if player.getIsAIPlayer():
                # Generate random number to determine AI action
                num = random.randint(1, 9)
                
                # 40% chance to call
                if num <= 4:
                    player.setBet(self.previousBet)
                    self.pot += amountToCall
                    playersActed[currentPlayerIndex] = True
                    print(f"{player.getName()} calls ${amountToCall}")
                
                # 10% chance to raise
                elif num == 5:
                    raiseAmount = self.previousBet * 2
                    additionalAmount = raiseAmount - player.getBet()
                    player.setBet(raiseAmount)
                    self.pot += additionalAmount
                    self.previousBet = raiseAmount
                    lastRaiserIndex = currentPlayerIndex
                    playersActed[currentPlayerIndex] = True
                    # Reset acted status for players before this one (they need to respond to raise)
                    for i in range(len(playersActed)):
                        if i != currentPlayerIndex:
                            playersActed[i] = False
                    print(f"{player.getName()} raises to ${raiseAmount}")
                
                # 50% chance to fold
                else:
                    player.setFoldStatus(True)
                    playersActed[currentPlayerIndex] = True
                    print(f"{player.getName()} folds")
            
            # Handle human player action
            else:
                validAction = False
                while not validAction:
                    # Prompt for action
                    action = input(f"Fold, call ${amountToCall}, or raise? (f/c/r): ").lower()
                    
                    # Handle fold
                    if action == "f" or action == "fold":
                        player.setFoldStatus(True)
                        playersActed[currentPlayerIndex] = True
                        print(f"{player.getName()} folds")
                        validAction = True
                    
                    # Handle call
                    elif action == "c" or action == "call":
                        player.setBet(self.previousBet)
                        self.pot += amountToCall
                        playersActed[currentPlayerIndex] = True
                        print(f"{player.getName()} calls ${amountToCall}")
                        validAction = True
                    
                    # Handle raise
                    elif action == "r" or action == "raise":
                        minimumRaise = self.previousBet * 2
                        raiseAmount = utils.inputValidation(
                            input(f"Raise to (minimum ${minimumRaise}): "), 
                            int, 
                            "+"
                        )
                        
                        # Validate raise amount
                        if raiseAmount < minimumRaise:
                            print(f"Raise amount must be at least ${minimumRaise} (double the current bet)")
                        else:
                            additionalAmount = raiseAmount - player.getBet()
                            player.setBet(raiseAmount)
                            self.pot += additionalAmount
                            self.previousBet = raiseAmount
                            lastRaiserIndex = currentPlayerIndex
                            playersActed[currentPlayerIndex] = True
                            # Reset acted status for players before this one
                            for i in range(len(playersActed)):
                                if i != currentPlayerIndex:
                                    playersActed[i] = False
                            print(f"{player.getName()} raises to ${raiseAmount}")
                            validAction = True
                    
                    # Invalid input
                    else:
                        print("Invalid input. Please enter 'f' (fold), 'c' (call), or 'r' (raise)")
            
            # Show current pot after each action
            print(f"Pot: ${self.pot}")
            
            # Move to next player
            currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
            
            # Check if we've completed the betting round
            # Round is complete when we return to the player after the last raiser
            # and all active players have acted and matched the bet
            if currentPlayerIndex == (lastRaiserIndex + 1) % len(self.playerList):
                allMatched = True
                for i, player in enumerate(self.playerList):
                    if not player.getFoldStatus() and (not playersActed[i] or player.getBet() != self.previousBet):
                        allMatched = False
                        break
                if allMatched:
                    break
        
        print("\n======================================")
        print("Preflop betting round complete")
        print(f"Final pot: ${self.pot}")
        print("======================================\n")
        

    def playFlop(self) -> None:
        """Handles the flop betting round logic"""
        
        print("\n======================================")
        print("Starting Flop")
        print("======================================\n")
        
        # Check if only one player remains (everyone else folded)
        activePlayers = [p for p in self.playerList if not p.getFoldStatus()]
        if len(activePlayers) == 1:
            print(f"{activePlayers[0].getName()} wins by default (all others folded)!")
            activePlayers[0].setChipStack(activePlayers[0].getChipStack() + self.pot)
            print(f"{activePlayers[0].getName()} wins ${self.pot}")
            return
        
        # Deal the flop
        print("Dealing the Flop...")
        self.communityCards.dealFlop(self.deck)
        self.communityCards.printCommunityCards()
        print()
        
        # Reset all player bets for this new betting round
        for player in self.playerList:
            player.setBet(0)
        
        # Reset current bet amount for the new round
        self.previousBet = 0
        
        # Track who has acted this round
        hasActed = [False] * len(self.playerList)
        
        # Post-flop betting starts with small blind (position 0)
        currentPlayerIndex = 0
        
        # Find first active player to start betting
        while self.playerList[currentPlayerIndex].getFoldStatus():
            currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
        
        firstPlayerIndex = currentPlayerIndex
        
        # Main Betting loop
        while True:
            player = self.playerList[currentPlayerIndex]
            
            # Skip folded players
            if player.getFoldStatus():
                hasActed[currentPlayerIndex] = True
                currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
                continue
            
            # Check if betting round is complete
            # Round ends when all active players have acted and matched the current bet or folded
            allDone = True
            for i, p in enumerate(self.playerList):
                if not p.getFoldStatus():
                    if not hasActed[i] or p.getBet() != self.previousBet:
                        allDone = False
                        break
            
            if allDone:
                break
            
            # Skip if player already matched current bet and has acted
            if hasActed[currentPlayerIndex] and player.getBet() == self.previousBet:
                currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
                continue
            
            # Calculate amount to call
            amountToCall = self.previousBet - player.getBet()
            
            print(f"\n{player.getName()}'s turn (Stack: ${player.getChipStack()}, Current bet: ${player.getBet()}, Pot: ${self.pot})")
            
            # AI Player logic
            if player.getIsAIPlayer():
                num = random.randint(1, 10)
                
                # If there's no bet yet, AI can check or bet
                if self.previousBet == 0:
                    if num <= 6:  # Check (60%)
                        print(f"{player.getName()} checks")
                    elif num <= 8:  # Bet (20%)
                        betAmount = self.bb  # Bet one big blind
                        if player.getChipStack() >= betAmount:
                            player.setChipStack(player.getChipStack() - betAmount)
                            player.setBet(betAmount)
                            self.pot += betAmount
                            self.previousBet = betAmount
                            # Reset acted status for other players
                            for i in range(len(hasActed)):
                                if i != currentPlayerIndex:
                                    hasActed[i] = False
                            print(f"{player.getName()} bets ${betAmount}")
                        else:
                            print(f"{player.getName()} checks (not enough chips to bet)")
                    else:  # Fold (20%)
                        player.setFoldStatus(True)
                        print(f"{player.getName()} folds")
                
                # If there's a bet to call
                else:
                    if num <= 4:  # Call (40%)
                        if player.getChipStack() >= amountToCall:
                            player.setChipStack(player.getChipStack() - amountToCall)
                            player.setBet(self.previousBet)
                            self.pot += amountToCall
                            print(f"{player.getName()} calls ${amountToCall}")
                        else:
                            player.setFoldStatus(True)
                            print(f"{player.getName()} folds (not enough chips)")
                    
                    elif num <= 5:  # Raise (10%)
                        raiseAmount = self.previousBet * 2
                        additionalAmount = raiseAmount - player.getBet()
                        if player.getChipStack() >= additionalAmount:
                            player.setChipStack(player.getChipStack() - additionalAmount)
                            player.setBet(raiseAmount)
                            self.pot += additionalAmount
                            self.previousBet = raiseAmount
                            # Reset acted status
                            for i in range(len(hasActed)):
                                if i != currentPlayerIndex:
                                    hasActed[i] = False
                            print(f"{player.getName()} raises to ${raiseAmount}")
                        else:
                            # Not enough to raise, just call if possible
                            if player.getChipStack() >= amountToCall:
                                player.setChipStack(player.getChipStack() - amountToCall)
                                player.setBet(self.previousBet)
                                self.pot += amountToCall
                                print(f"{player.getName()} calls ${amountToCall}")
                            else:
                                player.setFoldStatus(True)
                                print(f"{player.getName()} folds (not enough chips)")
                    
                    else:  # Fold (50%)
                        player.setFoldStatus(True)
                        print(f"{player.getName()} folds")
                
                hasActed[currentPlayerIndex] = True
            
            # Human player logic
            else:
                validAction = False
                while not validAction:
                    # If no bet, player can check or bet
                    if self.previousBet == 0:
                        action = input(f"Check, bet, or fold? (ch/b/f): ").lower()
                        
                        if action in ["ch", "check"]:
                            print(f"{player.getName()} checks")
                            validAction = True
                        
                        elif action in ["b", "bet"]:
                            minimumBet = self.bb
                            betAmount = utils.inputValidation(
                                input(f"Bet amount (minimum ${minimumBet}): "),
                                int,
                                "+"
                            )
                            
                            if betAmount < minimumBet:
                                print(f"Bet must be at least ${minimumBet}")
                            elif player.getChipStack() < betAmount:
                                print(f"Not enough chips! You only have ${player.getChipStack()}")
                            else:
                                player.setChipStack(player.getChipStack() - betAmount)
                                player.setBet(betAmount)
                                self.pot += betAmount
                                self.previousBet = betAmount
                                # Reset acted status
                                for i in range(len(hasActed)):
                                    if i != currentPlayerIndex:
                                        hasActed[i] = False
                                print(f"{player.getName()} bets ${betAmount}")
                                validAction = True
                        
                        elif action in ["f", "fold"]:
                            player.setFoldStatus(True)
                            print(f"{player.getName()} folds")
                            validAction = True
                        
                        else:
                            print("Invalid input. Please enter 'ch' (check), 'b' (bet), or 'f' (fold)")
                    
                    # If there's a bet to match
                    else:
                        action = input(f"Call ${amountToCall}, raise, or fold? (c/r/f): ").lower()
                        
                        if action in ["c", "call"]:
                            if player.getChipStack() < amountToCall:
                                print(f"Not enough chips! You only have ${player.getChipStack()}")
                                continue
                            player.setChipStack(player.getChipStack() - amountToCall)
                            player.setBet(self.previousBet)
                            self.pot += amountToCall
                            print(f"{player.getName()} calls ${amountToCall}")
                            validAction = True
                        
                        elif action in ["r", "raise"]:
                            minimumRaise = self.previousBet * 2
                            raiseAmount = utils.inputValidation(
                                input(f"Raise to (minimum ${minimumRaise}): "),
                                int,
                                "+"
                            )
                            
                            if raiseAmount < minimumRaise:
                                print(f"Raise must be at least ${minimumRaise}")
                            else:
                                additionalAmount = raiseAmount - player.getBet()
                                if player.getChipStack() < additionalAmount:
                                    print(f"Not enough chips! You only have ${player.getChipStack()}")
                                    continue
                                
                                player.setChipStack(player.getChipStack() - additionalAmount)
                                player.setBet(raiseAmount)
                                self.pot += additionalAmount
                                self.previousBet = raiseAmount
                                # Reset acted status
                                for i in range(len(hasActed)):
                                    if i != currentPlayerIndex:
                                        hasActed[i] = False
                                print(f"{player.getName()} raises to ${raiseAmount}")
                                validAction = True
                        
                        elif action in ["f", "fold"]:
                            player.setFoldStatus(True)
                            print(f"{player.getName()} folds")
                            validAction = True
                        
                        else:
                            print("Invalid input. Please enter 'c' (call), 'r' (raise), or 'f' (fold)")
                
                hasActed[currentPlayerIndex] = True
            
            print(f"Pot: ${self.pot}")
            
            # Move to next player
            currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
        
        print("\n======================================")
        print("Flop betting round complete")
        print(f"Final pot: ${self.pot}")
        print("======================================\n")







        

    def playTurn(self) -> None:
        """Handles the turn betting round logic"""
        pass    

    def playRiver(self) -> None:
        """Handles the river betting round logic"""
        pass

    def playShowdown(self) -> None:
        """Handles the showdown logic where players reveal their hands and the winner is determined"""
        pass

        


        



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


    



