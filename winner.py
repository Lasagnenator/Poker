import itertools

RANK_ORDER = "A234567890JQKA"
BASE_ORDER = "234567890JQKA"

def sort_cards(cards, reverse=True):
    def _key(x):
        return BASE_ORDER.index(x[0])
    return sorted(cards, key=_key, reverse = reverse)
    

def all_pairs(cards):
    out = []
    for pair in itertools.combinations(cards,2):
        if pair[0][0]==pair[1][0]:
            out.append(list(pair))
    return out

def all_triples(cards):
    out = []
    for trip in itertools.combinations(cards,3):
        #print(trip)
        if trip[0][0]==trip[1][0]==trip[2][0]:
            out.append(list(trip))
    return out

def is_full_house(cards):
    #if len(all_triples(cards))==1:
        #if len(all_pairs(cards))==4:
            #return True

    if cards[0][0]==cards[1][0]==cards[2][0]:
        if cards[3][0]==cards[4][0]:
            return [cards[0][0], cards[3][0]]
    elif cards[2][0]==cards[3][0]==cards[4][0]:
        if cards[0][0]==cards[1][0]:
            return [cards[2][0], cards[0][0]]
    
    return False

def is_flush(five):
    if five[0][1]==five[1][1]==five[2][1]==five[3][1]==five[4][1]:
        return sort_cards([five[0][0], five[1][0], five[2][0], five[3][0], five[4][0]])
    return False

def is_straight(cards):
    if cards[0][0]+cards[1][0]+cards[2][0]+cards[3][0]+cards[4][0] in RANK_ORDER:
        return cards[4][0]
    #need to check if ace is first
    if cards[4][0]+cards[0][0]+cards[1][0]+cards[2][0]+cards[3][0]=="A2345":
        return cards[3][0]
    return False

def is_four(cards):
    if cards[0][0]==cards[1][0]==cards[2][0]==cards[3][0]:
        return [cards[1][0], cards[4][0]]
    if cards[4][0]==cards[1][0]==cards[2][0]==cards[3][0]:
        return [cards[1][0], cards[0][0]]
    return False

def is_triple(cards):
    if cards[0][0]==cards[1][0]==cards[2][0]:
        return [cards[2][0], *sort_cards([cards[3][0], cards[4][0]])]
    if cards[3][0]==cards[1][0]==cards[2][0]:
        return [cards[2][0], *sort_cards([cards[0][0], cards[4][0]])]
    if cards[3][0]==cards[4][0]==cards[2][0]:
        return [cards[2][0], *sort_cards([cards[0][0], cards[1][0]])]
    return False

def is_two_pair(cards):
    #sorted so it reduces testing
    if cards[0][0]==cards[1][0]:
        if cards[2][0]==cards[3][0]:
            return [*sort_cards([cards[0][0], cards[2][0]]), cards[4][0]]
        elif cards[3][0]==cards[4][0]:
            return [*sort_cards([cards[0][0], cards[3][0]]), cards[2][0]]
        
    elif cards[1][0]==cards[2][0]:
        if cards[3][0]==cards[4][0]:
            return [*sort_cards([cards[1][0], cards[3][0]]), cards[0][0]]
    return False

def is_pair(cards):
    if cards[0][0]==cards[1][0]:
        return [cards[0][0], *sort_cards([cards[2][0], cards[3][0], cards[4][0]])]
    if cards[1][0]==cards[2][0]:
        return [cards[1][0], *sort_cards([cards[0][0], cards[3][0], cards[4][0]])]
    if cards[2][0]==cards[3][0]:
        return [cards[2][0], *sort_cards([cards[0][0], cards[1][0], cards[4][0]])]
    if cards[3][0]==cards[4][0]:
        return [cards[3][0], *sort_cards([cards[0][0], cards[1][0], cards[2][0]])]
    return False

comb_order = ["Straight flush", "Four of a kind", "Full house",
              "Flush", "Straight", "Three of a kind", "Two pairs",
              "Pair", "High card"]
