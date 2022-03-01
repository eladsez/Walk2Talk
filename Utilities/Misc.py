import os
import sys

"""
This class is for some static helper methods we used across the project
"""


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.abspath("./")
    return os.path.join(base_path, relative_path)


def paint_txt(style, txt_color, back_ground, text: str):
    """
    This method colors a string
    """
    return f'\033[{style};{txt_color};{back_ground}m {text}\n'
