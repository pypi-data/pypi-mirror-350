#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" This is for use in testing, but also for user tools too."""

from qutayba.containers.OrderedDicts import OrderedDict
from qutayba.TreeXML import fromFile
from qutayba.utils.ModuleNames import ModuleName


def parseCompilationReport(filename):
    return fromFile(filename)


def extractModulesUsedByModule(compilation_report, module_name):
    # Note: Avoiding usage of "xpath", to lower requirements to not need lxml.
    for module_node in compilation_report.findall("module"):
        if module_node.attrib["name"] != module_name:
            continue

        result = OrderedDict()

        for module_usage_node in module_node.find("module_usages").findall(
            "module_usage"
        ):
            entry = OrderedDict(module_usage_node.attrib)

            used_module_name = ModuleName(entry["name"])
            del entry["name"]
            entry["line"] = int(entry["line"])
            entry["excluded"] = bool(entry["finding"] == "excluded")

            result[used_module_name] = entry

        return result

    # Not found, no usages, user needs to handle that.
    return None


def _getResolvedCompilationPath(path, prefixes):
    for prefix_name, prefix_path in prefixes:
        path = path.replace(prefix_name, prefix_path)

    return path


def getCompilationOutputBinary(compilation_report, prefixes):
    return _getResolvedCompilationPath(
        path=compilation_report.find("output").attrib["run_filename"], prefixes=prefixes
    )


def getCompilationOutputMode(compilation_report):
    return compilation_report.attrib["mode"]


def getEmbeddedDataFilenames(compilation_report):
    result = []

    for datafile_node in compilation_report.findall("data_file"):
        if "embed-run-time" in datafile_node.attrib["tags"].split(
            ","
        ) or "embed-compile-time" in datafile_node.attrib["tags"].split(","):
            result.append(datafile_node.attrib["name"])

    return result