def sort_highest(combs):
    #all seven cards
    #determines highest value combination
    #returns list of the combination that is highest
    combs = list(set(combs))
    def _key(x):
        return comb_order.index(x[0])
    combs = sorted(combs, key=_key)
    #now take highest type
    best_type = combs[0][0]
    new = []
    for comb in combs:
        if comb[0]==best_type:
            new.append(comb)
    #print(new)
            
    #now to sort out equals
    best = 0
    for i in range(1, len(new)):
        for j in range(1, len(new[0])):
            prev = BASE_ORDER.index(new[best][j])
            test = BASE_ORDER.index(new[i][j])
            if test<prev: #higher is better
                break
            if test>prev:
                best = i
    #print(new[best])
            
    return new[best]

def strip_suits(cards):
    out = []
    for c in cards:
        out.append(c[0])
    return out

def get_highest_comb(cards):
    #all seven cards
    plays = []
    for five in itertools.combinations(cards, 5): #21 different combinations
        play = sort_cards(five, reverse=False)
        
        if is_flush(play) and is_straight(play): #straight flush
            plays.append((comb_order[0], is_straight(play)))
            
        elif is_four(play): #four of a kind
            plays.append((comb_order[1], *is_four(play)))
            
        elif is_full_house(play): #full house
            plays.append((comb_order[2], *is_full_house(play)))
            
        elif is_flush(play): #flush
            plays.append((comb_order[3], *is_flush(play)))
            
        elif is_straight(play): #straight
            plays.append((comb_order[4], is_straight(play)))
            
        elif is_triple(play): #three of a kind
            plays.append((comb_order[5], *is_triple(play)))
            
        elif is_two_pair(play): #two pair
            plays.append((comb_order[6], *is_two_pair(play)))
            
        elif is_pair(play): #pair
            plays.append((comb_order[7], *is_pair(play)))
            
        else: #highcard
            plays.append((comb_order[8], *strip_suits(sort_cards(play))))
    #print(plays)
    #remove duplicates
    plays = list(set(plays))
    #print(plays)
    highest = sort_highest(plays)
    #print(highest)
    return highest

def compare_hand(p1_hand, p2_hand):
    #hand is all seven cards
    #determines winner of two players
    #return 1 if p2>p1, 0 if p2=p1, -1 if p2<p1
    best_p1 = get_highest_comb(p1_hand)
    best_p2 = get_highest_comb(p2_hand)
    p1_index = comb_order.index(best_p1[0])
    p2_index = comb_order.index(best_p2[0])
    if p2_index<p1_index: #p2 better
        return 1
    if p2_index>p1_index: #p1 better
        return -1

    #same type
    best = 0
    for j in range(1, len(best_p1)):
        prev = BASE_ORDER.index(best_p1[j])
        test = BASE_ORDER.index(best_p2[j])
        if test<prev: #higher is better
            best = -1
            break
        if test>prev:
            best = 1
    return best

def determine_winner_cards(_player_hands, table_cards):
    #list of 2-card hands and the 5 on table
    #determines the winner
    #returns the wining hand and type of win
    player_hands = []
    for i in range(len(_player_hands)):
        player_hands.append(_player_hands[i]+table_cards)
    num = len(player_hands)
    best = [0]
    for i in range(1,num):
        #only need to take the first of tie as all others are equal
        comp = compare_hand(player_hands[best[0]], player_hands[i])
        if comp==1: #p2 better
            best = [i]
        if comp==0: #tie
            best.append(i)

    #return best

    win_type = get_highest_comb(player_hands[best[0]])[0]

    return best, win_type

def fname_to_cards(fnames):
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
    for i in range(len(cards)):
        cards[i] += get_suit(fnames[i])
    return cards

def get_suit(fname):
    if "Clubs" in fname:
        return "C"
    elif "D" in fname:
        return "D"
    elif "H" in fname:
        return "H"
    elif "S" in fname:
        return "S"

def determine_winner(fnames_hands, fnames_table):
    hands = []
    for hand in fnames_hands:
        hands.append(fname_to_cards(hand))
    table = fname_to_cards(fnames_table)

    best, win_type = determine_winner_cards(hands, table)

    best_hands = []
    for i in best:
        best_hands.append(fnames_hands[i])

    return best_hands, win_type
