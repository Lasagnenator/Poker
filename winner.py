import itertools

RANK_ORDER = ["A234567890JQKA"]

def all_pairs(cards):
    out = []
    for pair in itertools.combinations(cards,2):
        if pair[0]==pair[1]:
            out.append(list(pair))
    return out

def all_triples(cards):
    out = []
    for trip in itertools.combinations(cards,3):
        if trip[0]==trip[1]==trip[2]:
            out.append(list(trip))
    return out

def has_full_house(cards):
    if len(all_triples(cards))>=1:
        if len(all_pairs(cards))>=4:
            return True
    return False

def has_flush(cards):
    for five in itertools.combinations(cards, 5):
        if five[0][1]==five[1][1]==five[2][1]==five[3][1]==five[4][1]:
            return True
    return False

def get_highest(cards):
    #all seven cards
    #determines highest value combination
    #returns list of the combination that is highest
    pass

def compare_hand(p1_hand, p2_hand):
    #hand is all seven cards
    #determines winner of two players
    #return 1 if p2>p1, 0 if p2=p1, -1 if p2<p1
    pass

def determine_winner(player_hands, table_cards):
    #list of 2-card hands
    #determines the winner
    for i in range(len(player_hand)):
        player_hand[i].extend(table_cards)
    num = len(player_hands)
    best = [0]
    for i in range(1,num):
        #only need to take the first of tie as all others are equal
        comp = compare_hand(player_hands[best], player_hands[best[0]])
        if comp==1: #p2 better
            best = [i]
        if comp==0: #tie
            best.append(i)
    return best

def convert_fname_to_cards(fnames):
    cards = []
    for fname in fnames:
        if "2" in fname:
            cards.append("2")
        elif "3" in fname:
            cards.append("3")
        elif "4" in fname:
            cards.append("4")
        elif "5" in fname:
            cards.append("5")
        elif "6" in fname:
            cards.append("6")
        elif "7" in fname:
            cards.append("7")
        elif "8" in fname:
            cards.append("8")
        elif "9" in fname:
            cards.append("9")
        elif "10" in fname:
            cards.append("0")
        elif "J" in fname:
            cards.append("J")
        elif "Q" in fname:
            cards.append("Q")
        elif "K" in fname:
            cards.append("K")
        elif "A" in fname:
            cards.append("A")
    for i, card in enumerate(cards):
        cards[i] += get_suit(fnames[i])
    return cards

def get_suit(fname):
    if "C" in fname:
        return "C"
    elif "D" in fname:
        return "D"
    elif "H" in fname:
        return "H"
    elif "S" in fname:
        return "S"
