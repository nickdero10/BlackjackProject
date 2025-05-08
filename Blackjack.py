'''
Author: Nicholas DeRobertis
I Pledge my Honor that I have Abided by the Stevens Honor System
CPE 551 Python Final Project
'''

import random
import os

# Given Card Class
class Card:
    suit_list = ["Clubs", "Diamond", "Hearts", "Spades"]
    rank_list = ["None", "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
    
    # Handles ascii outputs
    def ascii(self):
        rank = Card.rank_list[self.rank]
        suit = Card.suit_list[self.suit]

        suit_symbols = {
        "Clubs": "♣",
        "Diamond": "♦",
        "Hearts": "♥",
        "Spades": "♠"
        }

        symbol = suit_symbols[suit]

        # For Jack, Queen, King, and Ace display J, Q, K, and A
        rank_display = rank if len(rank) == 2 else rank[0]


        # Ensure rank_display fits width
        rank_top = rank_display.ljust(2)
        rank_bot = rank_display.rjust(2)

        card_lines = [
            "┌─────────┐",
            f"│{rank_top}       │",
            "│         │",
            f"│    {symbol}    │",
            "│         │",
            f"│       {rank_bot}│",
            "└─────────┘"
        ]
        return card_lines

# Back of card for dealer when face down
class CardBack:
    def ascii(self):
        return [
            "┌─────────┐",
            "│?        │",
            "│         │",
            "│    ?    │",
            "│         │",
            "│        ?│",
            "└─────────┘"
        ]

# Prints out the ascii generated pictures
def print_ascii(cards):
    ascii_cards = [card.ascii() for card in cards]
    for line in zip(*ascii_cards):
        print("  ".join(line))


# Class to create the deck structure
class Deck:
    # Makes a deck with all suits and ranks 
    # and "shuffles" or randomizes the stack of the deck
    def __init__(self):
        self.build_deck()
 
    # Creates a card from each rank in the rank_list for each suit by looping
    # Creates 4 decks because blackjack is played with more than 1 deck
    def build_deck(self):
        self.cards = [Card(suit, rank) for _ in range(4) for suit in range(4) for rank in range(1, 14)]
        random.shuffle(self.cards)
    
    # "Deals" or returns whatever card was popped off the array
    # If the decks are finished it reshuffles all decks
    def deal_card(self):
        if not self.cards:
            print("Decks are finished — reshuffling new decks.")
            self.build_deck()
        return self.cards.pop()

# Class to create a hand for the player
# Handles adding cards to hand and making values from cards in hand
class Hand:
    def __init__(self):
        self.cards = []
    
    # Adds the card from deck to hand
    def add_card(self, card):
        self.cards.append(card)
    
    # Creates a value for players hand
    def create_value(self):
        value = 0
        ace_count = 0
        for card in self.cards:
            # Face Cards
            if card.rank > 10:
                value += 10
            # Ace's
            elif card.rank == 1:
                value += 11
                ace_count += 1
            # Normal Number Cards
            else:
                value += card.rank
        
        # If ace is present and the hand busts, the value goes down to 1 instead of 11
        while value > 21 and ace_count:
            value -= 10
            ace_count -= 1
        
        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)


# Class to create a hand for the player
# Handles hitting cards to  player hand
class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.hand = Hand()

    def hit(self, deck):
        self.hand.add_card(deck.deal_card())

# Inherits Player information also alows for hands and hits for dealer
# Checks if dealer can hit
class Dealer(Player):
    def __init__(self):
        super().__init__(name="Dealer")

    # Dealer can't hit if hand value is 17 or higher
    def dealer_hit(self):
        return self.hand.create_value() < 17

