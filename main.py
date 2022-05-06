import sys
from subprocess import Popen, PIPE, STDOUT
from subprocess import check_output

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

def get_best_bet(count):
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

def process_cards(cards_detected):
    cards = cards_detected.split(", ")
    for card in cards:
        number = card[2]
        suit = card[3]
        if number == "1":
            number = "10"
            suit = card[4]
        full_deck.get(str(number)).update({str(suit): 0})

def detect_cards(weights, conf_threshold):
    global detect
    #detect = Popen([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--conf-thres", str(conf_threshold), "--nosave"], stdout=PIPE, stderr=STDOUT)
    out = check_output([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--conf-thres", str(conf_threshold), "--nosave"])
    print(out)
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
