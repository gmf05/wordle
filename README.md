`Solver` class in `solver.py` finds optimal Wordle paths given an initial guess (and a possible solutions list at `five_letter_words_short.txt`).

Running `main.py` plays against the [current NYT Puzzle](https://www.nytimes.com/games/wordle/index.html).

```
python main.py --initial_guess "RAISE"
```

```
INFO:root:TURN 1: Initial guess RAISE
INFO:root:TURN 1: Getting feedback
INFO:root:TURN 1: Feedback is ['R', 'A', 'I', 'S', 'E'], ['absent', 'absent', 'absent', 'absent', 'absent']
INFO:root:TURN 1: Updated total information with feedback
INFO:root:TURN 1: Updating remaining words...
INFO:root:TURN 2: Updated remaining words, N=167
INFO:root:TURN 2: Finding best guess among remaining...
INFO:root:TURN 2: Best guess is COULD. Exp words remaining after is 6.3
INFO:root:TURN 2: Submitting guess...
INFO:root:TURN 2: Submission done!
INFO:root:TURN 2: Getting feedback
INFO:root:TURN 2: Feedback is ['C', 'O', 'U', 'L', 'D'], ['absent', 'absent', 'present', 'present', 'absent']
INFO:root:TURN 2: Updated total information with feedback
INFO:root:TURN 2: Updating remaining words...
INFO:root:TURN 3: Updated remaining words, N=3
INFO:root:TURN 3: Finding best guess among remaining...
INFO:root:TURN 3: Best guess is BULKY. Exp words remaining after is 1.0
INFO:root:TURN 3: Submitting guess...
INFO:root:TURN 3: Submission done!
INFO:root:TURN 3: Getting feedback
INFO:root:TURN 3: Feedback is ['B', 'U', 'L', 'K', 'Y'], ['correct', 'correct', 'correct', 'correct', 'correct']
INFO:root:TURN 3: SOLVED!
```
