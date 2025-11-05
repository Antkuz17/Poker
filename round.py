from Card import Card
from Deck import Deck
from Hand import Hand
from Player import Player
from AIPlayer import AIPlayer
import utils
import random 
from CommunityCards import CommunityCards
from HandEvaluator import HandEvaluator
from itertools import combinations
from collections import Counter

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
            """Handle AI player action using Monte Carlo simulation
            
            Args:
                player: The AI player
                playerIndex: Index of player in playerList
                amountToCall: Amount needed to call
                hasActed: List tracking who has acted
            """
            print(f"\n{player.getName()}'s turn (current bet: ${player.getBet()}, needs ${amountToCall} to call)")
            
            # Calculate win probability using Monte Carlo simulation
            win_prob = self._simulateWinProbability(player, num_simulations=500)
            print(f"  [AI thinks win probability: {win_prob:.1%}]")
            
            # Calculate pot odds if there's an amount to call
            pot_odds = amountToCall / (self.pot + amountToCall) if amountToCall > 0 else 0
            
            # Decision logic based on win probability
            if amountToCall == 0:
                # No cost to stay in - decide whether to bet/raise or check
                if win_prob > 0.55:
                    # Strong hand means consider raising
                    raiseAmount = self.previousBet * 2 if self.previousBet > 0 else self.bb
                    additionalAmount = raiseAmount - player.getBet()
                    
                    #Raise probability increases with hand strength
                    should_raise = random.random() < (win_prob - 0.55) * 2
                    
                    if player.getChipStack() >= additionalAmount and should_raise:
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
                        print(f"{player.getName()} checks")
                else:
                    print(f"{player.getName()} checks")
            
            else:
                # Good call if win_prob > pot_odds (with 20% margin for safety)
                if win_prob > pot_odds * 1.2:
                    if player.getChipStack() >= amountToCall:
                        # Good value - decide between calling and raising
                        if win_prob > 0.70 and random.random() < 0.25:
                            # Very strong hand - sometimes raise
                            raiseAmount = self.previousBet * 2
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
                                # Not enough to raise, just call
                                player.setChipStack(player.getChipStack() - amountToCall)
                                player.setBet(self.previousBet)
                                self.pot += amountToCall
                                print(f"{player.getName()} calls ${amountToCall}")
                        else:
                            # Call
                            player.setChipStack(player.getChipStack() - amountToCall)
                            player.setBet(self.previousBet)
                            self.pot += amountToCall
                            print(f"{player.getName()} calls ${amountToCall}")
                    else:
                        player.setFoldStatus(True)
                        print(f"{player.getName()} folds (not enough chips)")
                else:
                    # Bad value - fold
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
    
    def _simulateWinProbability(self, player, num_simulations=500):
        """
        Run Monte Carlo simulation to estimate win probability
        In essece this function simulates random outcomes for the remaining community cards
        and opponent hole cards, then evaluates how often the given player wins.
        
        Args:
            player: The player to evaluate
            num_simulations: Number of simulations to run
            
        Returns:
            float: Win probability (0.0 to 1.0)
        """
        player_hole_cards = player.hand.getCards()
        community_cards = self.communityCards.getCommunityCards()
        
        # Count active opponents
        num_opponents = sum(1 for p in self.playerList if not p.getFoldStatus() and p != player)
        
        if num_opponents == 0:
            return 1.0  # No opponents, we win
        
        wins = 0
        ties = 0
        
        # Get all known cards
        known_cards = set()
        for card in player_hole_cards + community_cards:
            known_cards.add((card.getRank(), card.getSuit()))
        
        # Create deck of unknown cards
        all_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        all_suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
        unknown_deck = [(r, s) for r in all_ranks for s in all_suits if (r, s) not in known_cards]
        
        # Central Simulation Loop used to run the simulation
        for _ in range(num_simulations):
            # Shuffle unknown cards
            random.shuffle(unknown_deck)
            
            # Deal remaining community cards
            cards_needed = 5 - len(community_cards)
            simulated_community = list(community_cards)
            
            for i in range(cards_needed):
                rank, suit = unknown_deck[i]
                # Create a simple card-like object
                card = type('Card', (), {'getRank': lambda r=rank: r, 'getSuit': lambda s=suit: s})()
                simulated_community.append(card)
            
            # Evaluate player's hand
            player_hand_rank = self._evaluateHandQuick(player_hole_cards + simulated_community)
            
            # Simulate opponent hands
            deck_idx = cards_needed
            player_wins_this_sim = True
            player_ties_this_sim = False
            
            for _ in range(num_opponents):
                # Deal 2 cards to opponent
                opp_cards = []
                for _ in range(2):
                    rank, suit = unknown_deck[deck_idx]
                    card = type('Card', (), {'getRank': lambda r=rank: r, 'getSuit': lambda s=suit: s})()
                    opp_cards.append(card)
                    deck_idx += 1
                
                # Evaluate opponent's hand
                opp_hand_rank = self._evaluateHandQuick(opp_cards + simulated_community)
                
                # Compare
                if opp_hand_rank > player_hand_rank:
                    player_wins_this_sim = False
                    break
                elif opp_hand_rank == player_hand_rank:
                    player_ties_this_sim = True
            
            if player_wins_this_sim:
                if player_ties_this_sim:
                    ties += 1
                else:
                    wins += 1
        
        return (wins + ties * 0.5) / num_simulations

    def _evaluateHandQuick(self, cards):
        """
        Quick hand evaluation returning a comparable number (higher = better)
        Returns tuple: (hand_rank, tiebreakers)
        """
        if len(cards) < 5:
            return (0, [])
        
        # Convert cards to (rank_value, suit) tuples
        rank_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '10': 10,
                       '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
        
        card_tuples = [(rank_values[card.getRank()], card.getSuit()) for card in cards]
        
        # Try all 5-card combinations and get the best
        best_rank = (0, [])
        for combo in combinations(card_tuples, 5):
            rank = self._evaluate5Cards(list(combo))
            if rank > best_rank:
                best_rank = rank
        
        return best_rank

    def _evaluate5Cards(self, cards) -> tuple:
        """Evaluate exactly 5 cards - returns (hand_rank, tiebreakers)"""
        ranks = sorted([c[0] for c in cards], reverse=True)
        suits = [c[1] for c in cards]
        rank_counts = Counter(ranks)
        
        is_flush = len(set(suits)) == 1
        is_straight = (ranks[0] - ranks[4] == 4 and len(rank_counts) == 5) or \
                      (ranks == [14, 5, 4, 3, 2])  
        
        counts = sorted(rank_counts.values(), reverse=True)
        
        # Straight Flush (including Royal)
        if is_flush and is_straight:
            return (8, ranks)
        
        # Four of a Kind
        if counts == [4, 1]:
            four = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (7, [four, kicker])
        
        # Full House
        if counts == [3, 2]:
            three = [r for r, c in rank_counts.items() if c == 3][0]
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            return (6, [three, pair])
        # Flush
        if is_flush:
            return (5, ranks)
        
        # Straight
        if is_straight:
            return (4, ranks)
        
        # Three of a Kind
        if counts == [3, 1, 1]:
            three = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (3, [three] + kickers)
        
        # Two Pair (Same card twice, two times)
        if counts == [2, 2, 1]:
            pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (2, pairs + [kicker])
        # One Pair
        if counts == [2, 1, 1, 1]:
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (1, [pair] + kickers)
        
        # High Card
        return (0, ranks)


        






    



