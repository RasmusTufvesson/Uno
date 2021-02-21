from card import *
from player import *
from deck import *
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


player_num = int(input("number of players playing:\n"))
card_deck = Deck()#gen_deck()
curr_card = card_deck.next()
while curr_card.type != BLACK:
    curr_card = card_deck.next()


players = []
for i in range(player_num):
    cards = []
    for j in range(7):
        cards.append(card_deck.next())
    players.append(Player(cards))


curr_player = 0
next_up = True
def reverse():
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
            curr_player = player_num
            #print ("to low")
    #print (curr_player)
    return curr_player

give = 0

on = True
while on:
    clear()
    input ("########### Waiting for player ###########")
    clear()

    for i in range(give):
        players[curr_player].give_cards([card_deck.next()])

    print (f"Current card: {curr_card.get_color() + ' ' + curr_card.get_type()}")

    print ()
    print ("Your cards:")
    #print (players[curr_player])#players[curr_player].deck)
    for i in players[curr_player].deck:
        print (i.get_color(), i.get_type())
    print ()

    card = int(input("Number of card to play:\n"))
    card_num = card - 1
    card = players[curr_player].get_deck()[card_num]
    if card.possible(curr_card):
        players[curr_player].remove_card(card_num)
        if len(players[curr_player].deck) == 6:
            new_card = [card_deck.next()]
            players[curr_player].give_cards(new_card)
            #print (players[curr_player])
            #print (new_card[0])
            #input()
    else:
        print ("\nNot a playable card")
        input ()

    if card.possible(curr_card):
        prev_card = curr_card
        curr_card = card
        if card.type == CBLOCK:
            next_player()
        elif card.type == CSWITCH:
            reverse()
        elif card.type == C2MORE:
            give = 2
        elif card.type == C4MORE:
            give = 4
            curr_card.color = prev_card.color
        elif card.type == CCOLOR:
            curr_card.color = color_translate.get(input("\nNew color:\n"), 0)

    next_player()