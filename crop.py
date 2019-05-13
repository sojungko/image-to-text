#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
import cv2
import numpy as np
import detect_letter

pixel_to_2d_arr = detect_letter.pixel_to_2d_arr
np.set_printoptions(threshold=np.inf)

def not_all_zeroes(arr):
    """
    returns whether not all elements in array are 0
    """
    return not all(element == 0 for element in arr)

def get_letters(two_d_arr):
    """
    returns array like [ {start: 0, length: 2}, { start: 3, length: 2 } ]
    """
    # initialize array of letter lengths
    letters = []
    transposed = two_d_arr.T

    def recursively_get_letter(arr, letter, index, length):
      # return if at end of array
        if index == len(arr):
            if 'start' in letter:
                letters.append(letter)
            return
        # if column all zeroes
        if not not_all_zeroes(arr[index]):
            # check if a letter has been detected and append
            if 'start' in letter:
                letters.append(letter)
            # move onto next column, set length back to 0
            recursively_get_letter(arr, dict(), index + 1, 0)
        if not_all_zeroes(arr[index]):
            if 'start' in letter:
                letter['length'] += 1
            else:
                letter['start'] = index
                letter['length'] = 1
            recursively_get_letter(arr, letter, index + 1, length)

    recursively_get_letter(transposed, dict(), 0, 0)
    return letters


# img_arr = pixel_to_2d_arr("hi_sam.png", (0.1, 0.8))
# letters_data = get_letters(img_arr)
# print(letters_data)

def get_spaces(two_d_arr):
    """
    returns array like [ {start: 0, length: 2}, { start: 3, length: 2 } ]
    """
    # initialize array of space lengths
    spaces = []
    transposed = two_d_arr.T

    def recursively_get_space(arr, space, index, length):
      # return if at end of array
        if index == len(arr):
            if 'start' in space:
                spaces.append(space)
            return
        # if column all zeroes
        if not_all_zeroes(arr[index]):
            # check if a space has been detected and append
            if 'start' in space:
                spaces.append(space)
            # move onto next column, set length back to 0
            recursively_get_space(arr, dict(), index + 1, 0)
        if not not_all_zeroes(arr[index]):
            if 'start' in space:
                space['length'] += 1
            else:
                space['start'] = index
                space['length'] = 1
            recursively_get_space(arr, space, index + 1, length)

    recursively_get_space(transposed, dict(), 0, 0)
    return spaces

# spaces_data = get_spaces(img_arr)
# mean_space = np.mean(list(map(lambda x: x['length'], spaces_data)))
# spaces_btwn_words = list(filter(lambda x: x['length'] > mean_space, spaces_data))

def trimmed_spaces(spaces, letters):
    """
    if first or last spaces need to be trimmed, trim them
    """
    if spaces[0]['start'] < letters[0]['start']:
        spaces = spaces[1:]
    if spaces[-1]['start'] > letters[-1]['start']:
        spaces = spaces[0:-1]
    return spaces

# trimmed_spaces_btwn_words = trimmed_spaces(spaces_btwn_words, letters_data)
# print('trimmed spaces', trimmed_spaces_btwn_words)

def get_letter_breaks(letters, spaces):
    """
    return indices of letters array where a word ends
    """
    breaks = []
    for i in range(len(letters)):
        for space in spaces:
            if letters[i]['start'] + letters[i]['length'] == space['start']:
                breaks.append(i + 1)
    return breaks

# letter_breaks = get_letter_breaks(letters_data, trimmed_spaces_btwn_words)
# print('letter breaks', letter_breaks)

def get_letters_2d_array(two_d_arr, letters):
    """
    takes 2d array of image
    returns array of 2d arrays of letters
    """
    result = list()
    transposed = two_d_arr.T
    for letter in letters:
        result.append(transposed[letter['start']:letter['start'] + letter['length']].T)
    return result

# letters_2d_arr = get_letters_2d_array(img_arr, letters_data)
# # print(letters_2d_arr)

# parsed_letters = []
# for i in range(len(letters_2d_arr)):
#     parsed_letters.append(detect_letter.main(letters_2d_arr[i]))

# print('parsed', parsed_letters)

def main(img_arr):
    letters_data = get_letters(img_arr)
    spaces_data = get_spaces(img_arr)
    mean_space = np.mean(list(map(lambda x: x['length'], spaces_data)))
    spaces_btwn_words = list(filter(lambda x: x['length'] > mean_space, spaces_data))
    trimmed_spaces_btwn_words = trimmed_spaces(spaces_btwn_words, letters_data)
    letter_breaks = get_letter_breaks(letters_data, trimmed_spaces_btwn_words)
    letters_2d_arr = get_letters_2d_array(img_arr, letters_data)


    parsed_letters = []
    for i in range(len(letters_2d_arr)):
        parsed_letters.append(detect_letter.main(letters_2d_arr[i]))

    print('parsed', parsed_letters)

    # if single word, join parsed letters and return
    if len(trimmed_spaces_btwn_words) == 0:
        print(''.join(parsed_letters))
        return ''.join(parsed_letters)
    else:
        words = []
        start = 0
        for i in range(len(letter_breaks)):
            # if at end of letter_breaks array
            if i == len(letter_breaks) - 1:
                words.append(''.join(parsed_letters[start:letter_breaks[i]]))
                words.append(''.join(parsed_letters[letter_breaks[i]:]))
            else:
                words.append(''.join(parsed_letters[start:letter_breaks[i]]))
                start = letter_breaks[i]
    print('words', ' '.join(words))
    return ' '.join(words)