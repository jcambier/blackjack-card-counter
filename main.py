import sys
from subprocess import Popen, PIPE, STDOUT
#import pyfiglet

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
cur_deck = full_deck.copy()

def count_cards():
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    count = [ 4,   4,   4,   4,   4,   4,   4,   4,    4,   4,   4,   4,   4 ]
    suits = ["c", "d", "h", "s"]
    for i, card in enumerate(cards):
        suits = cur_deck.get(card)
        for suit in suits:
            cnt = suits.get(suit)
            if cnt == 0:
                count[i] -= 1
    print("There are %s cards left" % sum(count))
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
    print(numbers_remaining)
    return sum(count), numbers_remaining

def get_best_play(cards_detected):
    # here is where we tell the player what to do based on the cards left/value of cards left
    total_cards, numbers_remaining = count_cards()
    return "<do this>"

def process_cards(cards_detected):
    cards = cards_detected.split(", ")
    for card in cards:
        print("card:", card)
        number = card[2]
        print("number:", number)
        suit = card[3]
        print("suit:", suit)

        if number == "1":
            number = "10"
            suit = card[4]
        
        cur_deck.get(str(number)).update({str(suit): 0})

def detect_cards():
    weights = "best_weights.pt"
    conf_treshold = 0.5
    global detect
    detect = Popen([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--conf-thres", str(conf_treshold), "--nosave"], stdout=PIPE, stderr=STDOUT)
    for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                print("YOLO v5 detector started successfully!\n")
                break

def main():
    #pyfiglet.print_figlet("Blackjack Card Counter")
    print("Starting YOLO v5 detector via webcam (source 0)...")
    detect_cards()
    while True:
        for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                cards_detected = line[line.find("640 ")+len("640 "):line.rfind(" Done.")]
                if cards_detected:
                    cards_detected = cards_detected[:-1]
                    print("Detected cards: " + cards_detected)
                    cards_detected = process_cards(cards_detected)
                    play = get_best_play(cards_detected)
                    print("Based off of the cards present, you should %s\n" % play)

if __name__ == "__main__":
    main()
