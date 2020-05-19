#######################################################################
# FILE : ex5.py
# WRITERS : Rotem_Amsalem , ra260296 , 207596297
#           Elia_Hene , eh51195 , 324502145
# EXERCISE : intro2cs ex4 2017-2018
# DESCRIPTION: an implementation of a crossword game.
########################################################################

import sys
import os.path

NUMBER_OF_ARGUMENTS = 4

direction_lst = ['u', 'l', 'r', 'd', 'w', 'x', 'y', 'z']


def check_args(argv):
    """" This function checks the arguments which were given. It checks
    whether the number of arguments is valid or not only if it does,
    the function starts to check the arguments and printed the matching
    error messages according to the instructions. """
    if len(argv) != NUMBER_OF_ARGUMENTS + 1:
        print('ERROR: invalid number of parameters. Please enter word_file '
              'matrix_file output_file direction.')
        return False
    elif len(argv) == NUMBER_OF_ARGUMENTS + 1:
        if not (os.path.isfile(argv[1])):
            print('ERROR: Word file ' + str(argv[1]).split('\\')[-1] +
                  ' does not exist.')
            return False
        if not (os.path.isfile(argv[2])):
            print('ERROR: Matrix file ' + str(argv[2]).split('\\')[-1] +
                  ' does not exist.')
            return False
        for letter in list(argv[4]):
            if letter not in direction_lst:
                print('ERROR: invalid directions.')
                return False
        return True
    else:
        return True


def load_words(file):
    """ This function loading the words from an external file and put it into a
    list of words."""
    words = []
    f_words = open(file)
    for line in f_words:
        word = line.strip()
        if word.isalpha:
            words.append(word.lower())
    f_words.close()
    return words


def load_matrix(file):
    """ This function loading the matrix from an external file and put it
    into a list. This list's members are other lists that are the rows of the
    matrix and each of those lists (the rows) contains the members of the
    columns of the matrix at the matched row."""
    mat_lst = []
    f_mat = open(file)
    for line in f_mat:
        seq = line.strip()
        mat_lst.append(seq.lower())
    for i in range(len(mat_lst)):
        mat_lst[i] = mat_lst[i].split(',')
    f_mat.close()
    return mat_lst


def concat_list(str_lst):
    """ This function receives a list of strings, and return the
    concatenation of the list's parts as one string."""
    length = len(str_lst)  # the list can be an empty list.
    one_str = ''
    for i in range(length):
        one_str = one_str + str_lst[i]
    return one_str


def check_directions(lst1, lst2, words):
    """ This function receives two lists. The first one is matrix list and the
    second is an empty list which in the end will contain the words
    according to each searching words direction."""
    for j in range(len(words)):
        for i in range(len(lst1)):
            if words[j] in lst1[i]:
                for p in range(len(lst1[i])-len(words[j])+1):
                    check = lst1[i][p:p+len(words[j])]
                    if check == words[j]:
                        lst2.append(words[j])
    return lst2


def u_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the up direction."""
    up_lst = []
    word_up_lst = []
    for j in range(len(matrix_lst[0])):
        for i in range(len(matrix_lst)-1, -1, -1):
            row = matrix_lst[i]
            up_lst.append(row[j].lower())
        up_lst.append(' ')
    column_up_lst = str(concat_list(up_lst)).split()
    return check_directions(column_up_lst, word_up_lst, words)


def d_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the down direction. """
    down_lst = []
    word_down_lst = []
    for j in range(len(matrix_lst[0])):
        for i in range(len(matrix_lst)):
            row = matrix_lst[i]
            down_lst.append(row[j].lower())
        down_lst.append(' ')
    column_down_lst = str(concat_list(down_lst)).split()
    return check_directions(column_down_lst, word_down_lst, words)


def r_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the right direction. """
    right_lst = []
    word_right_lst = []
    for i in range(len(matrix_lst)):
        for j in range(len(matrix_lst[0])):
            row = matrix_lst[i]
            right_lst.append(row[j].lower())
        right_lst.append(' ')
    column_right_lst = str(concat_list(right_lst)).split()
    return check_directions(column_right_lst, word_right_lst, words)


def l_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the left direction."""
    left_lst = []
    word_left_lst = []
    for i in range(len(matrix_lst)):
        for j in range(len(matrix_lst[0])-1, -1, -1):
            row = matrix_lst[i]
            left_lst.append(row[j].lower())
        left_lst.append(' ')
    column_left_lst = str(concat_list(left_lst)).split()
    return check_directions(column_left_lst, word_left_lst,words)


