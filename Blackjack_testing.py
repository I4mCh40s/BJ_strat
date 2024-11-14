import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from strategy import lookup_blackjack_strategy

def game_loop (cycles, init_bal, init_bet, stand):
    #Defining a single deck of cards
    deck = {'Ace': 4, '2': 4, '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9':4, '10':4, 'Jack':4, 'Queen':4, 'King': 4}

    #Creating 8 deck shoe (Typical shoe size: 6-8 decks)
    shoe = [deck.copy() for _ in range(8)]

    #Converting to pandas DataStructure
    shoe_df=pd.DataFrame(shoe)
    #print(f"Full shoe: \n{shoe_df}")

    '''
    Creating a game round with the following rules:
        Player
        1. Money: 1000
        2. Bet: 10
        3. Martingale: Off
        4. Insurance: Off
        5. Doubling: Off
        6. 10 split: Off
        7. Stand on: 18

        Dealer
        1. Stand on: 17
    '''
    # Setting initial variables for Player
    balance = init_bal
    bet = init_bet
    player_stand_on = stand
    MTG=False
    INS=False
    DBL=False
    SPLT_10=False

    # Setting initial variables for Dealer
    dealer_stand_on = 17

    # Tens
    tens = ["Jack", "Queen", "King"]

    # Function to pull a random card from the DataFrame
    def draw_card(shoe_df):

        #Reshuffling
        total_cards = shoe_df.sum().sum()
        #print(f"{total_cards} left in the deck")

        if total_cards <= 1:
            shoe = [deck.copy() for _ in range(8)]
            shoe_df=pd.DataFrame(shoe)

        while True:
            # Randomly select a row and column index
            row = np.random.randint(0, shoe_df.shape[0])
            col = np.random.choice(shoe_df.columns)

            # Check if the card is available (count > 0)
            if shoe_df.iloc[row][col] > 0:
                # Decrease the card count by 1
                shoe_df.iloc[row, shoe_df.columns.get_loc(col)] -= 1
                total_cards = total_cards - 1
                return col  # Return the card type that was drawn
            
    # Strategy lookup function | Hit or stand

    def look_at_strategy(dealer_card1, player_score):
        if dealer_card1 in tens:
            y = "10"
        elif dealer_card1 == "Ace":
            y = "11"
        else:
            y = str(dealer_card1)
        x = str(player_score)
        des = lookup_blackjack_strategy.at[x, y]
        return des


    #Creating an empty PD data structure to store parameters
    game_results = pd.DataFrame(columns=["D1_card", "D2_card", "P1_card", "P2_card", "D_score", "P_score", "Balance", "Bet", "Win"])

    # G A M E  B E G I N S
    # for the research stage - hide 'prints' or simplify them e.g. 'win/lose' or balance updates
    g = cycles #Number of games

    # print(f"Starting balance is: {balance} and your bet is: {bet}")
    for i in range(g):
        #print(f"\nGame {i+1}")
        #print(f"########################")
        
        # Wins
        win = False
        
        bet_placed = 0  # Initialize bet_placed for each game round

    # Check previous game results starting from the third round
        if i >= 4:
            # Double bet if last game was a win and balance allows
            if ((game_results.loc[i-1, "Win"] == False) & (balance >= bet * 2) & (game_results.loc[i-2, "Win"] == False))&((game_results.loc[i-3, "Win"] == True)):
                bet_placed = game_results.loc[i-1, "Bet"] * 2
                balance -= bet_placed
            # Regular bet if last game was a loss and balance allows
            elif (game_results.loc[i-1, "Win"] == True) & (balance >= bet):
                bet_placed = bet
                balance -= bet_placed            
            # Check if balance is too low to continue
            elif balance < bet:
                print("Your balance is too low to continue")
                break

    # If no bet has been placed, place a regular bet for early rounds
        if bet_placed == 0:
            if balance >= bet:
                bet_placed = bet
                balance -= bet_placed
            else:
                print("Your balance is too low to continue")
                break


        #print(f"\nBet of {bet_placed} is placed. Current balance is: {balance}")

        # Dealer draws 2 cards
        dealer_score = 0
        dealer_card1_score = 0 # score for player's decision
        dealer_card1 = draw_card(shoe_df)
        dealer_secret = draw_card(shoe_df)
        #print(f"Dealer pulled: {dealer_card1}, and X")
        #print(f"Dealer pulled: {dealer_card1}, and {dealer_secret}")

        # Check for immediate BJ and get the score

        # 1st card
        if dealer_card1 in tens:
            dealer_score += 10
            dealer_card1_score += 10
        elif dealer_card1 == "Ace":
            # Ace can be worth 11 points initially (or 1 if the score exceeds 21)
            dealer_score += 11
            dealer_card1_score += 11
        else:
            # Convert the card to an integer for number cards
            dealer_score += int(dealer_card1)
            dealer_card1_score += int(dealer_card1)

        # X card
        if dealer_secret in tens:
            dealer_score += 10
        elif dealer_secret == "Ace":
            # Ace can be worth 11 points initially (or 1 if the score exceeds 21)
            dealer_score += 11
        else:
            # Convert the card to an integer for number cards
            dealer_score += int(dealer_secret)

        # BJ
        if dealer_score == 22: 
            dealer_score = 2
        elif dealer_score == 21:
            #print(f"Dealer pulled: {dealer_card1} and {dealer_secret} and got a BlackJack!")
            # Saving game parameters
            game_data = {
                "D1_card": dealer_card1,
                "D2_card": dealer_secret,
                "P1_card": "X",
                "P2_card": "X",
                "D_score": dealer_score,
                "P_score": 0,
                "Win": win,
                "Bet": bet_placed,
                "Balance": balance
            }

            # Append the game data as a new row to the DataFrame
            game_results = pd.concat([game_results, pd.DataFrame([game_data])], ignore_index=True)
            continue

        #remove checks
        #print(f"Dealer's score: {dealer_score}") 

        # Player draws 2 cards
        player_score = 0
        player_card1 = draw_card(shoe_df)
        player_card2 = draw_card(shoe_df)

        #print(f"You got: {player_card1}, and {player_card2}")

        # Check for immediate BJ and get the score

        # 1st card
        if player_card1 in tens:
            player_score += 10
        elif player_card1 == "Ace":
            # Ace can be worth 11 points initially (or 1 if the score exceeds 21)
            player_score += 11
        else:
            # Convert the card to an integer for number cards
            player_score += int(player_card1)

        # 2nd card
        if player_card2 in tens:
            # check for score == 10 | if true - call for split 10s
            player_score += 10
        elif player_card2 == "Ace":
            # Ace can be worth 11 points initially (or 1 if the score exceeds 21)
            player_score += 11
        else:
            # Convert the card to an integer for number cards
            player_score += int(player_card2)

        # BJ
        if player_score == 22: 
            player_score = 2
        elif player_score == 21:
            #print(f"You got: {player_card1} and {player_card2} and got a BlackJack!")
            balance = balance + (bet_placed*3)
            #print(f"Player wins!")
            #print(f"Now you have {balance} money")
            win = True
            # Saving game parameters
            game_data = {
                "D1_card": dealer_card1,
                "D2_card": dealer_secret,
                "P1_card": player_card1,
                "P2_card": player_card2,
                "D_score": dealer_score,
                "P_score": player_score,
                "Win": win,
                "Bet": bet_placed,
                "Balance": balance
            }

            # Append the game data as a new row to the DataFrame
            game_results = pd.concat([game_results, pd.DataFrame([game_data])], ignore_index=True)
            continue

        #remove checks
        #print(f"Your score: {player_score}") 

        # PLAYER'S TURN
        # (player_score < player_stand_on)&((dealer_stand_on - dealer_card1_score <= 10) & (player_score < (dealer_card1_score*2))):
        while (player_score < player_stand_on):
            des = look_at_strategy(dealer_card1, player_score)
            #des = 'H'
            # print(des)
            if des == 'H':
                player_card3=draw_card(shoe_df)
                #print(f"You hit and got: {player_card3}")
                if player_card3 in tens:
                    player_score += 10
                    #print(f"Your new score: {player_score}")
                elif player_card3 == "Ace":
                    # Ace can be worth 11 points initially (or 1 if the score exceeds 21)
                    player_score += 1
                    #print(f"Your new score: {player_score}")
                else:
                    # Convert the card to an integer for number cards
                    player_score += int(player_card3)
                    #print(f"Your new score: {player_score}")
            else:
                break

        
                

        # DEALER'S TURN
        while (dealer_score < dealer_stand_on) & (player_score <= 21):
            dealer_card3=draw_card(shoe_df)
            #print(f"Dealer hit and got: {dealer_card3}")
            if dealer_card3 in tens:
                dealer_score += 10
                #print(f"Dealer's new score: {dealer_score}")
            elif dealer_card3 == "Ace":
                # Ace can be worth 11 points initially (or 1 if the score exceeds 21)
                dealer_score += 1
                #print(f"Dealer's new score: {dealer_score}")
            else:
                # Convert the card to an integer for number cards
                dealer_score += int(dealer_card3)
                #print(f"Dealer's new score: {dealer_score}")
            
        # Results

        if player_score > 21:
            print(win) 

        elif dealer_score > 21:
            #print(f"Dealer's score is {player_score}: BUST!")  
            balance = balance + (bet_placed*2)
            #print(f"Player wins!")
            win = True
            print(win)         
            
        elif player_score == dealer_score:
            balance = balance + bet_placed
            #print(f"Tie!")
            #print(f"Now you have {balance} money")
            print(win)
                
            
        elif (player_score > dealer_score) & (player_score <= 21):
            balance = balance + (bet_placed*2)
            #print(f"Player wins!")
            win=True
            print(win)
            #print(f"Now you have {balance} money")
                
                
        else:
            #print(f"Dealer wins!")
            print(win)
            #print(f"Now you have {balance} money")

        # Saving game parameters
        game_data = {
            "D1_card": dealer_card1,
            "D2_card": dealer_secret,
            "P1_card": player_card1,
            "P2_card": player_card2,
            "D_score": dealer_score,
            "P_score": player_score,
            "Win": win,
            "Bet": bet_placed,
            "Balance": balance
        }

        # Append the game data as a new row to the DataFrame
        game_results = pd.concat([game_results, pd.DataFrame([game_data])], ignore_index=True)

    #print(f"\nShoe after {g} games:")
    #print(shoe_df)

    #print(f"\nGame results after {g} games:")
    #print(game_results)
    filename = f"{cycles}_{init_bal}_{init_bet}_{stand}.csv"
    game_results.to_csv(filename, index=False)



# Plot a graph
# plt.plot(game_results.index+1, game_results["Balance"])
# plt.show()


# Remaining lines below need to be active while the game_loop function is disabled

# wins_num = game_results["Win"].sum()
# wins_per = (wins_num*100)/g
# print(f"\nStats: ")
# print(f"Wins (number): {wins_num}, which is: {wins_per}%")
# print(f"Your balance is: {balance}")
# if balance > 1000:
#     print(f"You won: {balance-1000} moneys!")
# elif balance < 1000:
#     print(f"You lost: {1000-balance} moneys -_-")
# else:
#     print(f"You lost nothing and won nothing")

# (dealer_stand - dealer_card1 > 10) & (player_score >= (dealer_score + 10)) - stand
# (dealer_stand - dealer_card1_score <= 10) & (player_score < (dealer_card1_score + 10)) - hit

# (player_score < player_stand_on) | ((dealer_stand_on - dealer_card1_score <= 10) & (player_score < (dealer_card1_score + 10)))
