import sys
from subprocess import Popen, PIPE, STDOUT
import pyfiglet

detecting = False
detect = ""

def get_best_play(cards_detected):
    return "GOOOO"

def detect_cards():
    weights = "best_weights.pt"
    conf_treshold = 0.75
    global detect
    detect = Popen([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--conf-thres", str(conf_treshold), "--nosave"], stdout=PIPE, stderr=STDOUT)

def main():
    pyfiglet.print_figlet("Blackjack Card Counter")
    detect_cards()
    while True:
        input("Press enter to capture cards")
        last_cards = ""
        for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                cards_detected = line[line.find("640 ")+len("640 "):line.rfind(" Done.")]
                if cards_detected:
                    if last_cards != cards_detected:
                        print("Detected cards: " + cards_detected)
                        play = get_best_play(cards_detected)
                        print("Based off of the cards present, you should %s\n" % play)
                    last_cards = cards_detected

if __name__ == "__main__":
    main()
