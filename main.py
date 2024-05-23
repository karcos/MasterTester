from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import Tag
from typing import *

import locale
import copy

from mastertester import MasterTester
from gui_handler import GUIHandler


if __name__ == '__main__':
    # MasterTester().run()
    a = GUIHandler()
    a.loop()
