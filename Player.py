from Hand import Hand

"""
player.py

This module contains the 'Player' class which represents a poker player
Each player has a name, chipstack, hand, current bet, and fold status 

This module includes methods for
- Setting and getting the player's name
- Setting and getting the player's chipstack
- Setting and getting the player's current bet
- Setting and getting the player's fold status
"""

class Player:
    def __init__(self, name: str, chipstack: int) -> None:
        self.name = name # Name of the player
        self.chipstack = chipstack # Amount of chips the player has
        self.hand = Hand() # The hand object that contains the 2 cards the player has
        self.bet = 0 # The current bet of the player
        self.fold = False # Whether the player has folded or not
        self.isAIPlayer = False # Whether this player is an AI bot or not
        self.allIn = False # Whether the player is all in or not
        

    # Getters and Setters
    
    def setName(self, name: str) -> None:
        """Sets the name of this player"""
        self.name = name
    
    def setChipStack(self, chipstack: int) -> None:
        """Sets the value of the chipstack to the number input"""
        self.chipstack = chipstack

    def setBet(self, bet:int) -> None:
        """Sets the bet of the player and deducts that amount from their chipstack, if the bet is equal to their chipstack
        then the player is all in"""
        self.chipstack -= bet
        self.bet = bet
        if self.chipstack == 0:
            self.allIn = True

    
    def setFoldStatus(self, status: bool) -> None:
        """Sets the status of a player to folded or not"""
        self.fold = bool

    def getName(self) -> str:
        """Returns the name of the player as type string"""
        return self.name

    def getChipStack(self) -> int:
        """Returns the amount of money the player has as type int"""
        return self.chipstack
    
    def getIsAIPlayer(self) -> bool:
        """Returns whether this player is an AI bot or not, used in the main game loop to allow turns to go smoother"""
        return self.isAIPlayer
    
    def getHand(self) -> list:
        """Returns the 2 cards the player has within their hand, returns an empty list"""
        return self.Cards
    
    def getBet(self) -> int:
        """Returns the current bet of the player as an int"""
        return self.bet
    
    def getFoldStatus(self) -> bool:
        """Returns whether the player has folded or not as a boolean"""
        return self.fold
    
