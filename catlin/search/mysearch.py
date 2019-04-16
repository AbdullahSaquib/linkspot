"""The fuzzy_compare_word takes two inputs as arguments.
The convention is that, the second argument is the correct
word against which the word in the first argument is compared.
It return a real number between 0 and 1, which is a measure
of how well the two words matches. The fuzzy_compare_words
allow one missing word, it can be improved further by adding
another layer of try except statements.
"""


def fuzzy_compare_words(search_word, db_word):
    db_wd = db_word.lower()
    s_wd = search_word.lower()
    db_wd_len = len(db_word)
    s_wd_len = len(s_wd)
    mc = 1  # marks center
    ml = 0.5  # marks left
    mr = 0.5  # marks right
    marks = 0.0
    for i in range(0, s_wd_len):
        try:
            if s_wd[i] == db_wd[i]:
                marks += mc
                continue
            else:
                raise IndexError
        except IndexError:
            try:
                if s_wd[i] == db_wd[i+1]:
                    marks += mr
                    continue
                else:
                    raise IndexError
            except IndexError:
                try:
                    if s_wd[i] == db_wd[i-1]:
                        marks += ml
                except IndexError:
                    pass

    if db_wd_len < s_wd_len:
        return marks/db_wd_len
    else:
        return marks/s_wd_len


"""A crude function that compares two words to return a
real number between 0 and 1, measuring how well the
two words matches
"""


def compare_words(wd1, wd2):
    marks = 0
    score = 0
    len1 = len(wd1)
    len2 = len(wd2)
    wd1 = wd1.lower()
    wd2 = wd2.lower()
    if len1 < len2:
        ln = len1
    else:
        ln = len2
    for i in range(0, ln):
        if wd1[i] == wd2[i]:
            marks += 1.0
        else:
            marks -= 0.5
    score = marks/ln
    if score < 0:
        return 0
    return score


"""campare_strings compare two strings to return a number
between 0 and 1, measuring how well the two strings matches.
The convention is that the first argument is the searched
string, and the second argument is the title in database,
that is the correct string.
"""


def compare_strings(search_string, db_string):
    search_words_list = search_string.split()
    db_string_words_list = db_string.split()
    marks = 0
    score = 0
    for wd1 in search_words_list:
        for wd2 in db_string_words_list:
            temp = fuzzy_compare_words(wd1, wd2)  # change compare words here
            if temp > marks:
                marks = temp
            if marks == 1:
                break
        score += marks
        marks = 0
    len1 = len(search_words_list)
    return score/len1


"""sort the list of strings against the given search string
"""


def search_sort(search_string, db_titles_list, max_results=10):
    threshold = 0.2
    sorted_array = []
    score_array = []
    for db_string in db_titles_list:
        score_array.append(compare_strings(search_string, db_string))
    print(score_array)
    for i in range(0, max_results):
        max1 = max(score_array)
        if max1 > threshold:
            index = score_array.index(max1)
            sorted_array.append(db_titles_list[index])
            score_array[index] = 0
    return sorted_array


db1 = [
    'How to write',
    'About life',
    'The door of life',
    'My pen says',
    'Django Web Development',
    'English Poems by Robert Frost',
    'Hindi Poems by Kumar Vishawas',
    'Django Codes',
    'Classes Django',
    'Flask Development Classes',
    'Web Spider',
    'Django Learning',
    'flasky things',
]
db2 = [
    'Python',
    'Django',
    'Other Frameworks',
    'Machine Learning',
    'Neural Networks',
    'Computational Physics,'
    'Django REST API',
    'English Poems - By Robert Frost',
    'Hindi Poems - By Kumar Vishawas',
    'FPS Games',
]

# search_string = 'Django class'
# print(search_sort(search_string, db1))
