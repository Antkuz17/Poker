# Texas Hold'em Poker with Monte Carlo AI

A command-line Texas Hold'em poker game with AI opponents that use Monte Carlo simulation to make decisions.

## Overview

This is a complete implementation of Texas Hold'em poker featuring AI players that calculate win probabilities through Monte Carlo simulation. Instead of making random decisions, the AI runs hundreds of simulations per action to estimate their chances of winning, then uses pot odds to make mathematically sound decisions.

## Features

- Complete Texas Hold'em implementation with all betting rounds
- AI opponents using Monte Carlo simulation (500 simulations per decision)
- Proper hand evaluation from High Card through Royal Flush
- Multi-round gameplay with chip stack management
- Interactive betting interface for human players

## Installation

```bash
git clone https://github.com/yourusername/poker-monte-carlo-ai.git
cd poker-monte-carlo-ai
python main.py
```

No external dependencies required. Python 3.7 or higher.

## How the AI Works

The AI makes decisions by running Monte Carlo simulations:

1. For each decision, randomly deal remaining community cards and opponent hands x times
2. Evaluate all hands and count wins, losses, and ties
3. Calculate win probability from simulation results
4. Compare win probability to pot odds
5. Make decision: call if win probability exceeds pot odds, fold otherwise

Example output:
```
Bot 1's turn (current bet: $0, needs $10 to call)
  [AI thinks win probability: 67.4%]
Bot 1 calls $10
```

## Configuration

Adjust AI difficulty in `round.py`:

```python
# Change number of simulations (line ~342)
win_prob = self._simulateWinProbability(player, num_simulations=500)

# More simulations = stronger AI, slower decisions
# Fewer simulations = weaker AI, faster decisions
```

Adjust blinds in `main.py`:

```python
game = Game(playerList, bb=1, sb=0.5)
```


## License

MIT License - see LICENSE file for details.
