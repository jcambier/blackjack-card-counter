import sys
from subprocess import Popen, PIPE, STDOUT
import time

mode_basic = None
detect = None
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
num_cards_detected = {}

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
basic_strategy_splitchart = [["YN","YN","Y","Y","Y","Y","N","N","N","N"],
                            ["YN","YN","Y","Y","Y","Y","N","N","N","N"],
                            ["N","N","N","YN","YN","N","N","N","N","N"],
                            ["N","N","N","N","N","N","N","N","N","N"],
                            ["YN","Y","Y","Y","Y","N","N","N","N","N"],
                            ["Y","Y","Y","Y","Y","Y","N","N","N","N"],
                            ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"],
                            ["Y","Y","Y","Y","Y","N","Y","Y","N","N"],
                            ["N","N","N","N","N","N","N","N","N","N"],
                            ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"]]

def recomended_move(rec_move):
    '''
    Recommends what move to do by translating the inputed acronym into a word or sentence
    Example:
    Input: "H:
    Output: "Recomended Move: Hit"
    '''
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
    '''
    Basic Blackjack strategy
    Looking at the inputed list that represents the starting hand, that has the first 2 numbers as the player's hand and the last number 
    is the dealer's hand, it recommends the move by looking at the strategy chart. 
    '''
    player_hand = sum(player_and_dealer_hand[0:2])
    if 5 <= player_hand <= 7:
        rec_move = "H"
    elif 18 <= player_hand <= 20:
        rec_move = "S"
    elif player_hand == 21:
        rec_move = "B"
    elif player_and_dealer_hand[0] == player_and_dealer_hand[1]:
        rec_move = basic_strategy_splitchart[player_and_dealer_hand[0] - 2][player_and_dealer_hand[2] - 2]
    elif player_and_dealer_hand[0] == 11 or player_and_dealer_hand[1] == 11:
        if player_and_dealer_hand[0] == 11:
            not_ace_card = player_and_dealer_hand[1]
        else:
            not_ace_card = player_and_dealer_hand[0]
        rec_move = basic_strategy_soft_chart[not_ace_card - 2][player_and_dealer_hand[2] - 2]
    else:
        rec_move = basic_strategy_hard_chart[player_hand - 8][player_and_dealer_hand[2] - 2]
    recomended_move(rec_move)

def update_starting_hand(number):
    ''''
    Get player and dealer starting hands by looking at the first 3 cards detected. Those 3 cards are the first 3 cards that the player can view
    in the beginning of the round. After 3 cards are detected, the round begins, a move is recommended, and the round last for 20 seconds. 
    During those 20 seconds, the counting algorithm still runs, however additional cards will not be recorded in list as they are not the 
    starting hand. After 20 seconds, the code will wait for 3 more cards to start the next round. 
    '''
    global start_time
    global player_and_dealer_hand
    global round_num
    # start_time is only 0 when the round hasn't started yet
    if start_time != 0:
        time_passed = time.time() - start_time
        print("Time left in round:", max(0, int(20 - time_passed)))
        #Only when the 20 seconds pass does a new round start a new hand is given
        if time_passed > 20:
            start_time = 0
            player_and_dealer_hand = []
    #This is adding the first 3 cards detected to a list
    if len(player_and_dealer_hand) < 3:
        if number == "J" or number == "Q" or number == "K":
            number = "10"
        elif number == "A":
            number = "11"
        player_and_dealer_hand.append(int(number))
        #Once all cards are given, the round starts and a move is recommended based on basic strategy chart
        if len(player_and_dealer_hand) == 3:
            round_num += 1
            print("Round:", round_num)
            basic_strategy(player_and_dealer_hand)
            start_time = time.time()
    print("Player and Dealer's Starting Hand", player_and_dealer_hand)

def get_best_bet(count):
    '''
    Gets the running count of cards based on how 
    many cards have been played, then tells you 
    if it is more favorable to bet low or high
    '''
    running_count = 0
    # card counting strategy, keeps a running count of cards based on value and quantity
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
    '''
    Count cards based off of detections from the
    card deck dictionary
    '''
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    count = [ 4,   4,   4,   4,   4,   4,   4,   4,    4,   4,   4,   4,   4 ]
    suits = ["c", "d", "h", "s"]
    # loop through the dictionary, if there are any cards
    # marked as 0 they have been seen so we remove 1 from
    # the count
    for i, card in enumerate(cards):
        suits = full_deck.get(card)
        for suit in suits:
            cnt = suits.get(suit)
            if cnt == 0:
                count[i] -= 1
    # remaining cards as a dictionary
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

def process_cards(cards_detected):
    ''''
    Process detected cards and mark them in dictionary
    '''
    cards = cards_detected.split(", ")
    # split the cards given to identify each number/suit
    for card in cards:
        number = card[2]
        suit = card[3]
        if number == "1":
            number = "10"
            suit = card[4]
        # this makes sure it adds the card only once even if it is detected again
        if full_deck.get(number).get(suit) == 1 and not mode_basic:
            update_starting_hand(number)
        # update the deck that we have seen/counted the card
        full_deck.get(str(number)).update({str(suit): 0})
        
def detect_cards(weights, conf_threshold):
    ''''
    Run YOLOv5 detect in background and set global
    variable to read stdout from (for detections)
    '''
    global detect
    # run YOLOv5 detect in the background, with a global variable to read stdout buffer
    detect = Popen([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--conf-thres", str(conf_threshold), "--nosave"], stdout=PIPE, stderr=STDOUT)
    for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            # once YOLOv5 detect starts, it outputs lines starting with 0 (the webcam source)
            if line[0] == "0":
                print("YOLO v5 detector started successfully!")
                break

if __name__ == "__main__":
    '''
    Main loop where we call card detection, processing, and recommendations
    '''
    if sys.argv[1] == "basic":
        mode_basic = True
    elif sys.argv[1] == "advanced":
        mode_basic = False
    if float(sys.argv[2]) > 0.0 and float(sys.argv[2]) < 100.0:
        confidence = float(sys.argv[2])
    if int(sys.argv[3]) >= 0 and float(sys.argv[3]) <= 10:
        false_positive_filter = float(sys.argv[3])
    # configure mode, confidence, and false positive filtering
    assert mode_basic is not None
    assert confidence
    assert false_positive_filter
    print("Blackjack Card Counter")
    print("Starting YOLO v5 detector via webcam (source 0)...")
    weights = "best_weights.pt"
    conf_threshold = confidence
    # use our weights trained on a large dataset of playing cards
    detect_cards(weights, conf_threshold)
    while True:
        for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                # now we check for a new line that has objects printed out (meaning cards were detected)
                cards_detected = line[line.find("640 ")+len("640 "):line.rfind(" Done.")]
                if cards_detected:
                    # this is how we handle false positives,
                    # we have a dictionary where the detected
                    # cards are the key, and the value is the count
                    # (number of times they have been detected)
                    cur = num_cards_detected.get(cards_detected)
                    if cur == None:
                        cur = 0
                    # we update the count based on if the card(s) are
                    # detected
                    num_cards_detected.update({cards_detected: int(cur) + 1})
                    # we only process the cards if they have a count greater 
                    # than the configured false positive filter
                    if num_cards_detected.get(cards_detected) > false_positive_filter:
                        cards_detected = cards_detected[:-1]
                        if mode_basic:
                            # couldn't fix printing for advanced version
                            sys.stdout.write("\033[F"*8)
                            print("\n\n\n\n\nDetected cards: " + cards_detected)
                        else:
                            print("\nDetected cards: " + cards_detected)
                        # process and count cards (update dictionary, count numbers, and if advanced mode is set, strategy is incorporated as well)
                        process_cards(cards_detected)
                        count_cards()
