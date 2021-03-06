from card import *
from player import *
from deck import *
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()
player_num = int(input("number of players playing:\n"))
card_deck = Deck()#[Card(0, 1), Card(0, 1), Card(0,1), Card(0, 1), Card(0,1), Card(0, 1), Card(0,1), Card(0, 1), Card(0,1), Card(0, 1), Card(0,1), Card(0, 1), Card(0,1), Card(0, 1), Card(0,1)])#gen_deck()
#print (card_deck)
curr_card = card_deck.next()
#print (curr_card)
while curr_card.type in (10, 11, 12, 13, 14):
    curr_card = card_deck.next()
    #print (curr_card)


players = []
for i in range(player_num):
    cards = []
    for j in range(7):
        cards.append(card_deck.next())
    name = input(f"Player {str(i + 1)}'s name: ")
    players.append(Player(name, cards))


curr_player = 0
next_up = True
def reverse():
    global next_up
    next_up = not next_up
def next_player():
    global curr_player, next_up
    #p = curr_player
    if next_up == True:
        curr_player += 1
        if curr_player == player_num:
            curr_player = 0
            #print ("to high")
    else:
        curr_player -= 1
        if curr_player == -1:
            curr_player = player_num-1
            #print ("to low")
    #print (curr_player)
    return curr_player

give = 0
remove = []

skips = 0

on = True
while on:
    clear()
    #print (curr_player)
    print (f"########### Waiting for {players[curr_player].name} ###########")
    print (f"Current card: {str(curr_card)}")
    print (f"Cards left: {str(card_deck.cards_left())}")
    print (f"########### Waiting for {players[curr_player].name} ###########")
    input()
    clear()

    for i in range(give):
        players[curr_player].give_cards([card_deck.next()])
    give = 0

    turn = True
    while turn:

        print (f"Current card: {curr_card.get_color() + ' ' + curr_card.get_type()}")
        print (f"Current player: {players[curr_player].name}")
        print (f"Cards left: {str(card_deck.cards_left())}")

        print ()
        print ("Your cards:")
        #print (players[curr_player])#players[curr_player].deck)
        players[curr_player].deck = sorted(players[curr_player].deck)
        for i in range(len(players[curr_player].deck)):
            print (str(i+1)+".", players[curr_player].deck[i].get_color(), players[curr_player].deck[i].get_type())
        print ()

        cards = input("Number of card(s) to play:\n").split(" ")
        skip = cards == [""] or cards == ["skip"] or cards == ["pass"]
        if not skip:
            player_for_turn = curr_player
            cards = list(map(int, cards))
            #next_card = curr_card
            #first_card = players[player_for_turn].get_deck()[cards[0] - 1]
            for card in cards:
                card_num = card - 1
                card = players[player_for_turn].get_deck()[card_num]
                if card.possible(curr_card):# and card == first_card:
                    #players[player_for_turn].remove_card(card_num)
                    remove.append(card_num)
                    #if len(players[player_for_turn].deck) == 7:
                    #    new_card = [card_deck.next()]
                    #    players[player_for_turn].give_cards(new_card)
                        #print (players[player_for_turn])
                        #print (new_card[0])
                        #input()

                #if card.possible(curr_card):# and card == first_card:
                    prev_card = curr_card
                    curr_card = card
                    if card.type == CBLOCK:
                        next_player()
                    elif card.type == CSWITCH:
                        reverse()
                    elif card.type == C2MORE:
                        give += 2
                    elif card.type == C4MORE:
                        give += 4
                        curr_card.color = prev_card.color
                        curr_card.recalculate_value()
                    elif card.type == CCOLOR:
                        curr_card.color = color_translate.get(input("\nNew color:\n"), 0)
                        curr_card.recalculate_value()
                    turn = False
                else:
                    print ("\nNot a playable card")
                    #print (card.possible(curr_card))
                    #print (card == first_card)
                    #print (card)
                    #print (first_card)
                    input ()
                    turn = True

            skips = 0

            remove = reversed(sorted(remove))
            for i in remove:
                players[player_for_turn].remove_card(i)
                if len(players[player_for_turn].deck) < 7:
                    new_card = [card_deck.next()]
                    players[player_for_turn].give_cards(new_card)
            remove = []

            if len(players[player_for_turn].deck) == 0:
                clear()
                print (f"########### {players[player_for_turn].name} wins! ###########")
                on = False
                break

        else:
            skips += 1
            turn = False
    
    if skips == 2:
        curr_card = card_deck.next()
        skips = 0

    next_player()