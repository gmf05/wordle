import argparse
import time
import logging
from wordle.webdriver import WebDriver
from wordle.solver import Solver
from wordle.utils import web_feedback_to_information, combine_information


def main(driver, solver, initial_guess, hard_mode):

    # first turn: submit initial guess
    driver.start_game(hard_mode=hard_mode)
    time.sleep(2)
    driver.type_word(initial_guess)
    driver.submit()

    logging.info('TURN 1: Initial guess {}'.format(initial_guess))

    # subsequent turns: repeat up to 5x
    # get feedback. apply feedback to update remaining words. compute best guess. submit
    for turn_number in range(1, 6):

        logging.info(f'TURN {str(turn_number)}: Getting feedback')
        letters, states = driver.get_turn_feedback(turn_number)
        logging.info(f'TURN {str(turn_number)}: Feedback is {str(letters)}, {str(states)}')
        assert 'tbd' not in states  # TODO: note -- need an error handler if these are unexpected!!!  else get feedback again

        # check whether we have solved it
        if states == ['correct']*5:
            logging.info(f'TURN {str(turn_number)}: SOLVED!')

            # if we are not in headless mode, stay alive for a couple minutes to allow for click through
            if not driver._headless:
                time.sleep(120)

            break

        new_info = web_feedback_to_information(letters, states)
        solver.update_information(combine_information(solver._information, new_info))
        logging.info(f'TURN {str(turn_number)}: Updated total information with feedback')

        logging.info(f'TURN {str(turn_number)}: Updating remaining words...')
        solver.update_remaining_words()
        num_remain = len(solver._remain_words)
        logging.info(f'TURN {str(turn_number)}: Updated remaining words, N={str(num_remain)}')

        logging.info(f'TURN {str(turn_number+1)}: Finding best guess among remaining...')
        guess, exp_remain = solver.compute_best_guess()
        logging.info(f'TURN {str(turn_number+1)}: Best guess is {guess}. Exp words remaining after is {str(exp_remain)}')

        logging.info(f'TURN {str(turn_number+1)}: Submitting guess...')
        driver.type_word(guess)
        driver.submit()
        logging.info(f'TURN {str(turn_number+1)}: Submission done!')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--initial_guess", help="Select which word to start with", default="SLATE", type=str)
    parser.add_argument("--show", help="Show browser as it solves", action="store_true")
    parser.add_argument("--hard", help="Toggle hard mode", action="store_true")
    parser.add_argument("--long", help="Toggle long word list", action="store_true")
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    solver = Solver('long' if args.long else 'short')

    # TODO: allow possibility of driver staying open to check analysis
    with WebDriver(headless=not args.show) as driver:
        main(driver, solver, args.initial_guess, args.hard)
        if args.show:
            time.sleep(300)

    # driver = WebDriver(headless=False, live=True)
    # main(driver, solver, args.initial_guess)



