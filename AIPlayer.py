from Card import Card
from Hand import Hand
from Player import Player
import random

"""
AIPlayer.py

This module contains the 'AIPlayer' class which represents an AI controlled poker player
This is the child class of the Player class with added functionality for AI behavior

This module includes methods for
- Setting and getting the aggression level of the AI player
- AI decision making for betting, folding, calling, and raising // Not done
"""


class AIPlayer(Player):

   def __init__(self, name: str, chipstack: int, aggression: int):
      """This constructor contains the parent constructor, the parent constructor will be called first
      and then extra variables will be initilized like aggression which regulates how aggresively the aiplayer will bet"""
      super().__init__(name, chipstack) # Calling the parent constructor
      self.isAIPlayer = True     # Setting the isAIPlayer variable to true so the game loop knows this player is an AI
      self.aggression = aggression


   def setAggression(self, aggression: int) -> None:
      """Setter function for stating the aggression level of the AI
      1-10 scale with higher numbers meaning more aggressive actions such as
      raising, calling, and going all in"""
      self.aggression = aggression

   def getAggression(self) -> int:
      """Returns the aggression level of the AI player"""
      return self.aggression
   
   




   
   
