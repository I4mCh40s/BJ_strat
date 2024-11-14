import pandas as pd

strategy_data = {
    "2":  ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S"],
    "3":  ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S"],
    "4":  ["H", "H", "S", "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "S", "S", "S", "S", "S"],
    "5":  ["H", "H", "S", "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "H", "S", "S", "S", "S"],
    "6":  ["H", "H", "S", "S", "S", "S", "S", "S", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S"],
    "7":  ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S", "S"],
    "8":  ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S", "S"],
    "9":  ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S", "S"],
    "10": ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S", "S"],
    "11": ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "S", "S", "S", "S"],
} # Player  2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19




# Create DataFrame
lookup_blackjack_strategy = pd.DataFrame(strategy_data, index=["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"])
#print(lookup_blackjack_strategy)

#file = "strat.csv"
#lookup_blackjack_strategy.to_csv(file, index=False)
