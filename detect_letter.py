# this file is for converting characters to 2d arrays

from functools import reduce
import string
import cv2
from skimage.transform import rescale
from PIL import Image, ImageFont, ImageDraw
import numpy as np

np.set_printoptions(threshold=np.inf)

"""
<<Strategy>>

1. Create dictionary of letters
    a. Dictionary stores letters in alphabet as keys and 2d array of letter as values
    b. Count "islands" in each letter. Islands are defined by blobs of 0s.
    c. Create another dictionary whose keys are the island counts and values are a list of letters

2. Parse image
    - Convert image to a 2d array

3. Match image to letter
    a.Compare island counts to narrow search
    b. if more than one match, compare island area ratios

"""

# draw letter and convert to 2d array


def char_to_2d_arr(text, path='arial.ttf', fontsize=60):
    # get width, height of font
    font = ImageFont.truetype(path, fontsize)
    w, h = font.getsize(text)
    image = Image.new('L', (w, h), 1)  # 'L' mode creates grayscale img

    # draw text
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)

    # convert drawing to array of 0s and 1s
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)  # convert 0 to 1 (invert)
    arr = arr[(arr != 0).any(axis=1)]  # delete useless rows that are all 0s
    arr = arr[:, np.sum(arr, 0) != 0]  # only include cols with sum !=0
    return arr


def count_islands(arr):
    count = 0
    areas = []

    def sink_islands(row, col, area):
        # if we go off bounds, return
        if row >= len(arr) or row < 0 or col >= len(arr[row]) or col < 0:
            return 0
        # if we hit a non-zero element, return
        if arr[row][col] != 0:
            return 0
        # if we hit zero, sink the island and check up, down, right, left
        if arr[row][col] == 0:
            arr[row][col] = 1
            area += 1
            area += sink_islands(row - 1, col, 0)
            area += sink_islands(row + 1, col, 0)
            area += sink_islands(row, col - 1, 0)
            area += sink_islands(row, col + 1, 0)
        return area

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 0:
                count += 1
                areas.append(sink_islands(i, j, 0))
    return (count, areas)

# read image and convert to 2d array


def pixel_to_2d_arr(path, scale):
    image = cv2.imread(path)  # test.png is capital letter 'A'

    # convert to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # downscale image
    grayscale = rescale(grayscale, scale)

    # formatting array
    for i in range(len(grayscale)):
      grayscale[i] = list(map(lambda x: int(round(x)), grayscale[i]))

    # convert pixel data to 2d array of 0s and 1s
    ret, threshold1 = cv2.threshold(grayscale, 0, 1, cv2.THRESH_BINARY)

    # process 2d array
    threshold1 = np.where(threshold1, 0, 1)  # convert 0 to 1 (invert)

    threshold1 = threshold1[(threshold1 != 0).any(
        axis=1)]  # delete useless rows
    # delete useless cols
    # threshold1 = threshold1[:, np.sum(threshold1, 0) != 0]

    return threshold1


# print("This is the numpy array representation of letter A")
# print(pixel_to_2d_arr("testA.png"))

# returns the island count and the island area ratio of the input image
def get_target(image_arr):
    target_count, target_areas = count_islands(image_arr)
    return (target_count, target_areas)


def get_area_ratios(candidate, target):
    return list(map(lambda x, y: x / y, candidate, target))


def main(img_arr):
    # generate dictionary of letters
    # keys are letters and values are another dictionary containing 2d array and island count
    dictionary = dict()
    for c in string.ascii_uppercase:
        count, areas = count_islands(char_to_2d_arr(c))
        dictionary[c] = {
            'array': char_to_2d_arr(c),
            'islandCount': count,
            'islandAreas': areas
        }

    # print(dictionary)
    # print(dictionary['S']['array'])

    # generate another dictionary; this time, keys are island count
    # this is to facilitate letter matching later on
    by_island_count = dict()
    for letter in dictionary:
        if dictionary[letter]['islandCount'] in by_island_count:
            by_island_count[dictionary[letter]['islandCount']].append(letter)
        else:
            by_island_count[dictionary[letter]['islandCount']] = [letter]

    # print('by_island_count', by_island_count)

    target_count, target_areas = get_target(img_arr)
    candidate_letters = by_island_count[target_count]

    # if there is only one candidate, return that
    if len(candidate_letters) == 1:
        print(candidate_letters[0])
        return candidate_letters[0]

    # otherwise, get the ratio of areas and pick the one with the smallest standard deviation
    else:
        candidate_areas = list(
            map(lambda x: dictionary[x]['islandAreas'], candidate_letters))

        print('candidate letters', candidate_letters)

        # create array of dictionaries that contain candidate letter and standard deviation of area ratios
        candidate_arr = []
        for i in range(len(candidate_letters)):
            candidate_arr.append({'letter': candidate_letters[i], 'std': float(
                np.std(get_area_ratios(candidate_areas[i], target_areas)))})

        def get_min_std(x, y):
            return x if x['std'] < y['std'] else y

        best_guess = reduce(get_min_std, candidate_arr)['letter']
        print('best guess', best_guess)
        return best_guess
