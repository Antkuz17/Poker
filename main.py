"""
main.py

Entry point for the poker game.
This file handles initial setup and starts the game.
"""

from game import Game
import utils

def main():
    print("***WELCOME TO POKER***")
    
    # Getting player name
    userName = input("What is your name?: ")
    
    print(f"Hello, your name is {userName} and you will be playing a $1/0.5 game with a starting stack of $100")
    
    # Get number of AI players
    numAIPlayers = utils.inputValidation(
        input("How many players would you like to play against?: "), 
        int, 
        "+"
    )
    
    # Create and start the game
    game = Game(userName, numAIPlayers, startingChips=100, bigBlind=1, smallBlind=0.5)
    game.play()

if __name__ == "__main__":
    main()