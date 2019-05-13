#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from detect_letter import pixel_to_2d_arr

"""
<<Strategy>>

1. Transform image into 2d array
2. Find top left, top right, bottom left, bottom right corners of sentence
    a. Find position (i, j) of 2d array where pixel color falls below certain threshold (denoting start of the text)
    b. Sometimes top left and bottom left positions will have different `j` indexes.
    (i.e. Top left `j` might be less than bottom left `j`)
    In that case, take smaller `j` and apply that to both top left and bottom left.
    Same applies to all corners. The goal is to get a rectangle, not a trapezoid.
3. "Crop" 2d array based on the bounding box indices.

"""

two_d_arr = pixel_to_2d_arr("hello_world.png", 0.5)
print(np.array_str(two_d_arr, max_line_width=1000))
