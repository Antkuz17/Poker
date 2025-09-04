from Hand import Hand

class Player:
    def __init__(self, name: str, chipstack: int, hand: Hand, bet: int) -> None:
        self.name = name
        self.chipstack = chipstack
        self.hand = Hand()
        self.bet = bet

    # Getters and Setters
    
    def setName(self, name: str) -> None:
        """Sets the name of this player"""
        self.name = name
    
    def setChipStack(self, chipstack: int) -> None:
        """Sets the value of the chipstack to the number input"""
        self.chipstack = chipstack

    def setbet(self, bet:int) -> None:
        """Sets the value of the bet variable"""
        self.bet = bet

    def getName(self) -> str:
        """Returns the name of the player as type string"""
        return self.name

    def getChipStack(self) -> int:
        """Returns the amount of money the player has as type int"""
        return self.chipstack
    
    # def get