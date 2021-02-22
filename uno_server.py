from card import *
from player import *
from deck import *
import os
import zmq


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def send(mes: str):
    pub.send_string(mes)

def listen():
    data = str(rec.recv())
    #print (data)
    return data[2:len(data)-1]


"""HOST=''
#HOST=input ('what is your host?\n')
PORT=input ('what port do you want to use?\n')
if HOST=='':
    HOST='localhost'
if PORT=='':
    PORT='65432'
PORT=int(PORT)
server=zmq.Context()
pub=server.socket(zmq.PUB)
pub.bind('tcp://*:'+str(PORT))
col=server.socket(zmq.PULL)
col.bind('tcp://*:'+str(PORT+1))"""
PORT = 65432
server = zmq.Context()
pub = server.socket(zmq.PUB)
pub.bind(f"tcp://*:{str(PORT)}")
rec = server.socket(zmq.PULL)
rec.bind(f"tcp://*:{str(PORT + 1)}")


clear()
clients = {}
player_num = int(input("number of players playing:\n"))
print ("waiting for players...")
for i in range(player_num):
    mes = listen().split()
    if mes[0] == "id":
        clients[mes[1]] = mes[2]
#clients = sorted(clients)
card_deck = Deck()#gen_deck()
curr_card = card_deck.next()
while curr_card.type != BLACK:
    curr_card = card_deck.next()


players = []
for i in clients:#range(player_num):
    cards = []
    for j in range(7):
        cards.append(card_deck.next())
    name = clients[i]#input(f"Player {str(i + 1)}'s name: ")
    players.append(Player(name, cards))
    send(f"{i} {str(len(players)-1)}")


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
    send(f"wait {players[curr_player].name}")
    print (f"########### Waiting for {players[curr_player].name} ###########")
    print (f"Current card: {str(curr_card)}")
    print (f"Cards left: {str(card_deck.cards_left())}")
    print (f"########### Waiting for {players[curr_player].name} ###########")
    #input()
    #clear()

    for i in range(give):
        players[curr_player].give_cards([card_deck.next()])
    give = 0

    send(f"{str(curr_player)} cc {curr_card.get_color() + ',' + curr_card.get_type()}")#print (f"Current card: {curr_card.get_color() + ' ' + curr_card.get_type()}")
    #print (f"Current player: {players[curr_player].name}")
    send(f"{str(curr_player)} cl {str(card_deck.cards_left())}")#print (f"Cards left: {str(card_deck.cards_left())}")

    #print ()
    #print ("Your cards:")
    #print (players[curr_player])#players[curr_player].deck)
    players[curr_player].deck = sorted(players[curr_player].deck)
    players_cards = []
    for i in range(len(players[curr_player].deck)):
        players_cards.append(players[curr_player].deck[i].value)#players[curr_player].deck[i].color+","+players[curr_player].deck[i].get_type())#print (str(i+1)+".", players[curr_player].deck[i].get_color(), players[curr_player].deck[i].get_type())
    send(f"{str(curr_player)} ca {' '.join(map(str, players_cards))}")#print ()

    send(f"{str(curr_player)} rc")
    cards = listen().split(" ")#input("Number of card(s) to play:\n").split(" ")
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
                if len(players[player_for_turn].deck) == 7:
                    new_card = [card_deck.next()]
                    players[player_for_turn].give_cards(new_card)
                    #print (players[player_for_turn])
                    #print (new_card[0])
                    #input()
            else:
                send(f"{str(player_for_turn)} np")
                #print ("\nNot a playable card")
                #print (card.possible(curr_card))
                #print (card == first_card)
                #print (card)
                #print (first_card)
                #input ()

            if card.possible(curr_card):# and card == first_card:
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
                    send(f"{str(player_for_turn)} cr")
                    curr_card.color = color_translate.get(listen(), 0)#input("\nNew color:\n"), 0)
                    curr_card.recalculate_value()

        skips = 0

        remove = reversed(sorted(remove))
        for i in remove:
            players[player_for_turn].remove_card(i)
        remove = []

    else:
        skips += 1
    
    if skips == 2:
        curr_card = card_deck.next()
        skips = 0

    next_player()