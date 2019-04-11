def compare_words(search_word, db_word):
    db_wd = db_word.lower() #is
    s_wd = search_word.lower() #summary
    db_wd_len = len(db_word)
    s_wd_len = len(s_wd)
    mc = 1
    ml = 0.5
    mr = 0.5
    score = 0
    marks = 0.0
    for i in range(0, s_wd_len):
        try :
            if s_wd[i] == db_wd[i]:
                marks += mc
                # print(s_wd[i], marks)
                continue
            else:
                raise
        except :
            try :
                if s_wd[i] == db_wd[i+1]:
                    marks += ml
                    # print(s_wd[i+1], marks)
                    continue
                else:
                    raise
            except:
                try :
                    if s_wd[i] == db_wd[i-1]:
                        marks += ml
                        # print(s_wd[i+1], marks)
                except:
                    pass

    if db_wd_len < s_wd_len:
        return marks/db_wd_len
    else :
        return marks/s_wd_len

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
