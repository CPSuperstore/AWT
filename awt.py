"""
The main script to run an AWT file

usage: awt.py [-h] -b {firefox,chrome,edge} [-e] [-i] [-p] filename

Executes a script to test websites

positional arguments:
  filename              The file to execute

optional arguments:
  -h, --help            show this help message and exit
  -b {firefox,chrome,edge}, --browser {firefox,chrome,edge}
                        The web browser to execute the test in
  -e, --headless        Runs the test in headless mode - Note: Not all
                        browsers support headless execution!
  -i, --highlight       Highlights each element which is selected as the test
                        is executed
  -p, --pause-mode      Pauses execution before terminating at both end of the
                        script and an unhandled exception
"""
import argparse
import logging
import os

import browser
import commands
import globals
from code_block import CodeBlock

# setup logging configurations
logging.basicConfig(
    format='[%(asctime)s] (%(levelname)s) %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# handle command line argument setup
parser = argparse.ArgumentParser(description='Executes a script to test websites')

parser.add_argument(
    'filename',
    help='The file to execute'
)
parser.add_argument(
    "-b", "--browser", help="The web browser to execute the test in", choices=browser.BROWSERS.keys(),
    required=True
)
parser.add_argument(
    "-e", "--headless",
    help="Runs the test in headless mode - Note: Not all browsers support headless execution!",
    action="store_true"
)
parser.add_argument(
    "-i", "--highlight", help="Highlights each element which is selected as the test is executed", action="store_true"
)
parser.add_argument(
    "-p", "--pause-mode",
    help="Pauses execution before terminating at both end of the script and an unhandled exception",
    action="store_true"
)

args = parser.parse_args()

logging.info("Initializing AWT Interpreter...")

# set global properties
globals.filename = args.filename
globals.highlight_mode = args.highlight
globals.terminate_pause = args.pause_mode

# set the filename in the memory heap
globals.memory_heap["filename"] = os.path.basename(globals.filename)

# read the full file which will be executed
# it is read all at once at the start, so file changes during execution will be ignored
with open(globals.filename) as f:
    steps = f.readlines()

# set the application CWD
globals.cwd = os.path.dirname(globals.filename)

logging.info("Initializing Web Browser...")

# initialize the web browser
browser.initialize_browser(args.browser, args.headless)

block = False
code = ""
block_type = None

# import the input file
commands.import_module(globals.filename, None, literal_path=True)

# create a code block from the starting file as the main/starting code block
main = CodeBlock(globals.filename, [], steps)

logging.info("Initialization Complete. Commencing Command Execution...")

# execute the main script
main.execute()

# kill the browser
browser.kill()
quit()