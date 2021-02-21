
from card import *
import random

"""
def gen_deck():
    def gen_cards(times, colors, card_type):
        out = []
        for i in range(times):
            for j in colors:
                out.append(Card(j, card_type))
        return out

    deck = []

    for i in range(1, 15):
        if i in [0, 14, 13]:
            deck += gen_cards(1, [0,1,2,3], i)
        else:
            deck += gen_cards(2, [0,1,2,3], i)

    return deck
"""

class Deck:
    def __init__(self):
        deck = []

        for i in range(1, 15):
            if i in [0, 14, 13]:
                deck += self.gen_cards(1, [0,1,2,3], i)
            else:
                deck += self.gen_cards(2, [0,1,2,3], i)

        random.shuffle(deck)

        self.deck = deck
        self.deck_pointer = len(self.deck)-1
    
    def gen_cards(self, times, colors, card_type):
        out = []
        for i in range(times):
            for j in colors:
                out.append(Card(j, card_type))
        return out
    
    def next(self):
        if self.deck_pointer != -1:
            c = self.deck[self.deck_pointer]
            self.deck_pointer -= 1
            #print (c)
            #print (self)
            return c
        else:
            return None
    
    def __str__(self):
        s = str(list(map(str, self.deck))).replace("'", "")
        return f"Deck<{s[1:len(s)-1]}>"
    
    def cards_left(self):
        return self.deck_pointer+1
