import re
import shutil
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# first pass at autodetecting firefox path
def __find_path():
    if sys.platform == "win32":
        path = next((os.path.join(p, "Mozilla Firefox", "firefox.exe") for p in [os.getenv("PROGRAMFILES"), os.getenv("PROGRAMFILES(X86)") ] if p and os.path.exists(os.path.join(p, "Mozilla Firefox"))), None)
    elif sys.platform == "darwin":
        path = '/Applications/Firefox.app/Contents/MacOS/firefox'
    else:  # Linux (including Snap version)
        #snap_path = '/snap/firefox/current/usr/bin/firefox'
        snap_path = '/snap/firefox/current/usr/lib/firefox/firefox'
        path = '/usr/bin/firefox' if os.path.exists('/usr/bin/firefox') and not os.path.isdir('/usr/bin/firefox') else None
    
        # If not found, check for Snap's path
        #if not path:
        #    snap_path = '/snap/firefox/current/usr/bin/firefox'
        #    path = snap_path if os.path.exists(snap_path) else None
        # # TODO: snap detection needs to be better above
        path = snap_path

    return path

FIREFOX_BINARY_PATH = __find_path() 


class WebDriver:

    def __init__(self, headless=True, live=False, hard_mode=False):
        self._headless = headless

        if live:
            options = Options()
            options.binary_location = FIREFOX_BINARY_PATH 
            print(options.binary_location)
            # options.log = '/dev/null'  # hiding log
            if self._headless:
                options.add_argument('--headless')
            self._driver = webdriver.Firefox(options=options)
        else:
            self._driver = None

    # this will be forced if live is not specified / live is False
    # this a safer way to initialize bc it ensures any child browser process gets killed when we hit an error
    # as __exit__() will be run for any __enter__()
    def __enter__(self):
        options = Options()
        options.binary_location = FIREFOX_BINARY_PATH 
        print(options.binary_location)

        # options.log = '/dev/null'  # hiding log
        if self._headless:
            options.add_argument('--headless')
        self._driver = webdriver.Firefox(options=options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

    def start_game(self, hard_mode=False):
        url = 'https://www.nytimes.com/games/wordle/index.html'
        self._driver.get(url)
        time.sleep(3)  # how to determine in general?
   
        # TODO: seems we can drop this with latest page changes (?)
        try:
            continue_button = self._driver.find_element(By.XPATH, '//button[@class="purr-blocker-card__button"]')
            if continue_button:
                time.sleep(1)
                continue_button.click()
        except:
            pass

        self._driver.find_element(By.XPATH, '//button[@data-testid="Play"]').click()
        
        try:
            time.sleep(1)
            self._driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        except:
            pass
        
        if hard_mode:
            time.sleep(3.5)
            self._driver.find_element(By.XPATH, '//button[@aria-label="Settings"]').click()
            time.sleep(1.5)
            self._driver.find_element(By.XPATH, '//button[@aria-label="Hard Mode"]').click()
            time.sleep(0.5)
            self._driver.find_element(By.XPATH, '//body').send_keys(Keys.ESCAPE)

    def type_word(self, word):
        assert len(word) <= 5, 'Submission is too long'
        self._driver.find_element(By.XPATH, '//body').send_keys(word)

    def submit(self):
        self._driver.find_element(By.XPATH, '//body').send_keys(Keys.ENTER)
        time.sleep(1.5)
        # assert turn number changed, update

    def clear_word(self):
        self._driver.find_element(By.XPATH, '//body').send_keys(Keys.BACKSPACE * 5)
        # TODO: do we want to assert the clear worked?
        # letters, states = self.__get_turn_feedback(self._turn_number)
        # assert letters == ['', '', '', '', ''], 'Clear failed'

    def __get_game_state(self):
        row_divs = [self._driver.find_element(By.XPATH, '//div[@aria-label="Row {}"]'.format(str(n))) for n in range(1, 6)]
        row_tiles = [[rr for rr in r.find_elements(By.TAG_NAME, 'div') if rr.get_attribute('aria-label') is not None] for r in row_divs ]
        tile_matrix = [[t.get_attribute('aria-label') for i, t in enumerate(r)] for j, r in enumerate(row_tiles)]
        letter_matrix = [[re.findall('[1-5][a-z][a-z] letter, ([A-Z]?)', x)[0] for x in t] for t in tile_matrix]
        state_matrix = [[t.get_attribute('data-state') for t in r] for r in row_tiles]
        return letter_matrix, state_matrix

    def get_turn_feedback(self, turn_number):
        letter_matrix, state_matrix = self.__get_game_state()
        letters = letter_matrix[turn_number-1]
        states = state_matrix[turn_number-1]
        return letters, states

