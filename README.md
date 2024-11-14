This is a WIP practice project. It does the job, but a few things are missing.

Basically it simulates a Blackjack game against a dealer with various parameters that you can change and see how it affects the outcome.

**You can control:**
- Number of game cycles
- Initial bet
- Initial balance
- "Stand on" value (for player)
- 'Hit' vs 'Stand' strategy (as a pandas data frame)

**A few features that are available:**
- Light Martingale: doubling the bet (2 times max in order to avoid total loss of balance) after the loss
- Dealer always stands on 17

**WIP:**
- Doubling
- Card splitting
- Insurance

**When X game cycles are played through the script produces a .CSV file with these parameters for each game:**
Dealer's card #1 | Dealer's card #2 | Player's card #1 | Player's card #2 | Dealer's score | Player's score | bool Win/Lose | Bet placed | Balance after the game

**Finally the game gives a few stats about that game cycle and shows the scatter graph (what card combos produced more frequent wins):**

500 cycles | Init balance 1000 | Bet 10 | Stand on 18

Wins (number): 213, which is: 42.6%
Mean score: 18.65
End balance: 800
