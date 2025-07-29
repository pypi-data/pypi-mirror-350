from clight.system.importer import cli  # DON'T REMOVE THIS LINE

# import openai==0:28

import os
import sys
import time
import openai
import asyncio
import keyboard
import pyautogui
import pyperclip
import subprocess
from pathlib import Path
from functools import partial
from googletrans import Translator

from modules.ai import AI
