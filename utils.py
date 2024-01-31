def new_information():
    information = {
        'correct': [''] * 5,
        'saturated': set(),
        'present': set(),
        'absent': set(),  # TODO: maybe absent is subsumed by wrong_place
        'wrong_place': [set(), set(), set(), set(), set()]
    }
    return information



def update_information(information, guess, solution):

    considered = set(range(5))
    removed = []

    for n in considered:
        if guess[n] == solution[n]:
            information['correct'][n] = guess[n]
            removed.append(n)

    considered = considered - set(removed)

    for n in considered:
        if guess[n] in information['saturated']:
            information['wrong_place'][n] = information['wrong_place'][n].union(guess[n])
        elif guess[n] in information['correct'] and guess[n] != solution[n]:
            information['saturated'] = information['saturated'].union(guess[n])
            information['wrong_place'][n] = information['wrong_place'][n].union(guess[n])
        elif guess[n] in solution:
            information['present'] = information['present'].union(guess[n])
            information['wrong_place'][n] = information['wrong_place'][n].union(guess[n])
        elif guess[n] not in information['absent']:
            information['absent'] = information['absent'].union(guess[n])

    return information


def combine_information(old_info, new_info):

    combined_info = old_info.copy()

    for n in range(5):
        combined_info['correct'][n] = new_info['correct'][n] if new_info['correct'][n] != '' else old_info['correct'][n]
        combined_info['wrong_place'][n] = old_info['wrong_place'][n].union(new_info['wrong_place'][n])

    for c in ['saturated', 'present', 'absent']:
        combined_info[c] = old_info[c].union(new_info[c])

    return combined_info


def information_excludes_word(information, word):

    # correct-ness exclusion
    for n, char in enumerate(information['correct']):
        if char != '' and word[n] != char:
            return True

    # present exclusion -- must have any known "present" chars
    for char in information['present']:
        if char not in word:
            return True

    # absent exclusion -- cannot have any "absent" chars
    for char in information['absent']:
        if char in word:
            return True

    # any known wrong places
    for n in range(5):
        if word[n] in information['wrong_place'][n]:
            return True

    # otherwise we can't tell enough to exclude
    return False


def web_feedback_to_information(letters, states):

    information = new_information()

    considered = list(range(5))

    for n in considered:
        if states[n] == 'correct':
            information['correct'][n] = letters[n]
            considered.remove(n)

    for n in considered:
        if states[n] == 'absent' and letters[n] in information['correct']:
            information['wrong_place'][n] = information['wrong_place'][n].union(letters[n])
            information['saturated'] = information['saturated'].union(letters[n])
        elif states[n] == 'absent':
            information['absent'] = information['absent'].union(letters[n])
        elif states[n] == 'present':
            information['present'] = information['present'].union(letters[n])
            information['wrong_place'][n] = information['wrong_place'][n].union(letters[n])

    return information


def update_remaining(remain_words, information):
    remain_words = [word for word in remain_words if not information_excludes_guess(information, word)]
    return remain_words