# Class for all game logic and information
class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()

    # Function for when player is asked to continue
    def ask_continue(self, balance, startingBalance):
        # Loop for only accepting vailid actions
        while True:
            action = input("Would you like to Continue? (yes/no)\n").strip().lower()
            # If player doesn't continue it returns continue as False
            if action == "no":
                # Shows net gain or loss if not continuing
                if startingBalance < balance:
                    print("You Won: $", balance - startingBalance)
                else:
                    print("You Lost: $", startingBalance - balance)
                return False
            # If player does continue it returns continue as True
            elif action == "yes":
                os.system("clear")
                return True     
            # If yes or no isn't entered it asks again
            else:
                print("Enter Valid Action!")
               

    # Where the game takes place
    def play(self):
        # Checks if balance is above $0
        while True:
            balance = int(input("Enter Spending Amount: $"))

            if balance <= 0:
                os.system("clear")
                print("Enter a Valid Balance!")
            else:
                break

        # Keeps track of input starting balance for gain or loss count at end
        startingBalance = balance

        while(1):
            # Clear player and dealers hands at start of next round
            self.player.hand = Hand()
            self.dealer.hand = Hand()

            # Intitialize double and hit checks as false when starting new round
            double_check = False
            hit_check = False

            # Checks if bet is valid and doesn't accept bets lower than zero or higher than balance
            while True:
                print("Your Balance: $", balance)
                bet = int(input("Enter Bet: $"))

                if bet > balance:
                    os.system("clear")
                    print("Insuficient Balance!")
                elif bet <= 0:
                    os.system("clear")
                    print("Enter a valid bet!")
                else:
                    # Subtracts bet from balance
                    balance -= bet
                    break

            # Gives the dealer two cards and the player two cards
            for _ in range(2):
                self.player.hit(self.deck)
                self.dealer.hit(self.deck)

            os.system("clear")

            # Shows one card in the dealers hand
            print("\nDealer shows: ")
            print_ascii([self.dealer.hand.cards[0], CardBack()])
            # Shows your hand
            print("Your hand: ")
            print_ascii(self.player.hand.cards)
            print("Your Bet: $", bet, "\n")


            # A couple things need to be handled before actually playing
            # Whether or not player or dealer has blackjack
            # These can skip the gameplay itself and instant lose or win
            # Whether the player has two of the same cards and wants to split
            # Makes you play with double the bet and two hands



            # BLACKJACK
            # Checks if players hand is only two cards that equal 21
            if self.player.hand.create_value() == 21 and len(self.player.hand.cards) == 2:
                print("Blackjack! You Win!\n")
                # Blackjack pays out 2:1, returns bet plus winnings
                balance += int(2.5 * bet)
                print("Balance: $", balance)

                # Continue Loop
                if not self.ask_continue(balance, startingBalance):
                    break
                else:
                    continue


            
            # INSURANCE
            # If the dealer is showing an Ace, insurance triggers
            if self.dealer.hand.cards[0].rank == 1:
                while True:
                    action = input("Dealers showing an Ace. Would you like to bet for insurance? (yes/no): ").strip().lower()
                    # Yes Insurance
                    if action == "yes":
                        insurance_bet = int(input("Enter Insurance Bet: $"))
                        # Only accepts valid insurance bets
                        if (balance - insurance_bet) < 0:
                            print("Insuficient Balance!")
                        else:
                            # Dealer has Blackjack
                            if (self.dealer.hand.create_value() == 21 and len(self.dealer.hand.cards) == 2):
                                # You lose bet but insurance pays 2:1
                                print("Dealer has Blackjack! You Win!")
                                balance -= bet
                                balance += int(2 * insurance_bet)
                                print("Balance: $", balance)

                                # Continue Loop
                                if not self.ask_continue(balance, startingBalance):
                                    return
                                else:
                                    break
                            
                            # Dealer does not have Blackjack
                            else:
                                # Game keeps going with insurance bet subtracted from balance
                                balance -= insurance_bet
                                print("Dealer does not have Blackjack! Your balance: $", balance)
                                break
                                
                    # No Insurance
                    elif action == "no":
                        # Dealer has Blackjack
                        if (self.dealer.hand.create_value() == 21 and len(self.dealer.hand.cards) == 2):
                            # You lose bet and asked to continue or not
                            print("Dealer has Blackjack! You Lose!")
                            print("Balance: $", balance)

                            if not self.ask_continue(balance, startingBalance):
                                return
                            else:
                                break

                        # Dealer does not have Blackjack
                        else:
                            # Continue game after valid output
                            print("Dealer does not have Blackjack!")
                            break 
                    # Validity Check
                    else:
                        print("Enter Valid Action!")
                                                


            # SPLIT
            if (self.player.hand.cards[0].rank == self.player.hand.cards[1].rank):
                action = input("Would you like to split Hand? (yes/no)\n").strip().lower()
                if action == "yes":
                    # Checks if balance is enough to split
                    if (balance - bet) < 0:
                        print("Not enough balance to split")
                    else:
                        # Subtracts second bet from balance and makes two hands
                        balance -= bet
                        hand1 = Hand()
                        hand2 = Hand()

                        # Takes each card from hand and splits into two hands
                        hand1.add_card(self.player.hand.cards[0])
                        hand2.add_card(self.player.hand.cards[1])

                        # Adds a new card to each hand
                        hand1.add_card(self.deck.deal_card())
                        hand2.add_card(self.deck.deal_card())

                        # Both hands and both bets are kept track of
                        hands = [hand1, hand2]
                        hand_bets = [bet, bet]

                        # handle hits for each hand
                        for i in range(2):
                            os.system("clear")
                            
                            print("\nDealer shows: ")
                            print_ascii([self.dealer.hand.cards[0], CardBack()])

                            print(f"\nPlaying Hand {i+1}:")
                            print_ascii(hands[i].cards)
                            while hands[i].create_value() < 21:
                                # Same actions for HAND CHECK
                                action = input("Hit, Stand, or Double?\n").strip().lower()
                                if action == "hit":
                                    hands[i].add_card(self.deck.deal_card())
                                    
                                    os.system("clear")

                                    hit_check = True

                                    print("Dealer shows: ")
                                    print_ascii([self.dealer.hand.cards[0], CardBack()])
                                    print("\nYour hand: ")
                                    print_ascii(hands[i].cards)
                                elif action == "double":
                                    if hit_check == True:
                                        print("Cannot double after hit!")
                                    else:
                                        if balance >= hand_bets[i]:
                                            balance -= hand_bets[i]
                                            hand_bets[i] *= 2
                                            hands[i].add_card(self.deck.deal_card())
                                            break
                                        else:
                                            print("Not enough balance to double.")
                                elif action == "stand":
                                    break
                                else:
                                    print("Invalid input.")

                        # Dealer plays after both hands are handled
                        if all(hand.create_value() <= 21 for hand in hands):
                            while self.dealer.dealer_hit():
                                self.dealer.hit(self.deck)  
                        
                        # Prints dealer hand
                        os.system("clear")
                        print("Dealer's Hand:")
                        print_ascii(self.dealer.hand.cards)
                        
                        # Prints results for both hands
                        for i in range(2):
                            print(f"\nResult for Hand {i+1}:")
                            print_ascii(hands[i].cards)
                            player_value = hands[i].create_value()
                            dealer_value = self.dealer.hand.create_value()
                            bet_i = hand_bets[i]

                            # Same Logic as DEALER CHECK
                            if player_value > 21:
                                print("You bust! Dealer wins!\n")
                            elif dealer_value > 21 or player_value > dealer_value:
                                print("You Win! $", bet_i)
                                balance += 2 * bet_i
                            elif dealer_value > player_value:
                                print("Dealer Wins!")
                            else:
                                print("You Push!")
                                balance += bet_i

                        print("Balance: $", balance)
                        if not self.ask_continue(balance, startingBalance):
                            break
                        else:
                            continue
                # If they don't want to split, game continues
                elif action == "no":
                    continue
                # Validty Check
                else:
                    print("Enter a Valid Response!")


            # HAND CHECK
            # Game takes place while players hand value is less than 21
            while (self.player.hand.create_value() < 21 and balance > 0):
                action = input("Hit, Stand, or Double?\n").strip().lower()
                # Adds card to players hand
                if action == "hit":
                    self.player.hit(self.deck)

                    os.system("clear")

                    # Makes hit_check true for double acceptance
                    hit_check = True

                    # Prints dealer and new hand
                    print("Dealer shows: ")
                    print_ascii([self.dealer.hand.cards[0], CardBack()])
                    print("\nYour hand: ")
                    print_ascii(self.player.hand.cards)

                # Adds one card to hand and doesn't accept anymore hits
                elif action == "double":
                    # Doesn't allow for double if already hit
                    if hit_check == True:
                        print("Cannot double after hit!")
                        continue
                    # Only accepts if enough balance
                    elif (balance - bet) < 0:
                        print("Not enough balance to double!")
                        continue
                    # Accepts double, takes second bet away from balance, and duplicates bet
                    else:
                        balance -= bet
                        bet *= 2
                        double_check = True
                        self.player.hit(self.deck)
                        break

                # Keeps hand and goes to dealer check
                elif action == "stand":
                    break

                # Validity Check
                else:
                    os.system("clear")
                    print("Input action isn't available")
                    print("Dealer shows: ")
                    print_ascii([self.dealer.hand.cards[0], CardBack()])
                    print("\nYour hand: ")
                    print_ascii(self.player.hand.cards)
                    print("Your Bet: $", bet, "\n")

            
            # DEALER CHECK
            if self.player.hand.create_value() <= 21:
                while self.dealer.dealer_hit():
                    self.dealer.hit(self.deck)

            os.system("clear")

            print("\nRevealed Dealers Hand: ")
            print_ascii(self.dealer.hand.cards)

            print("Your hand: ")
            print_ascii(self.player.hand.cards)

            player_value = self.player.hand.create_value()
            dealer_value = self.dealer.hand.create_value()

            # Logic that handles Payouts, Losses, or Pushes
            if player_value > 21:
                print("You bust! Dealer wins!\n")
            elif dealer_value > 21 or player_value > dealer_value:
                print("You Win! $", bet, "\n")
                balance += (bet * 2)
            elif dealer_value > player_value:
                print("Dealer Wins!\n")
            elif double_check == True:
                print("You Push!\n")
                balance += bet * 2
            else:
                print("You Push!\n")
                balance += bet 

            print("Balance: $", balance)
            
            # If there's no more balance, the game ends
            if balance <= 0:
                print("You Lose! Try Again!")
                break

            # Continue Loop
            if not self.ask_continue(balance, startingBalance):
                break
            else:
                continue

# Main to start game
if __name__ == "__main__":
    game = Game()
    game.play()
