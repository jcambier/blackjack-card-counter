# How to run:
python3 main.py basic 0.75 10

# Configurable parameters:
- "basic" can be "advanced" if you want to try out the strategy component of the project
- "0.75" is the confidence threshold for YOLOv5 object detection, which can be set from anywhere between 0.0 and 100.0
- "10" is the false positive filter which determines how many occurences of the card(s) must appear before it is added as seen (set from 0-10)
