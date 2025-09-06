from Card import Card
from Hand import Hand
from Player import Player
import random
class AIPlayer(Player):

   def __init__(self, name: str, chipstack: int, aggression: int):
      """This constructor contains the parent constructor, the parent constructor will be called first
      and then extra variables will be initilized like aggression which regulates how aggresively the aiplayer will bet"""
      super().__init__(name, chipstack) # Calling the parent constructor
      self.isAIPlayer = True
      self.aggression = aggression


   def setAggression(self, aggression: int) -> None:
      """Setter function for stating the aggression level of the AI
      1-10 scale with higher numbers meaning more aggressive actions such as
      raising, calling, and going all in"""
      self.aggression = aggression




   
   
