import glob
import random

_cards_path = glob.glob("./Cards/*.png")

def create_deck(num):
    cards = _cards_path*num
    random.shuffle(cards)
    return cards


