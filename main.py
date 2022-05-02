import multiprocessing
import detect
import subprocess
import os
import sys
from subprocess import Popen, PIPE, STDOUT

def main():
    weights = "best_weights.pt"
    img_sz = (640, 640)
    start = str(img_sz[1]) + " "
    end = " Done."
    detect = Popen([sys.executable, '-u', "detect.py", "--source", "0", "--weights", weights, "--nosave"], stdout=PIPE, stderr=STDOUT)
    with detect.stdout:
        for line in iter(detect.stdout.readline, b''):
            line = line.decode()
            if line[0] == "0":
                cards = line[line.find(start)+len(start):line.rfind(end)]
                if cards:
                    print(cards)
            else:
                print(line.strip())
    detect.wait()

if __name__ == "__main__":
    main()
