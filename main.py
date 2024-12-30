import os
import eel
import time

from engine.features import *
from engine.command import *

# Initialize Eel by specifying the folder where your HTML, CSS, and JS files are located
eel.init("web")

playAssistantAudio()

# Function to start the Eel server without opening a browser automatically
def start_eel():
    eel.start("index.html", mode=None, block=False)

# Function to open Arc Browser manually using os.system
def open_arc_browser():
    time.sleep(2)  # Small delay to give Eel time to start
    os.system("open -a 'Arc'   https://silasai.netlify.app")  # Open Arc Browser manually

# Step 1: Start Eel server
start_eel()

# Step 2: Open Arc Browser automatically after Eel server starts
open_arc_browser()

# Keep the script running and let the Eel server run
while True:
    eel.sleep(1)