import argparse
import logging
from wordle.solver import Solver
from wordle.utils import new_information, update_information


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--guess", help="Select which word to start with", default="SLATE", type=str, nargs='+')
    parser.add_argument("--solution", help="Solution word", type=str)
    args = parser.parse_args()

    logging.getLogger().setLevel(logging.INFO)

    solver = Solver()
    solution = args.solution
    information = new_information()

    for guess in args.guess:
        information = update_information(information, guess, solution)

    solver.update_information(information)
    solver.update_remaining_words()
    logging.info('Best Guesses:')
    logging.info('\n' + str(solver.compute_best_guess_list().head(25)))


























