from round import Round

"""
Game.py

This module contains the 'Game' class which manages the overall poker game.
It handles:
- Managing the player list across multiple rounds
- Tracking dealer position (button)
- Managing blinds
- Running the game loop
- Eliminating players who run out of chips
- Rotating player positions between rounds
"""

class Game:
    
    def __init__(self, playerList: list, bb: float, sb: float) -> None:
        """Initialize the game with players and blind amounts
        
        Args:
            playerList: List of Player/AIPlayer objects
            bb: Big blind amount
            sb: Small blind amount
        """
        self.playerList = playerList
        self.bb = bb
        self.sb = sb
        self.dealerPosition = 0  # Tracks button position
        self.roundCounter = 1
        
    def play(self) -> None:
        """Main game loop - plays rounds until only one player remains"""
        
        while self.hasActivePlayers():
            print(f"\n{'='*50}")
            print(f"ROUND {self.roundCounter}")
            print(f"{'='*50}\n")
            
            # Show chip counts
            self.showChipCounts()
            
            # Create and play a new round
            newRound = Round(self.playerList, self.bb, self.sb)
            newRound.playPreFlop()
            newRound.playFlop()
            # newRound.playTurn()
            # newRound.playRiver()
            # newRound.playShowdown()
            
            # Clean up after round
            self.cleanupAfterRound()
            
            # Check if game should continue
            if not self.hasActivePlayers():
                break
                
            # Prompt for next round
            input("\nPress Enter to continue to the next round...")
            
            self.roundCounter += 1
    
    def hasActivePlayers(self) -> bool:
        """Check if there are at least 2 players with chips
        
        Returns:
            True if game should continue, False otherwise
        """
        activePlayers = [p for p in self.playerList if p.getChipStack() > 0]
        
        if len(activePlayers) < 2:
            if len(activePlayers) == 1:
                print(f"\n{'='*50}")
                print(f"{activePlayers[0].getName()} is the last player remaining and wins the game!")
                print(f"{'='*50}")
            return False
        return True
    
    def showChipCounts(self) -> None:
        """Display each player's current chip count"""
        print("Current chip counts:")
        for i, player in enumerate(self.playerList):
            position = "Small Blind" if i == 0 else "Big Blind" if i == 1 else "Player"
            print(f"  {player.getName()} ({position}): ${player.getChipStack()}")
        print()
    
    def cleanupAfterRound(self) -> None:
        """Clean up game state after a round completes"""
        # Remove players with no chips
        self.eliminateBrokePlayers()
        
        # Rotate player positions (move button)
        self.rotatePositions()
        
        # Reset all player states for next round
        self.resetPlayerStates()
    
    def eliminateBrokePlayers(self) -> None:
        """Remove players with 0 chips from the game"""
        remainingPlayers = []
        for player in self.playerList:
            if player.getChipStack() <= 0:
                print(f"\n{player.getName()} has no chips remaining and is eliminated from the game")
            else:
                remainingPlayers.append(player)
        
        self.playerList = remainingPlayers
    
    def rotatePositions(self) -> None:
        """Rotate player positions - last player becomes first (button moves)"""
        if len(self.playerList) > 1:
            lastPlayer = self.playerList.pop()
            self.playerList.insert(0, lastPlayer)
    
    def resetPlayerStates(self) -> None:
        """Reset all player states for the next round"""
        for player in self.playerList:
            player.setBet(0)  # Clear bets
            player.setFoldStatus(False)  # Unfold all players
            player.hand.clearHand()  # Clear their hands