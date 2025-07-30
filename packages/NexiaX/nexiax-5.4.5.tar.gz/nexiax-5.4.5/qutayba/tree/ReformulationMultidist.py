#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Multidist re-formulation. """

import os

from qutayba.Options import getMainEntryPointFilenames
from qutayba.utils.ModuleNames import makeMultidistModuleName


def _stripPythonSuffix(filename):
    if filename.lower().endswith(".py"):
        return filename[:-3]
    elif filename.lower().endswith(".pyw"):
        return filename[:-4]
    else:
        return filename


def createMultidistMainSourceCode():
    main_filenames = getMainEntryPointFilenames()

    main_basenames = [
        _stripPythonSuffix(os.path.basename(main_filename))
        for main_filename in main_filenames
    ]

    main_module_names = [
        makeMultidistModuleName(count, main_basename)
        for count, main_basename in enumerate(main_basenames, start=1)
    ]

    from qutayba.utils.Jinja2 import renderTemplateFromString

    source_code = renderTemplateFromString(
        r"""
import sys, re, os
main_basename = re.sub(r'(.pyw?|\.exe|\.bin)?$', '', os.path.normcase(os.path.basename(__compiled__.original_argv0)))
{% for main_module_name, main_basename in zip(main_module_names, main_basenames) %}
if main_basename == "{{main_basename}}":
    __import__("{{main_module_name.asString()}}")
    sys.exit(0)
{% endfor %}

sys.exit("Error, failed to detect what to do for filename derived name '%s'." % main_basename)
""",
        main_module_names=main_module_names,
        main_basenames=main_basenames,
        zip=zip,
    )

    return source_code


def locateMultidistModule(module_name):
    multidist_index = int(str(module_name).split("-")[1])

    return (
        module_name,
        getMainEntryPointFilenames()[multidist_index - 1],
        "py",
        "absolute",
    )