def w_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the up_right_diagonal direction."""
    w_lst = []
    word_w_lst = []
    for k in range(len(matrix_lst) + len(matrix_lst[0]) - 1):
        w_lst.append(' ')
        for j in range(len(matrix_lst[0])):
            for i in range(len(matrix_lst)):
                if k == i + j:
                    w_lst.append(matrix_lst[i][j].lower())
    w_diagonal_lst = str(concat_list(w_lst)).split()
    return check_directions(w_diagonal_lst, word_w_lst, words)


def x_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the up_left_diagonal direction."""
    x_lst = []
    word_x_lst = []
    for k in range(len(matrix_lst) + len(matrix_lst[0]) - 1):
        x_lst.append(' ')
        for i in range(len(matrix_lst), -1, -1):
            for j in range(len(matrix_lst[0])):
                if k == j - i:
                    x_lst.append(matrix_lst[j][i].lower())
        for i in range(len(matrix_lst), -1, -1):
            for j in range(len(matrix_lst[0])):
                if k == j - i:
                    x_lst.append(matrix_lst[i][j].lower())
    x_diagonal_lst = str(concat_list(x_lst)).split()
    return check_directions(x_diagonal_lst, word_x_lst, words)


def y_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the down_right_diagonal direction."""
    y_lst = []
    word_y_lst = []
    for k in range(len(matrix_lst) + len(matrix_lst[0]) - 1):
        y_lst.append(' ')
        for i in range(len(matrix_lst)):
            for j in range(len(matrix_lst[0])):
                if k == i - j:
                    y_lst.append(matrix_lst[i][j].lower())
    y_diagonal_lst = str(concat_list(y_lst)).split()
    return check_directions(y_diagonal_lst, word_y_lst, words)


def z_direction(matrix_lst, words):
    """ This function receives the matrix list and returns the words that are
    found in the down_left_diagonal direction."""
    z_lst = []
    word_z_lst = []
    for k in range(len(matrix_lst)+len(matrix_lst[0])-1):
        z_lst.append(' ')
        for i in range(len(matrix_lst)):
            for j in range(len(matrix_lst[0])):
                if k == i + j:
                    z_lst.append(matrix_lst[i][j].lower())
    z_diagonal_lst = str(concat_list(z_lst)).split()
    return check_directions(z_diagonal_lst, word_z_lst, words)


def match_direction(direction, matrix, words):
    """ This function receives a direction of searching as a letter or a
    combination of few letters and match this direction to the function
    which searching in the matching direction and returns the founded word
    and how many time they were found as a dictionary when the word is the
    key and the number of times it was found is the value."""
    new_dict = []
    if load_matrix(sys.argv[2]) != [] and load_words(sys.argv[1]) != []:
        if 'u' in direction:
            new_dict.extend(u_direction(matrix, words))
        if 'd' in direction:
            new_dict.extend(l_direction(matrix, words))
        if 'l' in direction:
            new_dict.extend(d_direction(matrix, words))
        if 'r' in direction:
            new_dict.extend(r_direction(matrix, words))
        if 'w' in direction:
            new_dict.extend(w_direction(matrix, words))
        if 'x' in direction:
            new_dict.extend(x_direction(matrix, words))
        if 'y' in direction:
            new_dict.extend(y_direction(matrix, words))
        if 'z' in direction:
            new_dict.extend(z_direction(matrix, words))
    dict_final = {}
    for word in new_dict:
        if word not in dict_final:
            dict_final[word] = 1
        else:
            dict_final[word] += 1
    return dict_final


def load_output(mat_lst, words, file):
    """ This function exports the words which were founded, according to the
    direction which was entered as the last argument,to an external output
    file which its location is the sys.argv[3]."""
    output_dict = match_direction(sys.argv[4], mat_lst, words)
    f_output = open(file, 'w')
    keys = sorted(output_dict.keys())
    for i, key in enumerate(keys):
        if i == len(keys)-1:
            y = str(key) + ',' + str(output_dict[key])
        else:
            y = str(key) + ',' + str(output_dict[key]) + '\n'
        f_output.writelines(y)
    f_output.close()


def main(argv):
    """ This function checks the arguments and only if they are all valid it
    runs the code."""
    if not check_args(argv):
        return
    words = load_words(file=sys.argv[1])
    mat_lst = load_matrix(file=sys.argv[2])
    load_output(mat_lst, words, file=argv[3])


if __name__ == '__main__':
    main(sys.argv)





