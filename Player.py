from Hand import Hand

class Player:
    def __init__(self, name: str, chipstack: int) -> None:
        self.name = name
        self.chipstack = chipstack
        self.hand = Hand()
        self.bet = 0
        self.fold = False
        self.isAIPlayer = False
        

    # Getters and Setters
    
    def setName(self, name: str) -> None:
        """Sets the name of this player"""
        self.name = name
    
    def setChipStack(self, chipstack: int) -> None:
        """Sets the value of the chipstack to the number input"""
        self.chipstack = chipstack

    def setBet(self, bet:int) -> None:
        """Sets the value of the bet variable"""
        self.bet = bet
    
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
    
