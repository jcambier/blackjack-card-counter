from re import A
import sys
from subprocess import Popen, PIPE, STDOUT
import time

detecting = False
detect = ""
full_deck = {
    "2": {"c": 1, "d": 1, "h": 1, "s": 1},
    "3": {"c": 1, "d": 1, "h": 1, "s": 1},
    "4": {"c": 1, "d": 1, "h": 1, "s": 1},
    "5": {"c": 1, "d": 1, "h": 1, "s": 1},
    "6": {"c": 1, "d": 1, "h": 1, "s": 1},
    "7": {"c": 1, "d": 1, "h": 1, "s": 1},
    "8": {"c": 1, "d": 1, "h": 1, "s": 1},
    "9": {"c": 1, "d": 1, "h": 1, "s": 1},
    "10": {"c": 1, "d": 1, "h": 1, "s": 1},
    "J": {"c": 1, "d": 1, "h": 1, "s": 1},
    "Q": {"c": 1, "d": 1, "h": 1, "s": 1},
    "K": {"c": 1, "d": 1, "h": 1, "s": 1},
    "A": {"c": 1, "d": 1, "h": 1, "s": 1}
}

player_and_dealer_hand = []

round_num = 0

start_time = 0

basic_strategy_hard_chart = [["H","H","H","H","H","H","H","H","H","H"],
                             ["H","D","D","D","D","H","H","H","H","H"],
                             ["D","D","D","D","D","D","D","D","H","H"],
                             ["D","D","D","D","D","D","D","D","D","D"],
                             ["H","H","S","S","S","H","H","H","H","H"],
                             ["S","S","S","S","S","H","H","H","H","H"],
                             ["S","S","S","S","S","H","H","H","H","H"],
                             ["S","S","S","S","S","H","H","H","H","H"],
                             ["S","S","S","S","S","H","H","H","H","H"],                        
                             ["S","S","S","S","S","S","S","S","S","S"]]

basic_strategy_soft_chart = [["H","H","H","D","D","H","H","H","H","H"],
                            ["H","H","H","D","D","H","H","H","H","H"],         
                            ["H","H","D","D","D","H","H","H","H","H"],
                            ["H","H","D","D","D","H","H","H","H","H"],               
                            ["H","D","D","D","D","H","H","H","H","H"],             
                            ["Ds","Ds","Ds","Ds","Ds","S","S","H","H","H"],
                            ["S","S","S","S","Ds","S","S","S","S","S"],
                            ["S","S","S","S","S","S","S","S","S","S"]]

