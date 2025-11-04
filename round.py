from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils
import random 
from CommunityCards import CommunityCards
from HandEvaluator import HandEvaluator

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
    
    def __init__(self, playerList : list, bb: float, sb: float) -> None:
        """This constructor will initilize the round by creating a deck and shuffling the cards"""
        self.previousBet = 0
        self.playerList = playerList 
        self.pot = 0 # Before betting begins, the pot is set to 0
        self.deck = Deck() # Creating the Deck object that belongs to the game class
        self.bb = bb # Big blind
        self.sb = sb # Small blind
        self.deck.shuffleCards() # Shuffling all the cards in said deck
        self.communityCards = CommunityCards() # List that will hold the community cards



    def playPreFlop(self) -> None:
        """Handles the pre-flop betting round logic"""

        print("======================================")
        print("Starting Preflop Logic")
        print("======================================\n")

        # Giving each player 2 cards
        self._dealHoleCards()

        # Show human player their cards
        print(f"Your hand is: {self.playerList[0].hand.firstCard()} and {self.playerList[0].hand.secondCard()}")

        # Printing round introduction
        print("\nStarting round")
        print(f"This round will be a {self.bb}/{self.sb} structure")
        print("The minimum raise is double the previous bet\n")

        # Printing positions
        print(f"{self.playerList[0].getName()} is the small blind")
        print(f"{self.playerList[1].getName()} is the big blind")
        for i in range(2, len(self.playerList)):
            print(f"{self.playerList[i].getName()} is a regular player")
        print()

        # Post blinds
        self._postBlinds()
        
        # Run pre-flop betting
        self._runBettingRound(startIndex=2)
        
        print("\n======================================")
        print("Preflop betting round complete")
        print(f"Final pot: ${self.pot}")
        print("======================================\n")


        
    def playFlop(self) -> None:
        """Handles the flop betting round logic"""
        
        # Check if only one player remains (everyone else folded)
        if self._countActivePlayers() <= 1:
            print("All other players have folded!")
            return
        
        print("======================================")
        print("Starting Flop")
        print("======================================\n")
        
        # Burn one card and deal 3 community cards
        self.deck.draw()  # Burn card
        self.communityCards.dealFlop(self.deck)
        
        # Display community cards
        self.communityCards.printCommunityCards()
        print()
        
        # Reset bets for new betting round
        self.previousBet = 0
        for player in self.playerList:
            player.setBet(0)
        
        # Run flop betting (start with small blind - index 0)
        self._runBettingRound(startIndex=0)
        
        print("\n======================================")
        print("Flop betting round complete")
        print(f"Final pot: ${self.pot}")
        print("======================================\n")
    
    def playTurn(self) -> None:
        """Handles the turn betting round logic"""
        
        # Check if only one player remains
        if self._countActivePlayers() <= 1:
            print("All other players have folded!")
            return
        
        print("======================================")
        print("Starting Turn")
        print("======================================\n")
        
        # Burn one card and deal 1 community card
        self.deck.draw()  # Burn card
        self.communityCards.dealTurn(self.deck)
        
        # Display community cards
        self.communityCards.printCommunityCards()
        print()
        
        # Reset bets for new betting round
        self.previousBet = 0
        for player in self.playerList:
            player.setBet(0)
        
        # Run turn betting
        self._runBettingRound(startIndex=0)
        
        print("\n======================================")
        print("Turn betting round complete")
        print(f"Final pot: ${self.pot}")
        print("======================================\n")
    
    def playRiver(self) -> None:
        """Handles the river betting round logic"""
        
        # Check if only one player remains
        if self._countActivePlayers() <= 1:
            print("All other players have folded!")
            return
        
        print("======================================")
        print("Starting River")
        print("======================================\n")
        
        # Burn one card and deal 1 community card
        self.deck.draw()  # Burn card
        self.communityCards.dealRiver(self.deck)
        
        # Display community cards
        self.communityCards.printCommunityCards()
        print()
        
        # Reset bets for new betting round
        self.previousBet = 0
        for player in self.playerList:
            player.setBet(0)
        
        # Run river betting
        self._runBettingRound(startIndex=0)
        
        print("\n======================================")
        print("River betting round complete")
        print(f"Final pot: ${self.pot}")
        print("======================================\n")
    
    def playShowdown(self) -> None:
        """Handles the showdown logic where players reveal hands and winner is determined"""
        
        print("======================================")
        print("SHOWDOWN")
        print("======================================\n")
        
        # Get all players who haven't folded
        activePlayers = [p for p in self.playerList if not p.getFoldStatus()]
        
        if len(activePlayers) == 1:
            # Only one player left - they win by default
            winner = activePlayers[0]
            print(f"{winner.getName()} wins the pot of ${self.pot} (everyone else folded)")
            winner.setChipStack(winner.getChipStack() + self.pot)
        else:
            # Multiple players - evaluate hands
            print("Revealing hands...\n")
            
            # Evaluate each player's hand
            playerHands = []
            communityCardsList = self.communityCards.getCommunityCards()
            
            for player in activePlayers:
                holeCards = player.hand.getCards()
                evaluatedHand = HandEvaluator.evaluateBestHand(holeCards, communityCardsList)
                playerHands.append((player, evaluatedHand))
                
                # Show each player's cards and hand
                print(f"{player.getName()}'s hole cards: {holeCards[0]} and {holeCards[1]}")
                print(f"  {HandEvaluator.formatHandDescription(evaluatedHand, player.getName())}\n")
            
            # Find the winner(s)
            winners = [playerHands[0]]
            
            for i in range(1, len(playerHands)):
                comparison = HandEvaluator.compareHands(playerHands[i][1], winners[0][1])
                
                if comparison > 0:
                    # New best hand found
                    winners = [playerHands[i]]
                elif comparison == 0:
                    # Tie with current best
                    winners.append(playerHands[i])
            
            # Award pot
            print("="*50)
            if len(winners) == 1:
                winner = winners[0][0]
                print(f"\n🏆 {winner.getName()} WINS THE POT OF ${self.pot}! 🏆\n")
                winner.setChipStack(winner.getChipStack() + self.pot)
            else:
                # Split pot
                splitAmount = self.pot / len(winners)
                winnerNames = [w[0].getName() for w in winners]
                print(f"\n🤝 SPLIT POT between {', '.join(winnerNames)}!")
                print(f"Each player receives ${splitAmount:.2f}\n")
                
                for winner, _ in winners:
                    winner.setChipStack(winner.getChipStack() + splitAmount)
            
            print("="*50)


    def _dealHoleCards(self) -> None:
        """Deals two cards to each player in the game"""

        for player in self.playerList:
            player.hand.acceptCard(self.deck.draw())
            player.hand.acceptCard(self.deck.draw())


    def _postBlinds(self) -> None:
        """Have small blind and big blind post their forced bets"""
        # Small blind
        self.playerList[0].setBet(self.sb)
        self.playerList[0].setChipStack(self.playerList[0].getChipStack() - self.sb)
        print(f"{self.playerList[0].getName()} posts small blind: ${self.sb}")
        
        # Big blind
        self.playerList[1].setBet(self.bb)
        self.playerList[1].setChipStack(self.playerList[1].getChipStack() - self.bb)
        print(f"{self.playerList[1].getName()} posts big blind: ${self.bb}")
        
        # Add blinds to pot
        self.pot += self.sb + self.bb
        self.previousBet = self.bb
        print(f"Pot: ${self.pot}\n")

    def _runBettingRound(self, startIndex: int) -> None:
            """Run a complete betting round
            
            Args:
                startIndex: Index of player who acts first
            """
            # Track who has acted
            hasActed = [False] * len(self.playerList)
            currentPlayerIndex = startIndex
            
            # Continue until all active players have acted and matched the current bet
            while not self._isBettingComplete(hasActed):
                player = self.playerList[currentPlayerIndex]
                
                # Skip folded players
                if player.getFoldStatus():
                    hasActed[currentPlayerIndex] = True
                    currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
                    continue
                
                # Skip if already acted and bet is matched
                if hasActed[currentPlayerIndex] and player.getBet() == self.previousBet:
                    currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
                    continue
                
                # Calculate amount to call
                amountToCall = self.previousBet - player.getBet()
                
                # Handle player action
                if player.getIsAIPlayer():
                    self._handleAIAction(player, currentPlayerIndex, amountToCall, hasActed)
                else:
                    self._handleHumanAction(player, currentPlayerIndex, amountToCall, hasActed)
                
                hasActed[currentPlayerIndex] = True
                print(f"Pot: ${self.pot}\n")
                
                # Move to next player
                currentPlayerIndex = (currentPlayerIndex + 1) % len(self.playerList)
            
    def _isBettingComplete(self, hasActed: list) -> bool:
            """Check if betting round is complete
            
            Returns:
                True if all active players have acted and matched the bet
            """
            for i, player in enumerate(self.playerList):
                # Skip folded players
                if player.getFoldStatus():
                    continue
                
                # If player hasn't acted, betting not complete
                if not hasActed[i]:
                    return False
                
                # If player hasn't matched current bet, betting not complete
                if player.getBet() != self.previousBet:
                    return False
            
            return True
        
    def _handleAIAction(self, player, playerIndex: int, amountToCall: float, hasActed: list) -> None:
        """Handle AI player action
        
        Args:
            player: The AI player
            playerIndex: Index of player in playerList
            amountToCall: Amount needed to call
            hasActed: List tracking who has acted
        """
        print(f"\n{player.getName()}'s turn (current bet: ${player.getBet()}, needs ${amountToCall} to call)")
        
        # Simple AI logic
        action = random.randint(1, 10)
        
        # 40% call
        if action <= 4 and amountToCall > 0:
            if player.getChipStack() >= amountToCall:
                player.setChipStack(player.getChipStack() - amountToCall)
                player.setBet(self.previousBet)
                self.pot += amountToCall
                print(f"{player.getName()} calls ${amountToCall}")
            else:
                player.setFoldStatus(True)
                print(f"{player.getName()} folds (not enough chips)")
        
        # 10% raise
        elif action == 5:
            raiseAmount = self.previousBet * 2 if self.previousBet > 0 else self.bb
            additionalAmount = raiseAmount - player.getBet()
            
            if player.getChipStack() >= additionalAmount:
                player.setChipStack(player.getChipStack() - additionalAmount)
                player.setBet(raiseAmount)
                self.pot += additionalAmount
                self.previousBet = raiseAmount
                
                # Reset acted status for all other players
                for i in range(len(hasActed)):
                    if i != playerIndex:
                        hasActed[i] = False
                
                print(f"{player.getName()} raises to ${raiseAmount}")
            else:
                # Not enough to raise, just call or fold
                if amountToCall > 0 and player.getChipStack() >= amountToCall:
                    player.setChipStack(player.getChipStack() - amountToCall)
                    player.setBet(self.previousBet)
                    self.pot += amountToCall
                    print(f"{player.getName()} calls ${amountToCall}")
                else:
                    player.setFoldStatus(True)
                    print(f"{player.getName()} folds")
        
        # 50% fold or check
        else:
            if amountToCall == 0:
                print(f"{player.getName()} checks")
            else:
                player.setFoldStatus(True)
                print(f"{player.getName()} folds")

    def _handleHumanAction(self, player, playerIndex: int, amountToCall: float, hasActed: list) -> None:
        """Handle human player action
        
        Args:
            player: The human player
            playerIndex: Index of player in playerList
            amountToCall: Amount needed to call
            hasActed: List tracking who has acted
        """
        print(f"\n{player.getName()}'s turn")
        print(f"Your chips: ${player.getChipStack()}")
        print(f"Current bet: ${player.getBet()}")
        
        if amountToCall > 0:
            print(f"Amount to call: ${amountToCall}")
        
        validAction = False
        while not validAction:
            if amountToCall == 0:
                action = input("Check, bet, or fold? (ch/b/f): ").lower()
            else:
                action = input(f"Call ${amountToCall}, raise, or fold? (c/r/f): ").lower()
            
            # Handle check (when no bet to call)
            if action in ["ch", "check"] and amountToCall == 0:
                print(f"{player.getName()} checks")
                validAction = True
            
            # Handle bet (when no bet to call)
            elif action in ["b", "bet"] and amountToCall == 0:
                betAmount = utils.inputValidation(
                    input(f"Bet amount (minimum ${self.bb}): "),
                    float,
                    "+"
                )
                
                if betAmount < self.bb:
                    print(f"Bet must be at least ${self.bb}")
                elif player.getChipStack() < betAmount:
                    print(f"Not enough chips! You only have ${player.getChipStack()}")
                else:
                    player.setChipStack(player.getChipStack() - betAmount)
                    player.setBet(betAmount)
                    self.pot += betAmount
                    self.previousBet = betAmount
                    
                    # Reset acted status
                    for i in range(len(hasActed)):
                        if i != playerIndex:
                            hasActed[i] = False
                    
                    print(f"{player.getName()} bets ${betAmount}")
                    validAction = True
            
            # Handle call
            elif action in ["c", "call"] and amountToCall > 0:
                if player.getChipStack() < amountToCall:
                    print(f"Not enough chips! You only have ${player.getChipStack()}")
                else:
                    player.setChipStack(player.getChipStack() - amountToCall)
                    player.setBet(self.previousBet)
                    self.pot += amountToCall
                    print(f"{player.getName()} calls ${amountToCall}")
                    validAction = True
            
            # Handle raise
            elif action in ["r", "raise"]:
                minimumRaise = self.previousBet * 2 if self.previousBet > 0 else self.bb
                raiseAmount = utils.inputValidation(
                    input(f"Raise to (minimum ${minimumRaise}): "),
                    float,
                    "+"
                )
                
                if raiseAmount < minimumRaise:
                    print(f"Raise must be at least ${minimumRaise}")
                else:
                    additionalAmount = raiseAmount - player.getBet()
                    if player.getChipStack() < additionalAmount:
                        print(f"Not enough chips! You only have ${player.getChipStack()}")
                    else:
                        player.setChipStack(player.getChipStack() - additionalAmount)
                        player.setBet(raiseAmount)
                        self.pot += additionalAmount
                        self.previousBet = raiseAmount
                        
                        # Reset acted status
                        for i in range(len(hasActed)):
                            if i != playerIndex:
                                hasActed[i] = False
                        
                        print(f"{player.getName()} raises to ${raiseAmount}")
                        validAction = True
            
            # Handle fold
            elif action in ["f", "fold"]:
                player.setFoldStatus(True)
                print(f"{player.getName()} folds")
                validAction = True
            
            else:
                print("Invalid input. Please try again.")

    def _countActivePlayers(self) -> int:
        """Count players who haven't folded
        
        Returns:
            Number of active players
        """
        return sum(1 for p in self.playerList if not p.getFoldStatus())

        






    



