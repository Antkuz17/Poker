"""
main.py

Entry point for the poker game.
This file handles initial setup and starts the game.
"""

from game import Game
from Player import Player
from AIPlayer import AIPlayer
import utils

def main():
    print("***WELCOME TO POKER***")
    
    # Get player information
    userName = input("What is your name?: ")
    startingChips = 100
    print(f"Hello, your name is {userName} and you will be playing a $1/0.5 game with a starting stack of ${startingChips}")
    
    # Create player list FIRST
    playerList = []
    playerList.append(Player(userName, startingChips))
    
    # Get number of AI players
    numAIPlayers = utils.inputValidation(
        input("How many players would you like to play against?: "), 
        int, 
        "+"
    )
    
    # Create AI players
    for i in range(numAIPlayers):
        playerList.append(AIPlayer(f"Bot {i+1}", startingChips, 5))
        print(f"{playerList[i+1].getName()} has joined the game with ${playerList[i+1].getChipStack()}")
    
    # NOW create and start the game with the playerList
    game = Game(playerList, bb=1, sb=0.5)
    game.play()

if __name__ == "__main__":
    main()