#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" XML node tree handling

Means to create XML elements from nexium tree nodes and to convert the
XML tree to ASCII or output it.
"""

from qutayba.__past__ import BytesIO, StringIO


def _indent(elem, level=0, more_sibs=False):
    i = "\n"
    if level:
        i += (level - 1) * "  "
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            if level:
                elem.text += "  "
        count = 0
        for kid in elem:
            _indent(kid, level + 1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += "  "
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += "  "

    return elem


def _dedent(elem, level=0):
    if not elem.text or not elem.text.strip():
        elem.text = ""

    for child in elem:
        _dedent(child, level + 1)

    if not elem.tail or not elem.tail.strip():
        elem.tail = ""

    return elem


try:
    import xml.etree.ElementTree

    xml_module = xml.etree.ElementTree

    Element = xml.etree.ElementTree.Element

    def xml_tostring(tree, indent=True, encoding=None):
        if indent:
            _indent(tree)
        elif not indent:
            _dedent(tree)

        return xml_module.tostring(tree, encoding=encoding)

except ImportError:
    xml_module = None
    Element = None
    xml_tostring = None

# TODO: Use the writer to create the XML we output. That should be more
# scalable and/or faster.
# try:
#     from lxml import (
#         xmlfile as xml_writer,  # pylint: disable=I0021,import-error,unused-import
#     )
# except ImportError:
#     xml_writer = None


def toBytes(tree, indent=True, encoding=None):
    return xml_tostring(tree, indent=indent, encoding=encoding)


def toString(tree):
    result = toBytes(tree, encoding="utf8")

    if str is not bytes:
        result = result.decode("utf8")

    return result


def fromString(text, use_lxml=False):
    if type(text) is str:
        return fromFile(StringIO(text), use_lxml=use_lxml)
    else:
        return fromFile(BytesIO(text), use_lxml=use_lxml)


def fromFile(file_handle, use_lxml=False):
    if use_lxml:
        from lxml import etree  # pylint: disable=I0021,import-error

        return etree.parse(file_handle).getroot()
    else:
        return xml_module.parse(file_handle).getroot()


def appendTreeElement(parent, *args, **kwargs):
    element = Element(*args, **kwargs)

    parent.append(element)

    return element


def dumpTreeXMLToFile(tree, output_file):
    """Write an XML node tree to a file."""

    value = toBytes(tree).rstrip()
    output_file.write(value)
    output_file.write(b"\n")



