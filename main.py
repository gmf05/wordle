import argparse
import time
import logging
from wordle.webdriver import WebDriver
from wordle.solver import Solver
from wordle.utils import web_feedback_to_information, combine_information


def main(driver, solver, initial_guess):

    # first turn: submit initial guess
    driver = WebDriver(headless=False, live=True)
    driver.start_game()
    time.sleep(2)
    driver.type_word(initial_guess)
    driver.submit()

    logging.info('TURN 1: Initial guess {}'.format(initial_guess))

    # subsequent turns: repeat up to 5x
    # get feedback. apply feedback to update remaining words. compute best guess. submit
    for turn_number in range(1, 6):

        logging.info('TURN {}: Getting feedback'.format(str(turn_number)))
        letters, states = driver.get_turn_feedback(turn_number)
        logging.info('TURN {}: Feedback is {}, {}'.format(str(turn_number), str(letters), str(states)))
        assert 'tbd' not in states  # TODO: note -- need an error handler if these are unexpected!!!  else get feedback again

        # check whether we have solved it
        if states == ['correct']*5:
            logging.info('TURN {}: SOLVED!'.format(str(turn_number)))
            break

        new_info = web_feedback_to_information(letters, states)
        solver.update_information(combine_information(solver._information, new_info))
        logging.info('TURN {}: Updated total information with feedback'.format(str(turn_number)))

        logging.info('TURN {}: Updating remaining words...'.format(turn_number))
        solver.update_remaining_words()
        num_remain = len(solver._remain_words)
        logging.info('TURN {}: Updated remaining words, N={}'.format(str(turn_number+1), str(num_remain)))

        logging.info('TURN {}: Finding best guess among remaining...'.format(str(turn_number+1)))
        guess, exp_remain = solver.compute_best_guess()
        logging.info('TURN {}: Best guess is {}. Exp words remaining after is {}'.format(str(turn_number+1), guess, str(exp_remain)))

        logging.info('TURN {}: Submitting guess...'.format(str(turn_number+1)))
        driver.type_word(guess)
        driver.submit()
        logging.info('TURN {}: Submission done!'.format(str(turn_number+1)))

        # TODO: abandon guessing if we win


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--initial_guess", help="Select which word to start with", default="RAISE", type=str)
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    solver = Solver()

    # with WebDriver(headless=False) as driver:
    driver = None

    main(driver, solver, args.initial_guess)


























