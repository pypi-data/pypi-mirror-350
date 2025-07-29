#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from pathlib import Path
from typing import Optional, TypeVar, Union, Tuple

from numpy import ndarray

path = Union[str, Path]
collection = Union[list, set, Tuple, ndarray]

str_list = Optional[Union[str, list]]

T = TypeVar('T')
