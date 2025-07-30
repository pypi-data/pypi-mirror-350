#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Handling of images, esp. format conversions for icons.

"""

from .FileOperations import getFilenameExtension, hasFilenameExtension
from .Utils import isMacOS, isWin32Windows


def checkIconUsage(logger, icon_path):
    icon_format = getFilenameExtension(icon_path)

    if icon_format == "":
        logger.sysexit(
            """\
Cannot detect the icon format from filename extension of '%s'."""
            % (icon_path)
        )
    elif icon_format != ".icns" and isMacOS():
        needs_conversion = True
    elif icon_format != ".ico" and isWin32Windows():
        needs_conversion = True
    else:
        needs_conversion = False

    if needs_conversion:
        try:
            import imageio  # pylint: disable=I0021,import-error,unused-import
        except ImportError as e:
            from qutayba import Options

            if Options.is_debug:
                logger.info("Exception importing 'imageio' is %s" % repr(e))

            logger.sysexit(
                """\
Need to install 'imageio' to automatically convert the non native \
icon image (%s) in file in '%s'."""
                % (icon_format[1:].upper(), icon_path)
            )


def convertImageToIconFormat(logger, image_filename, converted_icon_filename):
    """Convert image file to icon file."""
    icon_format = converted_icon_filename.rsplit(".", 1)[1].lower()

    # Limit to supported icon formats.
    assert hasFilenameExtension(converted_icon_filename, (".ico", ".icns")), icon_format

    # Avoid importing unless actually used.
    import imageio  # pylint: disable=I0021,import-error

    try:
        image = imageio.imread(image_filename)
    except ValueError:
        logger.sysexit(
            "Unsupported file format for 'imageio' in '%s', use e.g. PNG or other supported file formats instead."
            % image_filename
        )

    imageio.imwrite(converted_icon_filename, image)



