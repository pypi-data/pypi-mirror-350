#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Indentation of code.

Language independent, the amount of the spaces is not configurable, as it needs
to be the same as in templates.
"""


def _indentedCode(codes, prefix):
    return "\n".join(
        prefix + line if (line and line[0] != "#") else line for line in codes
    )


def indented(codes, level=4, vert_block=False):
    if type(codes) is str:
        codes = codes.split("\n")

    if vert_block and codes != [""]:
        codes.insert(0, "")
        codes.append("")

    return _indentedCode(codes, " " * level)


def getCommentCode(comment, emit):
    emit("// " + comment)



