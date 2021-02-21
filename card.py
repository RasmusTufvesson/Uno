import random

C0 = 0
C1 = 1
C2 = 2
C3 = 3
C4 = 4
C5 = 5
C6 = 6
C7 = 7
C8 = 8
C9 = 9
CSWITCH = 10
CBLOCK = 11
C2MORE = 12
C4MORE = 13
CCOLOR = 14
TYPE_TRANSLATOR = {0: "0", 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: "reverse", 11: "block", 12: "+2", 13: "+4", 14: "color choice"}

RED = 0
BLUE = 1
YELLOW = 2
GREEN = 3
BLACK = 4
COLOR_TRANSLATOR = {0: "red", 1: "blue", 2: "yellow", 3: "green", 4: "black"}
color_translate = {"red": 0, "blue": 1, "yellow": 2, "green": 3}

COLORS = range(4)
TYPES = range(15)

class Card:
    def __init__(self, color, card_type):
        if card_type in (C4MORE, CCOLOR):
            self.color = BLACK
        else:
            self.color = color
        #self.color = (c if card_type in (C4MORE, CCOLOR) )
        self.type = card_type
    
    def possible(self, other):
        return self.color == other.color or self.type == other.type or self.color == BLACK
    
    def get_color(self):
        return COLOR_TRANSLATOR[self.color]
    def get_type(self):
        return TYPE_TRANSLATOR[self.type]
    
    def __str__(self):
        return self.get_color() + " " + self.get_type()
    def __eq__(self, other):
        return type(self) == type(other) and self.color == other.color and self.type == other.type
    def __gt__(self, other):
        selfvalue = (self.color * 100) + self.type
        othervalue = (other.color * 100) + other.type
        return selfvalue > othervalue
    def __lt__(self, other):
        selfvalue = (self.color * 100) + self.type
        othervalue = (other.color * 100) + other.type
        return selfvalue < othervalue

def gen_card():
    return Card(random.choice(COLORS), random.choice(TYPES))

