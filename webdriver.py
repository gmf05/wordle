import re
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class WebDriver:

    def __init__(self, headless=True, live=False):
        self._headless = headless

        if live:
            options = webdriver.FirefoxOptions()
            options.binary_location = shutil.which('firefox')
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
        options = webdriver.FirefoxOptions()
        options.binary_location = shutil.which('firefox')
        # options.log = '/dev/null'  # hiding log
        if self._headless:
            options.add_argument('--headless')
        self._driver = webdriver.Firefox(options=options)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.quit()

    def start_game(self):
        url = 'https://www.nytimes.com/games/wordle/index.html'
        self._driver.get(url)
        self._driver.find_element(By.XPATH, '//button[@data-testid="Play"]').click()
        self._driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()

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

