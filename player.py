
from card import gen_card

class Player:
    def __init__(self, name, cards = 7):
        self.name = name
        if type(cards) == int:
            self.card_num = cards
            self.deck = self.generate_deck()
        else:
            self.deck = cards
            self.card_num = len(self.deck)
    
    def generate_deck(self) -> list:
        out = []
        for i in range(self.card_num):
            out.append(gen_card())
        return out
    
    def get_deck(self) -> tuple:
        return tuple(self.deck)
    
    def give_random_cards(self, number):
        for i in range(number):
            self.deck.append(gen_card())
    
    def give_cards(self, cards):
        for i in cards:
            if i != None:
                self.deck.append(i)
    
    def remove_card(self, card_id):
        del self.deck[card_id]
    
    def __str__(self):
        s = str(list(map(str, self.deck))).replace("'", "")
        return f"Deck<{s[1:len(s)-1]}>"