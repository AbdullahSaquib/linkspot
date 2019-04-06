def compare_words(wd1, wd2):
    marks=0
    score=0
    len1 = len(wd1)
    len2 = len(wd2)
    wd1 = wd1.lower()
    wd2 = wd2.lower()
    if len1 < len2:
        ln = len1
    else:
        ln = len2
    for i in range(0,ln):
        if wd1[i] == wd2[i]:
            marks += 1.0
        else:
            marks -= 0.5
    score = marks/ln
    if score < 0:
        return 0
    return score

def compare_strings(search_string, db_string):
    search_words_list = search_string.split()
    db_string_words_list = db_string.split()
    marks = 0
    score = 0
    for wd1 in search_words_list:
        for wd2 in db_string_words_list:
            temp = compare_words(wd1,wd2)
            if temp > marks:
                marks = temp
            if marks == 1:
                break
        score += marks
        marks =0
    len1 = len(search_words_list)
    return score/len1

def search_sort(search_string ,db_titles_list, max_results = 10):
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
