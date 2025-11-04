"""
HandEvaluator.py

This module contains the HandEvaluator class which evaluates poker hands.
It can determine the best 5-card hand from 7 cards (2 hole cards + 5 community cards)
and compare hands to determine winners.

Hand Rankings (from highest to lowest):
9. Royal Flush
8. Straight Flush
7. Four of a Kind
6. Full House
5. Flush
4. Straight
3. Three of a Kind
2. Two Pair
1. One Pair
0. High Card
"""

from itertools import combinations

class HandEvaluator:
    
    # Hand rank constants
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9
    
    # Rank names for display
    HAND_NAMES = {
        0: "High Card",
        1: "One Pair",
        2: "Two Pair",
        3: "Three of a Kind",
        4: "Straight",
        5: "Flush",
        6: "Full House",
        7: "Four of a Kind",
        8: "Straight Flush",
        9: "Royal Flush"
    }
    
    @staticmethod
    def evaluateBestHand(holeCards: list, communityCards: list) -> tuple:
        """Evaluate the best 5-card hand from 7 cards
        Args:
            holeCards: List of 2 Card objects (player's hole cards)
            communityCards: List of 5 Card objects (community cards)
            
        Returns:
            Tuple: (hand_rank, tiebreaker_values, best_5_cards, hand_name)
        """
        # Combine all 7 cards
        allCards = holeCards + communityCards
        
        # Generate all possible 5-card combinations
        bestHand = None
        bestRank = -1
        bestTiebreakers = []
        bestCards = []
        
        for fiveCards in combinations(allCards, 5):
            fiveCards = list(fiveCards)
            rank, tiebreakers = HandEvaluator._evaluateFiveCards(fiveCards)
            
            # Compare this hand to the current best
            if rank > bestRank or (rank == bestRank and HandEvaluator._compareTiebreakers(tiebreakers, bestTiebreakers) > 0):
                bestRank = rank
                bestTiebreakers = tiebreakers
                bestCards = fiveCards
        
        handName = HandEvaluator.HAND_NAMES[bestRank]
        return (bestRank, bestTiebreakers, bestCards, handName)
    
    @staticmethod
    def _evaluateFiveCards(cards: list) -> tuple:
        """Evaluate a specific 5-card hand
        
        Args:
            cards: List of exactly 5 Card objects
            
        Returns:
            Tuple: (hand_rank, tiebreaker_values)
        """
        # Get rank values (convert face cards to numbers)
        ranks = [HandEvaluator._cardRankToValue(card.getRank()) for card in cards]
        suits = [card.getSuit() for card in cards]
        
        # Sort ranks in descending order
        ranks.sort(reverse=True)
        
        # Check for flush
        isFlush = len(set(suits)) == 1
        
        # Check for straight
        isStraight, straightHighCard = HandEvaluator._checkStraight(ranks)
        
        # Count rank frequencies
        rankCounts = {}
        for rank in ranks:
            rankCounts[rank] = rankCounts.get(rank, 0) + 1
        
        # Sort by count (descending) then by rank value (descending)
        sortedCounts = sorted(rankCounts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        
        # Determine hand type
        counts = [count for rank, count in sortedCounts]
        uniqueRanks = [rank for rank, count in sortedCounts]
        
        # Royal Flush (A-K-Q-J-10 suited)
        if isFlush and isStraight and straightHighCard == 14:
            return (HandEvaluator.ROYAL_FLUSH, [14])
        
        # Straight Flush
        if isFlush and isStraight:
            return (HandEvaluator.STRAIGHT_FLUSH, [straightHighCard])
        
        # Four of a Kind
        if counts[0] == 4:
            return (HandEvaluator.FOUR_OF_A_KIND, [uniqueRanks[0], uniqueRanks[1]])
        
        # Full House
        if counts[0] == 3 and counts[1] == 2:
            return (HandEvaluator.FULL_HOUSE, [uniqueRanks[0], uniqueRanks[1]])
        
        # Flush
        if isFlush:
            return (HandEvaluator.FLUSH, uniqueRanks)
        
        # Straight
        if isStraight:
            return (HandEvaluator.STRAIGHT, [straightHighCard])
        
        # Three of a Kind
        if counts[0] == 3:
            return (HandEvaluator.THREE_OF_A_KIND, [uniqueRanks[0]] + uniqueRanks[1:])
        
        # Two Pair
        if counts[0] == 2 and counts[1] == 2:
            return (HandEvaluator.TWO_PAIR, [uniqueRanks[0], uniqueRanks[1], uniqueRanks[2]])
        
        # One Pair
        if counts[0] == 2:
            return (HandEvaluator.ONE_PAIR, [uniqueRanks[0]] + uniqueRanks[1:])
        
        # High Card
        return (HandEvaluator.HIGH_CARD, uniqueRanks)
    
    @staticmethod
    def _cardRankToValue(rank: str) -> int:
        """Convert card rank to numeric value for comparison
        
        Args:
            rank: String representation of rank ('2'-'10', 'J', 'Q', 'K', 'A')
            
        Returns:
            Integer value (2-14, where Ace = 14)
        """
        if rank == 'A':
            return 14
        elif rank == 'K':
            return 13
        elif rank == 'Q':
            return 12
        elif rank == 'J':
            return 11
        else:
            return int(rank)
    
    @staticmethod
    def _checkStraight(ranks: list) -> tuple:
        """Check if ranks form a straight
        
        Args:
            ranks: Sorted list of rank values
            
        Returns:
            Tuple: (is_straight: bool, high_card: int)
        """
        ranks = sorted(ranks, reverse=True)
        
        # Check for regular straight
        if ranks[0] - ranks[4] == 4 and len(set(ranks)) == 5:
            return (True, ranks[0])
        
        # Check for wheel straight (A-2-3-4-5)
        if ranks == [14, 5, 4, 3, 2]:
            return (True, 5)  # In a wheel, 5 is the high card
        
        return (False, 0)
    
    @staticmethod
    def _compareTiebreakers(tiebreakers1: list, tiebreakers2: list) -> int:
        """Compare two hands with the same rank
        
        Args:
            tiebreakers1: List of tiebreaker values for hand 1
            tiebreakers2: List of tiebreaker values for hand 2
            
        Returns:
            1 if hand1 wins, -1 if hand2 wins, 0 if tie
        """
        for i in range(min(len(tiebreakers1), len(tiebreakers2))):
            if tiebreakers1[i] > tiebreakers2[i]:
                return 1
            elif tiebreakers1[i] < tiebreakers2[i]:
                return -1
        return 0
    
    @staticmethod
    def compareHands(hand1: tuple, hand2: tuple) -> int:
        """Compare two evaluated hands
        
        Args:
            hand1: Tuple from evaluateBestHand (rank, tiebreakers, cards, name)
            hand2: Tuple from evaluateBestHand (rank, tiebreakers, cards, name)
            
        Returns:
            1 if hand1 wins, -1 if hand2 wins, 0 if tie
        """
        rank1, tiebreakers1, _, _ = hand1
        rank2, tiebreakers2, _, _ = hand2
        
        # Compare ranks first
        if rank1 > rank2:
            return 1
        elif rank1 < rank2:
            return -1
        
        # Same rank, compare tiebreakers
        return HandEvaluator._compareTiebreakers(tiebreakers1, tiebreakers2)
    
    @staticmethod
    def formatHandDescription(hand: tuple, playerName: str) -> str:
        """Create a readable description of a player's hand
        
        Args:
            hand: Tuple from evaluateBestHand
            playerName: Name of the player
            
        Returns:
            Formatted string describing the hand
        """
        rank, tiebreakers, cards, handName = hand
        
        # Format card list
        cardStrs = [f"{card.getRank()}{card.getSuit()}" for card in cards]
        cardList = ", ".join(cardStrs)
        
        # Create description with specific details (yes this code is terrifying)
        if rank == HandEvaluator.ROYAL_FLUSH:
            description = f"{playerName} has a {handName}! [{cardList}]"
        elif rank == HandEvaluator.STRAIGHT_FLUSH:
            highCard = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has a {handName}, {highCard}-high! [{cardList}]"
        elif rank == HandEvaluator.FOUR_OF_A_KIND:
            fourRank = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has {handName}, {fourRank}s! [{cardList}]"
        elif rank == HandEvaluator.FULL_HOUSE:
            threeRank = HandEvaluator._valueToRankString(tiebreakers[0])
            pairRank = HandEvaluator._valueToRankString(tiebreakers[1])
            description = f"{playerName} has a {handName}, {threeRank}s over {pairRank}s! [{cardList}]"
        elif rank == HandEvaluator.FLUSH:
            highCard = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has a {handName}, {highCard}-high! [{cardList}]"
        elif rank == HandEvaluator.STRAIGHT:
            highCard = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has a {handName}, {highCard}-high! [{cardList}]"
        elif rank == HandEvaluator.THREE_OF_A_KIND:
            threeRank = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has {handName}, {threeRank}s! [{cardList}]"
        elif rank == HandEvaluator.TWO_PAIR:
            highPair = HandEvaluator._valueToRankString(tiebreakers[0])
            lowPair = HandEvaluator._valueToRankString(tiebreakers[1])
            description = f"{playerName} has {handName}, {highPair}s and {lowPair}s! [{cardList}]"
        elif rank == HandEvaluator.ONE_PAIR:
            pairRank = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has {handName}, {pairRank}s! [{cardList}]"
        else:  # high card logic
            highCard = HandEvaluator._valueToRankString(tiebreakers[0])
            description = f"{playerName} has {handName}, {highCard}-high! [{cardList}]"
        
        return description
    
    @staticmethod
    def _valueToRankString(value: int) -> str:
        """Convert numeric value back to rank string 
        Args:
            value: Numeric value (2-14)
            
        Returns:
            Rank string ('2'-'10', 'Jack', 'Queen', 'King', 'Ace')
        """
        valueMap = {
            14: "Ace",
            13: "King",
            12: "Queen",
            11: "Jack",
            10: "10",
            9: "9",
            8: "8",
            7: "7",
            6: "6",
            5: "5",
            4: "4",
            3: "3",
            2: "2"
        }
        return valueMap.get(value, str(value))