basic_strategy_split_chart = [["YN","YN","Y","Y","Y","Y","N","N","N","N"],
                              ["YN","YN","Y","Y","Y","Y","N","N","N","N"],
                              ["N","N","N","YN","YN","N","N","N","N","N"],
                              ["N","N","N","N","N","N","N","N","N","N"],
                              ["YN","Y","Y","Y","Y","N","N","N","N","N"],
                              ["Y","Y","Y","Y","Y","Y","N","N","N","N"],
                              ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"],
                              ["Y","Y","Y","Y","Y","N","Y","Y","N","N"],
                              ["N","N","N","N","N","N","N","N","N","N"],
                              ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"]]

def get_best_bet(count):
    '''
    Input 
    '''
    running_count = 0
    for i in range(13):
        if 0 <= i <= 4:
            running_count += 4 - count[i]
        elif 8 <= i <= 12:
            running_count -= 4 - count[i]
    if running_count <= 0:
        decision = "so you should bet low"
    else: 
        decision = "so you should bet high" 
    print("the count is", running_count, decision)

def count_cards():
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    count = [ 4,   4,   4,   4,   4,   4,   4,   4,    4,   4,   4,   4,   4 ]
    suits = ["c", "d", "h", "s"]
    for i, card in enumerate(cards):
        suits = full_deck.get(card)
        for suit in suits:
            cnt = suits.get(suit)
            if cnt == 0:
                count[i] -= 1
    numbers_remaining = {
        "2": count[0],
        "3": count[1],
        "4": count[2],
        "5": count[3],
        "6": count[4],
        "7": count[5],
        "8": count[6],
        "9": count[7],
        "10": count[8],
        "J": count[9],
        "Q": count[10],
        "K": count[11],
        "A": count[12]
    }
    print("There are %s cards left" % sum(count), numbers_remaining)
    get_best_bet(count)

def recomended_move(rec_move):
    if rec_move == "H":
        move = "Hit"
    
    elif rec_move == "S":
        move = "Stand"
    
    elif rec_move == "D":
        move = "Double if allowed, otherwise Hit"
    
    elif rec_move == "Ds":
        move = "Double if allowed, otherwise Stand"

    elif rec_move == "Y":
        move = "Split"

    elif rec_move == "N":
        move = "Hit instead of splitting"

    elif rec_move == "YN":
        move = "Split only if Double after spliting is allowed, otherwise Hit"

    elif rec_move == "B":
        move = "Blackjack! YOU WIN!!!"
    
    print("Recomended Move:", move)

def basic_strategy(player_and_dealer_hand):

    player_hand = sum(player_and_dealer_hand[0:2])
    if 5 <= player_hand <= 7:
        rec_move = "H"

    elif 18 <= player_hand <= 20:
        rec_move = "S"

    elif player_hand == 21:
        rec_move = "B"

    elif player_and_dealer_hand[0] == player_and_dealer_hand[1]:
        rec_move = basic_strategy_split_chart[player_and_dealer_hand[0] - 2][player_and_dealer_hand[2] - 2]

    elif player_and_dealer_hand[0] == 11 or player_and_dealer_hand[1] == 11:
        if player_and_dealer_hand[0] == 11:
            not_ace_card = player_and_dealer_hand[1]
        else:
            not_ace_card = player_and_dealer_hand[0]
        rec_move = basic_strategy_soft_chart[not_ace_card - 2][player_and_dealer_hand[2] - 2]
    else:
        rec_move = basic_strategy_hard_chart[player_hand - 8][player_and_dealer_hand[2] - 2]

    recomended_move(rec_move)

def get_player_and_dealer_hands(number):
    global start_time
    global player_and_dealer_hand
    global round_num

    if start_time != 0:
        time_passed = time.time() - start_time
        print("Time passed:", time_passed)
        if time_passed > 20:
            start_time = 0
            player_and_dealer_hand = []
    
    if len(player_and_dealer_hand) < 3:
        if number == "J" or number == "Q" or number == "K":
            number = "10"
        elif number == "A":
            number = "11"

        player_and_dealer_hand.append(int(number))

        if len(player_and_dealer_hand) == 3:
            round_num += 1
            print("Round:", round_num)
            basic_strategy(player_and_dealer_hand)
            start_time = time.time()
    
    print("The list", player_and_dealer_hand)
    
def process_cards(cards_detected):
    cards = cards_detected.split(", ")
    for card in cards:
        number = card[2]
        suit = card[3]
        if number == "1":
            number = "10"
            suit = card[4]
        if full_deck.get(number).get(suit) == 1: #This makes sure it adds the card only once even if it is detected again
            get_player_and_dealer_hands(number)
        full_deck.get(str(number)).update({str(suit): 0})
        
        

def detect_cards(weights, conf_threshold):
    global detect
    detect = Popen([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--conf-thres", str(conf_threshold), "--nosave"], stdout=PIPE, stderr=STDOUT)
    for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                print("YOLO v5 detector started successfully!")
                break

def main():
    print("Blackjack Card Counter")
    print("Starting YOLO v5 detector via webcam (source 0)...")
    weights = "best_weights.pt"
    conf_threshold = 0.8
    detect_cards(weights, conf_threshold)
    while True:
        for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                cards_detected = line[line.find("640 ")+len("640 "):line.rfind(" Done.")]
                if cards_detected:
                    cards_detected = cards_detected[:-1]
                    print("\nDetected cards: " + cards_detected)
                    process_cards(cards_detected)
                    count_cards()
                    


if __name__ == "__main__":
    main()

