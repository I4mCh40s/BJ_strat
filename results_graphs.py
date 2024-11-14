import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Blackjack_testing import game_loop

cycles = 500       # Game loops with the following params
init_bal = 1000    # Starting balance
init_bet = 10     # Bet amount
stand1 = 18      # Player stands on
stand2 = 0       #
stand3 = 0       #

game_loop(cycles, init_bal, init_bet, stand1)
    

# # Loading data for each game
# data = pd.read_csv(f"{cycles}_{init_bal}_{init_bet}_{stand1}.csv")


# # Prints
# wins_num1 = data["Win"].sum()
# wins_per1 = (wins_num1*100)/cycles
# print(f"\n{cycles} cycles | Init balance {init_bal} | Bet {init_bet} | Stand on {stand1}")
# print(f"\nWins (number): {wins_num1}, which is: {wins_per1}%")
# print(f"Mean score: {data['P_score'].mean(skipna=True)}")
# print(f"End balance: {data['Balance'].iloc[-1]}")


# # Define the desired order for card values
# card_order = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

# # Apply ordering to the columns for P1_card and P2_card
# data['P1_card'] = pd.Categorical(data['P1_card'], categories=card_order, ordered=True)
# data['P2_card'] = pd.Categorical(data['P2_card'], categories=card_order, ordered=True)

# # Convert both card columns to strings after categorical ordering
# data['P1_card_str'] = data['P1_card'].astype(str)
# data['P2_card_str'] = data['P2_card'].astype(str)

# # Create a pivot table to group by card pairs and aggregate the number of wins
# pivot_table = data.groupby(['P1_card_str', 'P2_card_str']).agg({'Win': 'sum'}).reset_index()

# # Create the scatter plot with card pairs as categorical values
# plt.figure(figsize=(10, 8))

# # Use pivot_table to plot, we need to convert card values to their indices for plotting
# bubble = plt.scatter(
#     pivot_table['P1_card_str'], 
#     pivot_table['P2_card_str'], 
#     s=pivot_table['Win']*100,  # Scale the bubble size
#     alpha=0.6
# )

# # Optional: add color bar to represent the number of wins
# plt.colorbar(bubble, label='Number of Wins')

# plt.xlabel('Card 1')
# plt.ylabel('Card 2')
# plt.title('Wins by Initial Card Pair')

# # Make sure the x and y axes are ordered by card rank
# plt.xticks(ticks=range(len(card_order)), labels=card_order)
# plt.yticks(ticks=range(len(card_order)), labels=card_order)

# # Optionally add gridlines to help visualize intersections more clearly
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# # Show the plot
# plt.show()


#################
# Loading data for each game
data = pd.read_csv(f"{cycles}_{init_bal}_{init_bet}_{stand1}.csv")

# Prints
wins_num1 = data["Win"].sum()
wins_per1 = (wins_num1 * 100) / cycles
print(f"\n{cycles} cycles | Init balance {init_bal} | Bet {init_bet} | Stand on {stand1}")
print(f"\nWins (number): {wins_num1}, which is: {wins_per1}%")
print(f"Mean score: {data['P_score'].mean(skipna=True)}")
print(f"End balance: {data['Balance'].iloc[-1]}")

# Define the desired order for card values
card_order = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

# Apply ordering to the columns for P1_card and P2_card
data['P1_card'] = pd.Categorical(data['P1_card'], categories=card_order, ordered=True)
data['P2_card'] = pd.Categorical(data['P2_card'], categories=card_order, ordered=True)

# Convert both card columns to strings after categorical ordering
data['P1_card_str'] = data['P1_card'].astype(str)
data['P2_card_str'] = data['P2_card'].astype(str)

# Create a pivot table to group by card pairs and aggregate the number of wins
pivot_table = data.groupby(['P1_card_str', 'P2_card_str']).agg({'Win': 'sum'}).reset_index()

# Filter to include only combinations with 2 or more wins
pivot_table = pivot_table[pivot_table['Win'] >= 2]

# Create the scatter plot with card pairs as categorical values
plt.figure(figsize=(10, 8))

# Use pivot_table to plot, we need to convert card values to their indices for plotting
bubble = plt.scatter(
    pivot_table['P1_card_str'], 
    pivot_table['P2_card_str'], 
    s=pivot_table['Win'] * 100,  # Scale the bubble size
    alpha=0.6,
    c=pivot_table['Win'],  # Optional: Color by the number of wins
    cmap="coolwarm",
    edgecolors="black"
)

# Add color bar to represent the number of wins
plt.colorbar(bubble, label='Number of Wins')

plt.xlabel('Card 1')
plt.ylabel('Card 2')
plt.title('Wins by Initial Card Pair (Wins >= 2)')

# Make sure the x and y axes are ordered by card rank
plt.xticks(ticks=range(len(card_order)), labels=card_order)
plt.yticks(ticks=range(len(card_order)), labels=card_order)

# Optionally add gridlines to help visualize intersections more clearly
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Show the plot
plt.show()