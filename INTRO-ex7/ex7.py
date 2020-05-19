##############################################################################
# FILE: ex7.py
# WRITER: Rotem Amsalem , ra260296, 207596297
# EXERCISE: intro2cs ex6 2017-2018
# DESCRIPTION: recursive functions and the hanoi game
##############################################################################

EMPTY_STRING = ""  # magic number


def print_to_n(n):
    """this function print the numbers from 1 to n"""
    if n == 1:  # base case
        print(1)
    elif n > 1:
        print_to_n(n - 1)
        print(n)


def print_reversed(n):
    """this function print the numbers from n to 1"""
    if n == 1:  # base case
        print(1)
    elif n > 1:
        print(n)
        print_reversed(n - 1)


def has_divisor_smaller_than(n, i):
    """this function checks if the number n has smaller divisor than i"""
    if i == 1:  # base case
        return False
    elif i > 1:
        if n % i == 0 and n != i:
            return True
        else:
            if has_divisor_smaller_than(n, i - 1):
                return True
            else:
                return False


def is_prime(n):
    """this function checks if n is a prime number"""
    if n == 1:  # base case
        return False
    elif n > 1:
        if has_divisor_smaller_than(n, n):
            return False
        else:
            return True
    else:
        return False


def divisors_list(n, i, div_lst):
    """this function return all the divisors of n from i till n"""
    if n == i:  # base case
        div_lst.append(n)
    elif n > i:
        if n % i == 0:
            div_lst.append(i)
        divisors_list(n, i + 1, div_lst)
    return div_lst


def divisors(n):
    """this function returns all the divisors of n from 1 till n"""
    if n == 0:
        return []
    else:
        return divisors_list(abs(n), 1, [])


def factorial(n):
    """this function return the factorial of n"""
    if n == 0:  # base case
        return 1
    else:
        return n * factorial(n - 1)


def exp_n_x(n, x):
    """this function returns the exponential sum, using the previous
    functions"""
    if n == 0:  # base case
        return 1
    else:
        return (x ** n / factorial(n)) + exp_n_x(n - 1, x)


def play_hanoi(hanoi, n, src, dest, temp):
    """this function implement the hanoi game. It moves all the discs from
    the source rod to the destination rod using the temporary rod"""
    if n <= 0:
        return
    elif n == 1:
        hanoi.move(src, dest)
    else:
        play_hanoi(hanoi, n - 1, src, temp, dest)
        play_hanoi(hanoi, 1, src, dest, temp)
        play_hanoi(hanoi, n - 1, temp, dest, src)


def print_binary_sequences_with_prefix(prefix, n):
    """this function prints all the possible combinations of 1 and 0 at n
    length that begins with prefix """
    if n == 0:
        return prefix
    else:
        zero_add = print_binary_sequences_with_prefix(prefix + "0", n - 1)
        one_add = print_binary_sequences_with_prefix(prefix + "1", n - 1)
        if zero_add is not None:
            print(zero_add)
        if one_add is not None:
            print(one_add)


def print_binary_sequences(n):
    """this function prints all the possible combinations of 1 and 0 at n
    length"""
    print_binary_sequences_with_prefix(EMPTY_STRING, n)
    if n == 0:
        print("")


def print_sequences_with_prefix(prefix, char_list, n):
    """this function prints all the possible combinations of characters
    from the char_list at n length that begins with prefix"""
    if n == 0:
        return prefix
    else:
        for i in range(len(char_list)):
            char_list_add = print_sequences_with_prefix(prefix + char_list[
                i], char_list, n - 1)
            if char_list_add is not None:
                print(char_list_add)


def print_sequences(char_list, n):
    """this function prints all the possible combinations of characters
    from the char_list at n length"""
    if n == 0:
        print(EMPTY_STRING)
    else:
        print_sequences_with_prefix(EMPTY_STRING, char_list, n)


def print_no_repetition_sequences_with_prefix(prefix, char_list, n):
    """this function prints all the possible combinations of characters
    from the char_list at n length that begins with prefix without
    repeating a char more than one time"""
    if n == 0:
        return prefix
    for i in range(len(char_list)):
        if char_list[i] not in prefix:
            char_list_add = print_no_repetition_sequences_with_prefix(
                prefix + char_list[i], char_list, n - 1)
            if char_list_add is not None:
                print(char_list_add)


def print_no_repetition_sequences(char_list, n):
    """this function prints all the possible combinations of characters
    from the char_list at n length without repeating a char more than one
    time"""
    if n == 0:
        print(EMPTY_STRING)
    else:
        print_no_repetition_sequences_with_prefix(EMPTY_STRING, char_list, n)


def no_repetition_sequences_list_with_prefix(prefix, char_list, n, rep_seq):
    """this function returns a list of all the possible combinations of
    characters from the char_list at n length that begins with prefix without
    repeating a char more than one time"""
    if n == 0:
        return prefix
    else:
        for i in range(len(char_list)):
            if char_list[i] not in prefix:
                chars_add = no_repetition_sequences_list_with_prefix(
                    prefix + char_list[i], char_list, n - 1, rep_seq)
                if chars_add is not None:
                    rep_seq.append(chars_add)


def no_repetition_sequences_list(char_list, n):
    """this function returns a list of all the possible combinations of
    characters from the char_list at n length without repeating a char more
    than one time"""
    if n == 0:
        return [EMPTY_STRING]
    else:
        rep_seq = []
        no_repetition_sequences_list_with_prefix(EMPTY_STRING, char_list, n,
                                                 rep_seq)
        return rep_seq
