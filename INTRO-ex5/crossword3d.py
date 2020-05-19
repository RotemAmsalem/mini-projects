#######################################################################
# FILE : ex5.py
# WRITERS : Rotem_Amsalem , ra260296 , 207596297
#           Elia_Hene , eh51195 , 324502145
# EXERCISE : intro2cs ex4 2017-2018
# DESCRIPTION: an implementation of a crossword game.
########################################################################

import sys
import os.path
import crossword
import copy

NUMBER_OF_ARGUMENTS = 4  # There are actually 5 arguments but the user
# entered only the last 4 of them and the first one is the location of the
# python file (crossword).

direction_3d_lst = ['a', 'b', 'c']


def check_args(argv):
    """" This function checks the arguments which were given. It checks
    whether the number of arguments is valid or not only if it does,
    the function starts to check the arguments and printed the matching
    error messages according to the instructions."""
    if len(argv) != NUMBER_OF_ARGUMENTS + 1:
        print('ERROR: invalid number of parameters. Please enter word_file '
              'matrix_file output_file direction.')
        return False
    if not (os.path.isfile(argv[1])):
        print('ERROR: Word file ' + str(argv[1]).split('\\')[-1] +
              ' does not exist.')
        return False
    if not (os.path.isfile(argv[2])):
        print('ERROR: Matrix file ' + str(argv[2]).split('\\')[-1] +
              ' does not exist.')
        return False
    for letter in list(argv[4]):
        if letter not in direction_3d_lst:
            print('ERROR: invalid directions.')
            return False
    return True


def load_3d_words(file):
    """ This function loading the words from an external file and put it into a
    list of words."""
    words_3d = []
    f_words = open(file)
    for line in f_words:
        word = line.strip()
        if word.isalpha:
            words_3d.append(word)
    f_words.close()
    return words_3d


def load_3d_matrix(file):
    """ This function loading the matrix from an external file and put it
    into a list that list contains other lists that contain other lists."""
    mat_3d_lst = []
    f_mat = open(file)
    for line in f_mat:
        seq = line.strip()
        if seq.isalpha:
            mat_3d_lst.append(seq)
    for i in range(len(mat_3d_lst)):
        mat_3d_lst[i] = mat_3d_lst[i].split(',')
    f_mat.close()
    return mat_3d_lst


def depth_matrix(matrix_3d_lst):
    """ This function receives matrix and returns the number of depth
    matrices."""
    index_lst = []
    for i in range(len(matrix_3d_lst)):
        if matrix_3d_lst[i] == ['***']:
            index_lst.append(i)
    return index_lst


def a_direction(matrix_3d_lst):
    """ This function returns all the 2d matrices which receives from the a
    direction (depth matrices)."""
    a_lst = []
    matrix_new =[]
    for i in range(len(matrix_3d_lst)):
        if i not in depth_matrix(matrix_3d_lst):
            matrix_new.append(matrix_3d_lst[i])
            continue
        if i in depth_matrix(matrix_3d_lst):
            a_lst.append(matrix_new)
            matrix_new = []
    a_lst.append(matrix_new)
    return a_lst


def b_direction(matrix_3d_lst):
    """ This function returns all the 2d matrices which receives from the b
    direction (length matrices)."""
    mat_to_cpy = copy.deepcopy(matrix_3d_lst)
    b_lst = []
    L = depth_matrix(matrix_3d_lst)[0]
    D = len(depth_matrix(matrix_3d_lst)) + 1
    p = 0
    for index in depth_matrix(matrix_3d_lst):
        del mat_to_cpy[index - p]
        p += 1
    for k in range(D):
        lst_2 = []
        for j in range(k, len(mat_to_cpy), L):
            lst_2.append(mat_to_cpy[j])
        b_lst.append(lst_2)
    return b_lst


def c_direction(matrix_3d_lst):
    """ This function returns all the 2d matrices which receives from the c
    direction (width matrices)."""
    c_lst = []
    L = depth_matrix(matrix_3d_lst)[0]
    D = len(depth_matrix(matrix_3d_lst)) + 1
    W = len(matrix_3d_lst[0])
    matrics = a_direction(matrix_3d_lst)
    for j in range(W):
        lst_3 = []
        for k in range(D):
            lst_4 = []
            for i in range(L):
                lst_4.append(matrics[k][i][j])
            lst_3.append(lst_4)
        c_lst.append(lst_3)
    return c_lst


def direction_to_matrix(direction, words_3d, matrix_3d_lst):
    """ This function receives a direction of searching as a letter or a
    combination of few letters and match this direction to the function
    which searching in the matching direction and returns the founded word
    and how many time they were found as a dictionary when the word is the
    key and the number of times it was found is the value."""
    new_lst = []
    if load_3d_matrix(sys.argv[2]) != [] and load_3d_words(sys.argv[1]) != []:
        if 'a' in direction:
            new_lst.extend(a_direction(matrix_3d_lst))
        if 'b' in direction:
            new_lst.extend(b_direction(matrix_3d_lst))
        if 'c' in direction:
            new_lst.extend(c_direction(matrix_3d_lst))
    dict_final = {}
    for mat in new_lst:
        dict_final_1 = crossword.match_direction('dulrxwyz', mat,words_3d)
        for words in dict_final_1:
            if words not in dict_final:
                dict_final[words] = dict_final_1[words]
            else:
                dict_final[words] += dict_final_1[words]
    return dict_final


def load_3d_output(matrix_3d_lst, words_3d, file):
    """ This function exports the words which were founded, according to the
    direction which was entered as the last argument,to an external output
    file which its location is the sys.argv[3]."""
    final_dict = direction_to_matrix(sys.argv[4], words_3d, matrix_3d_lst)
    f_output = open(file, 'w')
    keys = sorted(final_dict.keys())
    for i, key in enumerate(keys):
        if i == len(keys)-1:
            y = str(key) + ',' + str(final_dict[key])
        else:
            y = str(key) + ',' + str(final_dict[key]) + '\n'
        f_output.writelines(y)
    f_output.close()


def main(argv):
    """ This function checks the arguments and only if they are all valid it
    runs the code."""
    if not check_args(argv):
        return
    words_3d = load_3d_words(sys.argv[1])
    matrix_3d_lst = load_3d_matrix(sys.argv[2])
    load_3d_output(matrix_3d_lst, words_3d, argv[3])


if __name__ == '__main__':
    main(sys.argv)
