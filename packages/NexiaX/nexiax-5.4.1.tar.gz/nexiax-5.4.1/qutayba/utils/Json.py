#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Utils module to provide helper for our common json operations.

"""

from __future__ import absolute_import

import json

from .FileOperations import getFileContents, openTextFile


def loadJsonFromFilename(filename):
    try:
        return json.loads(getFileContents(filename))
    except ValueError:
        return None


def writeJsonToFilename(filename, contents, indent=2):
    with openTextFile(filename, "w") as output:
        json.dump(contents, output, indent=indent, sort_keys=True)



