# Python Blackjack

A console-based Blackjack game developed in Python for CPE 551 Final Project.  
Created by **Nicholas DeRobertis**  
*I Pledge my Honor that I have Abided by the Stevens Honor System*

## Features

- Full game of Blackjack with:
  - ASCII-rendered cards
  - Betting system
  - Double down
  - Splitting hands
  - Insurance bets
  - Multi-deck shuffling
- Dealer logic according to standard rules
- Input validation and error handling
- Persistent balance tracking through game rounds

## How to Run

1. Make sure you have Python 3 installed.
2. Clone or download this repository.
3. Open a terminal in the project directory.
4. Run the game:

```bash
python blackjack.py
```

## Classes Overview
 - Card: Represents a single playing card with ASCII art.
 - CardBack: Renders the back of a card (used for dealer's hidden card).
 - Deck: Creates and shuffles a multi-deck stack of cards.
 - Hand: Manages a player's or dealer's hand and calculates hand value.
 - Player: Represents a player in the game.
 - Dealer: Inherits from Player, includes hit logic specific to dealer.
 - Game: Manages game flow, betting, splitting, doubling, insurance, and rounds.

## Blackjack Rules
 - Blackjack pays 3:2
 - Insurance pays 2:1 if dealer has blackjack
 - Dealer stands on 17 and above
 - Players may split once
 - Double allowed only as first move

## Example Output
Dealer shows:
┌─────────┐  ┌─────────┐ \n
│9        │  │?        │
│         │  │         │
│    ♥    │  │    ?    │
│         │  │         │
│        9│  │        ?│
└─────────┘  └─────────┘

Your hand:
┌─────────┐  ┌─────────┐
│K        │  │A        │
│         │  │         │
│    ♠    │  │    ♦    │
│         │  │         │
│        K│  │        A│
└─────────┘  └─────────┘

Blackjack! You Win!
Balance: $125
