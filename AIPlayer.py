from Card import Card
from Hand import Hand
from Player import Player
import random
class AIPlayer(Player):

   def genRandChipStack(self, min: int, max: int) -> None:
      """Will generate a random integer within the specified bounds inclusive, returns no value"""
      chipstack = random.randint(min, max)
      print(f"{self.name} Chipstack has generated a value of {self.chipstack}")

