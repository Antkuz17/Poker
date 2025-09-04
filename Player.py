from Card import Card
from Hand import Hand
class Player:

    # When creating the AI players, each will start with random chipstack within a set amount
    # Each will have a hand and a risk analysis stat on the chance of them calling/raising
    def __init__(self, chipStack, hand):
        