#!/usr/bin/env python3
"""Utilities module"""

import requests
from functools import wraps


def get_json(url):
    """Fetch JSON from a given URL"""
    response = requests.get(url)
    return response.json()


def access_nested_map(nested_map, path):
    """Access a nested map with a tuple path"""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def memoize(method):
    """Memoization decorator"""

    @wraps(method)
    def wrapper(self):
        attr = f"_{method.__name__}"
        if not hasattr(self, attr):
            setattr(self, attr, method(self))
        return getattr(self, attr)

    return wrapper

