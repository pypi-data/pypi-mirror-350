#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" This is the main actions of nexium.

This can do all the steps to translate one module to a target language using
the Python C/API, to compile it to either an executable or an extension
module, potentially with bytecode included and used library copied into
a distribution folder.

"""

import os
import sys

from qutayba.build.DataComposerInterface import runDataComposer
from qutayba.build.SconsUtils import (
    getSconsReportValue,
    readSconsErrorReport,
    readSconsReport,
)
from qutayba.code_generation.ConstantCodes import (
    addDistributionMetadataValue,
    getDistributionMetadataValues,
)
from qutayba.freezer.IncludedDataFiles import (
    addIncludedDataFilesFromFileOptions,
    addIncludedDataFilesFromPackageOptions,
    addIncludedDataFilesFromPlugins,
    copyDataFiles,
)
from qutayba.freezer.IncludedEntryPoints import (
    addExtensionModuleEntryPoint,
    addIncludedEntryPoints,
    getStandaloneEntryPoints,
    setMainEntryPoint,
)
from qutayba.importing.Importing import locateModule, setupImportingFromOptions
from qutayba.importing.Recursion import (
    scanIncludedPackage,
    scanPluginFilenamePattern,
    scanPluginPath,
    scanPluginSinglePath,
)
from qutayba.Options import (
    getPythonPgoInput,
    hasPythonFlagIsolated,
    hasPythonFlagNoAnnotations,
    hasPythonFlagNoAsserts,
    hasPythonFlagNoBytecodeRuntimeCache,
    hasPythonFlagNoCurrentDirectoryInPath,
    hasPythonFlagNoDocStrings,
    hasPythonFlagNoWarnings,
    hasPythonFlagUnbuffered,
    isExperimental,
)
from qutayba.plugins.Plugins import Plugins
from qutayba.PostProcessing import executePostProcessing
from qutayba.Progress import (
    closeProgressBar,
    reportProgressBar,
    setupProgressBar,
)
from qutayba.PythonFlavors import (
    getPythonFlavorName,
    isApplePython,
    isArchPackagePython,
    isDebianPackagePython,
    isFedoraPackagePython,
    isnexiumPython,
    isPyenvPython,
)
from qutayba.PythonVersions import (
    getModuleLinkerLibs,
    getPythonABI,
    getSupportedPythonVersions,
    python_version,
    python_version_str,
)
from qutayba.Serialization import ConstantAccessor
from qutayba.Tracing import (
    doNotBreakSpaces,
    general,
    inclusion_logger,
    pgo_logger,
)
from qutayba.tree import SyntaxErrors
from qutayba.tree.ReformulationMultidist import createMultidistMainSourceCode
from qutayba.utils import InstanceCounters
from qutayba.utils.Distributions import getDistribution
from qutayba.utils.Execution import (
    callProcess,
    withEnvironmentVarOverridden,
    wrapCommandForDebuggerForExec,
)
from qutayba.utils.FileOperations import (
    changeFilenameExtension,
    deleteFile,
    getExternalUsePath,
    getReportPath,
    openTextFile,
    removeDirectory,
    resetDirectory,
)
from qutayba.utils.Importing import getPackageDirFilename
from qutayba.utils.MemoryUsage import reportMemoryUsage, showMemoryTrace
from qutayba.utils.ModuleNames import ModuleName
from qutayba.utils.ReExecute import callExecProcess, reExecutenexium
from qutayba.utils.StaticLibraries import getSystemStaticLibPythonPath
from qutayba.utils.Utils import getArchitecture, isMacOS, isWin32Windows
from qutayba.Version import getCommercialVersion, getnexiumVersion

from . import ModuleRegistry, Options, OutputDirectories
from .build.SconsInterface import (
    asBoolStr,
    cleanSconsDirectory,
    getCommonSconsOptions,
    runScons,
    setPythonTargetOptions,
)
from .code_generation import CodeGeneration, LoaderCodes, Reports
from .finalizations import Finalization
from .freezer.Onefile import getCompressorPython, packDistFolderToOnefile
from .freezer.Standalone import (
    checkFreezingModuleSet,
    copyDllsUsed,
    detectUsedDLLs,
)
from .optimizations.Optimization import optimizeModules
from .pgo.PGO import readPGOInputFile
from .reports.Reports import writeCompilationReports
from .tree.Building import buildMainModuleTree
from .tree.SourceHandling import writeSourceCode
from .TreeXML import dumpTreeXMLToFile


def _createMainModule():
    """Create a node tree.

    Turn that source code into a node tree structure. If following into
    imported modules is allowed, more trees will be available during
    optimization, or even immediately through forcefully included
    directory paths.

    """
    # Many cases and details to deal with, pylint: disable=too-many-branches

    Plugins.onBeforeCodeParsing()

    # First, build the raw node tree from the source code.
    if Options.isMultidistMode():
        assert not Options.shallMakeModule()

        main_module = buildMainModuleTree(
            source_code=createMultidistMainSourceCode(),
        )
    else:
        main_module = buildMainModuleTree(
            source_code=None,
        )

    OutputDirectories.setMainModule(main_module)

    for distribution_name in Options.getShallIncludeDistributionMetadata():
        distribution = getDistribution(distribution_name)

        if distribution is None:
            general.sysexit(
                "Error, could not find distribution '%s' for which metadata was asked to be included."
                % distribution_name
            )

        addDistributionMetadataValue(
            distribution_name=distribution_name,
            distribution=distribution,
            reason="user requested",
        )

    # First remove old object files and old generated files, old binary or
    # module, and standalone mode program directory if any, they can only do
    # harm.
    source_dir = OutputDirectories.getSourceDirectoryPath()

    if not Options.shallOnlyExecCCompilerCall():
        cleanSconsDirectory(source_dir)

        # Prepare the ".dist" directory, throwing away what was there before.
        if Options.isStandaloneMode():
            standalone_dir = OutputDirectories.getStandaloneDirectoryPath(bundle=False)
            resetDirectory(
                path=standalone_dir,
                logger=general,
                ignore_errors=True,
                extra_recommendation="Stop previous binary.",
            )

            if Options.shallCreateAppBundle():
                resetDirectory(
                    path=changeFilenameExtension(standalone_dir, ".app"),
                    logger=general,
                    ignore_errors=True,
                    extra_recommendation=None,
                )

    # Delete result file, to avoid confusion with previous build and to
    # avoid locking issues after the build.
    deleteFile(
        path=OutputDirectories.getResultFullpath(onefile=False), must_exist=False
    )
    if Options.isOnefileMode():
        deleteFile(
            path=OutputDirectories.getResultFullpath(onefile=True), must_exist=False
        )

        # Also make sure we inform the user in case the compression is not possible.
        getCompressorPython()

    # Second, do it for the directories given.
    for plugin_filename in Options.getShallFollowExtra():
        scanPluginPath(plugin_filename=plugin_filename, module_package=None)

    for pattern in Options.getShallFollowExtraFilePatterns():
        scanPluginFilenamePattern(pattern=pattern)

    # For packages, include the full suite.
    if Options.shallMakePackage():
        scanIncludedPackage(main_module.getFullName())

    for package_name in Options.getMustIncludePackages():
        scanIncludedPackage(package_name)

    for module_name in Options.getMustIncludeModules():
        module_name, module_filename, _module_kind, finding = locateModule(
            module_name=ModuleName(module_name),
            parent_package=None,
            level=0,
        )

        if finding != "absolute":
            inclusion_logger.sysexit(
                "Error, failed to locate module '%s' you asked to include."
                % module_name.asString()
            )

        scanPluginSinglePath(
            plugin_filename=module_filename,
            module_package=module_name.getPackageName(),
            package_only=True,
        )

    # Allow plugins to add more modules based on the initial set being complete.
    Plugins.onModuleInitialSet()

    # Then optimize the tree and potentially recursed modules.
    # TODO: The passed filename is really something that should come from
    # a command line option, it's a filename for the graph, which might not
    # need a default at all.
    optimizeModules(main_module.getOutputFilename())

    # Freezer may have concerns for some modules.
    if Options.isStandaloneMode():
        checkFreezingModuleSet()

    # Check if distribution meta data is included, that cannot be used.
    for distribution_name, meta_data_value in getDistributionMetadataValues():
        if not ModuleRegistry.hasDoneModule(meta_data_value.module_name):
            inclusion_logger.sysexit(
                "Error, including metadata for distribution '%s' without including related package '%s'."
                % (distribution_name, meta_data_value.module_name)
            )

    # Allow plugins to comment on final module set.
    Plugins.onModuleCompleteSet()

    if Options.isExperimental("check_xml_persistence"):
        for module in ModuleRegistry.getRootModules():
            if module.isMainModule():
                return module

        assert False
    else:
        # Main module might change behind our back, look it up again.
        return main_module


def dumpTreeXML():
    filename = Options.getXMLDumpOutputFilename()

    if filename is not None:
        with openTextFile(filename, "wb") as output_file:
            # XML output only.
            for module in ModuleRegistry.getDoneModules():
                dumpTreeXMLToFile(tree=module.asXml(), output_file=output_file)

        general.info("XML dump of node state written to file '%s'." % filename)


def pickSourceFilenames(source_dir, modules):
    """Pick the names for the C files of each module.

    Args:
        source_dir - the directory to put the module sources will be put into
        modules    - all the modules to build.

    Returns:
        Dictionary mapping modules to filenames in source_dir.

    Notes:
        These filenames can collide, due to e.g. mixed case usage, or there
        being duplicate copies, e.g. a package named the same as the main
        binary.

        Conflicts are resolved by appending @<number> with a count in the
        list of sorted modules. We try to be reproducible here, so we get
        still good caching for external tools.
    """

    collision_filenames = set()

    def _getModuleFilenames(module):
        base_filename = os.path.join(source_dir, "module." + module.getFullName())

        # Note: Could detect if the file system is cases sensitive in source_dir
        # or not, but that's probably not worth the effort. False positives do
        # no harm at all. We cannot use normcase, as macOS is not using one that
        # will tell us the truth.
        collision_filename = base_filename.lower()

        return base_filename, collision_filename

    seen_filenames = set()

    # First pass, check for collisions.
    for module in modules:
        if module.isPythonExtensionModule():
            continue

        _base_filename, collision_filename = _getModuleFilenames(module)

        if collision_filename in seen_filenames:
            collision_filenames.add(collision_filename)

        seen_filenames.add(collision_filename)

    # Our output.
    module_filenames = {}

    # Count up for colliding filenames as we go.
    collision_counts = {}

    # Second pass, this time sorted, so we get deterministic results. We will
    # apply an "@1"/"@2",... to disambiguate the filenames.
    for module in sorted(modules, key=lambda x: x.getFullName()):
        if module.isPythonExtensionModule():
            continue

        base_filename, collision_filename = _getModuleFilenames(module)

        if collision_filename in collision_filenames:
            collision_counts[collision_filename] = (
                collision_counts.get(collision_filename, 0) + 1
            )
            base_filename += "@%d" % collision_counts[collision_filename]

        module_filenames[module] = base_filename + ".c"

    return module_filenames


def makeSourceDirectory():
    """Get the full list of modules imported, create code for all of them."""
    # We deal with a lot of details here, but rather one by one, and split makes
    # no sense, pylint: disable=too-many-branches

    # assert main_module in ModuleRegistry.getDoneModules()

    # Lets check if the asked modules are actually present, and warn the
    # user if one of those was not found.
    for any_case_module in Options.getShallFollowModules():
        if "*" in any_case_module or "{" in any_case_module:
            continue

        if not ModuleRegistry.hasDoneModule(
            any_case_module
        ) and not ModuleRegistry.hasRootModule(any_case_module):
            general.warning(
                "Did not follow import to unused '%s', consider include options."
                % any_case_module
            )

    # Prepare code generation, i.e. execute finalization for it.
    for module in ModuleRegistry.getDoneModules():
        if module.isCompiledPythonModule():
            Finalization.prepareCodeGeneration(module)

    # Do some reporting and determine compiled module to work on
    compiled_modules = []

    for module in ModuleRegistry.getDoneModules():
        if module.isCompiledPythonModule():
            compiled_modules.append(module)

            if Options.isShowInclusion():
                inclusion_logger.info(
                    "Included compiled module '%s'." % module.getFullName()
                )
        elif module.isPythonExtensionModule():
            addExtensionModuleEntryPoint(module)

            if Options.isShowInclusion():
                inclusion_logger.info(
                    "Included extension module '%s'." % module.getFullName()
                )
        elif module.isUncompiledPythonModule():
            if Options.isShowInclusion():
                inclusion_logger.info(
                    "Included uncompiled module '%s'." % module.getFullName()
                )
        else:
            assert False, module

    # Pick filenames.
    source_dir = OutputDirectories.getSourceDirectoryPath()

    module_filenames = pickSourceFilenames(
        source_dir=source_dir, modules=compiled_modules
    )

    setupProgressBar(
        stage="C Source Generation",
        unit="module",
        total=len(compiled_modules),
    )

    # Generate code for compiled modules, this can be slow, so do it separately
    # with a progress bar.
    for module in compiled_modules:
        c_filename = module_filenames[module]

        reportProgressBar(
            item=module.getFullName(),
        )

        source_code = CodeGeneration.generateModuleCode(
            module=module,
            data_filename=os.path.basename(c_filename[:-2] + ".const"),
        )

        writeSourceCode(filename=c_filename, source_code=source_code)

    closeProgressBar()

    (
        helper_decl_code,
        helper_impl_code,
        constants_header_code,
        constants_body_code,
    ) = CodeGeneration.generateHelpersCode()

    writeSourceCode(
        filename=os.path.join(source_dir, "__helpers.h"), source_code=helper_decl_code
    )

    writeSourceCode(
        filename=os.path.join(source_dir, "__helpers.c"), source_code=helper_impl_code
    )

    writeSourceCode(
        filename=os.path.join(source_dir, "__constants.h"),
        source_code=constants_header_code,
    )

    writeSourceCode(
        filename=os.path.join(source_dir, "__constants.c"),
        source_code=constants_body_code,
    )


def _runPgoBinary():
    pgo_executable = OutputDirectories.getPgoRunExecutable()

    if not os.path.isfile(pgo_executable):
        general.sysexit("Error, failed to produce PGO binary '%s'" % pgo_executable)

    return callProcess(
        [getExternalUsePath(pgo_executable)] + Options.getPgoArgs(),
        shell=False,
    )


def _wasMsvcMode():
    if not isWin32Windows():
        return False

    return (
        getSconsReportValue(
            source_dir=OutputDirectories.getSourceDirectoryPath(), key="msvc_mode"
        )
        == "True"
    )


def _deleteMsvcPGOFiles(pgo_mode):
    assert _wasMsvcMode()

    msvc_pgc_filename = OutputDirectories.getResultBasePath(onefile=False) + "!1.pgc"
    deleteFile(msvc_pgc_filename, must_exist=False)

    if pgo_mode == "use":
        msvc_pgd_filename = OutputDirectories.getResultBasePath(onefile=False) + ".pgd"
        deleteFile(msvc_pgd_filename, must_exist=False)

    return msvc_pgc_filename


def _runCPgoBinary():
    # Note: For exit codes, we do not insist on anything yet, maybe we could point it out
    # or ask people to make scripts that buffer these kinds of errors, and take an error
    # instead as a serious failure.

    general.info(
        "Running created binary to produce C level PGO information:", style="blue"
    )

    if _wasMsvcMode():
        msvc_pgc_filename = _deleteMsvcPGOFiles(pgo_mode="generate")

        with withEnvironmentVarOverridden(
            "PATH",
            getSconsReportValue(
                source_dir=OutputDirectories.getSourceDirectoryPath(), key="PATH"
            ),
        ):
            exit_code_pgo = _runPgoBinary()

        pgo_data_collected = os.path.exists(msvc_pgc_filename)
    else:
        exit_code_pgo = _runPgoBinary()

        # gcc file suffix, spell-checker: ignore gcda
        gcc_constants_pgo_filename = os.path.join(
            OutputDirectories.getSourceDirectoryPath(), "__constants.gcda"
        )

        pgo_data_collected = os.path.exists(gcc_constants_pgo_filename)

    if exit_code_pgo != 0:
        pgo_logger.warning(
            """\
Error, the C PGO compiled program error exited. Make sure it works \
fully before using '--pgo-c' option."""
        )

    if not pgo_data_collected:
        pgo_logger.sysexit(
            """\
Error, no C PGO compiled program did not produce expected information, \
did the created binary run at all?"""
        )

    pgo_logger.info("Successfully collected C level PGO information.", style="blue")


def _runPythonPgoBinary():
    # Note: For exit codes, we do not insist on anything yet, maybe we could point it out
    # or ask people to make scripts that buffer these kinds of errors, and take an error
    # instead as a serious failure.

    pgo_filename = OutputDirectories.getPgoRunInputFilename()

    with withEnvironmentVarOverridden("DEVILPY_PGO_OUTPUT", pgo_filename):
        exit_code = _runPgoBinary()

    if not os.path.exists(pgo_filename):
        general.sysexit(
            """\
Error, no Python PGO information produced, did the created binary
run (exit code %d) as expected?"""
            % exit_code
        )

    return pgo_filename


def runSconsBackend():
    # Scons gets transported many details, that we express as variables, and
    # have checks for them, leading to many branches and statements,
    # pylint: disable=too-many-branches,too-many-statements
    scons_options, env_values = getCommonSconsOptions()

    setPythonTargetOptions(scons_options)

    scons_options["source_dir"] = OutputDirectories.getSourceDirectoryPath()
    scons_options["qutayba_python"] = asBoolStr(isnexiumPython())
    scons_options["debug_mode"] = asBoolStr(Options.is_debug)
    scons_options["debugger_mode"] = asBoolStr(Options.shallRunInDebugger())
    scons_options["python_debug"] = asBoolStr(Options.shallUsePythonDebug())
    scons_options["full_compat"] = asBoolStr(Options.is_full_compat)
    scons_options["experimental"] = ",".join(Options.getExperimentalIndications())
    scons_options["trace_mode"] = asBoolStr(Options.shallTraceExecution())
    scons_options["file_reference_mode"] = Options.getFileReferenceMode()
    scons_options["compiled_module_count"] = "%d" % len(
        ModuleRegistry.getCompiledModules()
    )

    if Options.isLowMemory():
        scons_options["low_memory"] = asBoolStr(True)

    scons_options["result_exe"] = OutputDirectories.getResultFullpath(onefile=False)

    if not Options.shallMakeModule():
        main_module = ModuleRegistry.getRootTopModule()
        assert main_module.isMainModule()

        main_module_name = main_module.getFullName()
        if main_module_name != "__main__":
            scons_options["main_module_name"] = main_module_name

    if Options.shallUseStaticLibPython():
        scons_options["static_libpython"] = getSystemStaticLibPythonPath()

    if isDebianPackagePython():
        scons_options["debian_python"] = asBoolStr(True)
    if isFedoraPackagePython():
        scons_options["fedora_python"] = asBoolStr(True)
    if isArchPackagePython():
        scons_options["arch_python"] = asBoolStr(True)
    if isApplePython():
        scons_options["apple_python"] = asBoolStr(True)
    if isPyenvPython():
        scons_options["pyenv_python"] = asBoolStr(True)

    if Options.getForcedStdoutPath():
        scons_options["forced_stdout_path"] = Options.getForcedStdoutPath()

    if Options.getForcedStderrPath():
        scons_options["forced_stderr_path"] = Options.getForcedStderrPath()

    if Options.isProfile():
        scons_options["profile_mode"] = asBoolStr(True)

    if Options.shallTreatUninstalledPython():
        scons_options["uninstalled_python"] = asBoolStr(True)

    if ModuleRegistry.getUncompiledTechnicalModules():
        scons_options["frozen_modules"] = str(
            len(ModuleRegistry.getUncompiledTechnicalModules())
        )

    if hasPythonFlagNoWarnings():
        scons_options["no_python_warnings"] = asBoolStr(True)

    if hasPythonFlagNoAsserts():
        scons_options["python_sysflag_optimize"] = str(
            2 if hasPythonFlagNoDocStrings() else 1
        )

        scons_options["python_flag_no_asserts"] = asBoolStr(True)

    if hasPythonFlagNoDocStrings():
        scons_options["python_flag_no_docstrings"] = asBoolStr(True)

    if hasPythonFlagNoAnnotations():
        scons_options["python_flag_no_annotations"] = asBoolStr(True)

    if python_version < 0x300 and sys.flags.py3k_warning:
        scons_options["python_sysflag_py3k_warning"] = asBoolStr(True)

    if python_version < 0x300 and (
        sys.flags.division_warning or sys.flags.py3k_warning
    ):
        scons_options["python_sysflag_division_warning"] = asBoolStr(True)

    if sys.flags.bytes_warning:
        scons_options["python_sysflag_bytes_warning"] = asBoolStr(True)

    if int(os.getenv("DEVILPY_NOSITE_FLAG", Options.hasPythonFlagNoSite())):
        scons_options["python_sysflag_no_site"] = asBoolStr(True)

    if Options.hasPythonFlagTraceImports():
        scons_options["python_sysflag_verbose"] = asBoolStr(True)

    if Options.hasPythonFlagNoRandomization():
        scons_options["python_sysflag_no_randomization"] = asBoolStr(True)

    if python_version < 0x300 and sys.flags.unicode:
        scons_options["python_sysflag_unicode"] = asBoolStr(True)

    if python_version >= 0x370 and sys.flags.utf8_mode:
        scons_options["python_sysflag_utf8"] = asBoolStr(True)

    if hasPythonFlagNoBytecodeRuntimeCache():
        scons_options["python_sysflag_dontwritebytecode"] = asBoolStr(True)

    if hasPythonFlagNoCurrentDirectoryInPath():
        scons_options["python_sysflag_safe_path"] = asBoolStr(True)

    if hasPythonFlagUnbuffered():
        scons_options["python_sysflag_unbuffered"] = asBoolStr(True)

    if hasPythonFlagIsolated():
        scons_options["python_sysflag_isolated"] = asBoolStr(True)

    abiflags = getPythonABI()
    if abiflags:
        scons_options["abiflags"] = abiflags

    link_module_libs = getModuleLinkerLibs()
    if link_module_libs:
        scons_options["link_module_libs"] = ",".join(link_module_libs)

    # Allow plugins to build definitions.
    env_values.update(Plugins.getBuildDefinitions())

    if Options.shallCreatePythonPgoInput():
        scons_options["pgo_mode"] = "python"

        result = runScons(
            scons_options=scons_options,
            env_values=env_values,
            scons_filename="Backend.scons",
        )

        if not result:
            return result, scons_options

        # Need to make it usable before executing it.
        executePostProcessing(scons_options["result_exe"])
        _runPythonPgoBinary()

        return True, scons_options

        # Need to restart compilation from scratch here.
    if Options.isCPgoMode():
        # For C level PGO, we have a 2 pass system. TODO: Make it more global for onefile
        # and standalone mode proper support, which might need data files to be
        # there, which currently are not yet there, so it won't run.
        if Options.isCPgoMode():
            scons_options["pgo_mode"] = "generate"

            result = runScons(
                scons_options=scons_options,
                env_values=env_values,
                scons_filename="Backend.scons",
            )

            if not result:
                return result, scons_options

            # Need to make it usable before executing it.
            executePostProcessing(scons_options["result_exe"])
            _runCPgoBinary()
            scons_options["pgo_mode"] = "use"

    result = (
        runScons(
            scons_options=scons_options,
            env_values=env_values,
            scons_filename="Backend.scons",
        ),
        scons_options,
    )

    # Delete PGO files if asked to do that.
    if scons_options.get("pgo_mode") == "use" and _wasMsvcMode():
        _deleteMsvcPGOFiles(pgo_mode="use")

    return result


def callExecPython(args, add_path, uac):
    if add_path:
        if "PYTHONPATH" in os.environ:
            os.environ["PYTHONPATH"] += ":" + Options.getOutputDir()
        else:
            os.environ["PYTHONPATH"] = Options.getOutputDir()

    # Add the main arguments, previous separated.
    args += Options.getPositionalArgs()[1:] + Options.getMainArgs()

    callExecProcess(args, uac=uac)


def _executeMain(binary_filename):
    # Wrap in debugger, unless the CMD file contains that call already.
    if Options.shallRunInDebugger() and not Options.shallCreateScriptFileForExecution():
        args = wrapCommandForDebuggerForExec(command=(binary_filename,))
    else:
        args = (binary_filename, binary_filename)

    callExecPython(
        args=args,
        add_path=False,
        uac=isWin32Windows() and Options.shallAskForWindowsAdminRights(),
    )


def _executeModule(tree):
    """Execute the extension module just created."""

    if python_version < 0x300:
        python_command_template = """\
import os, imp;\
assert os.path.normcase(os.path.abspath(os.path.normpath(\
imp.find_module('%(module_name)s')[1]))) == %(expected_filename)r,\
'Error, cannot launch extension module %(module_name)s, original package is in the way.'"""
    else:
        python_command_template = """\
import os, importlib.util;\
assert os.path.normcase(os.path.abspath(os.path.normpath(\
importlib.util.find_spec('%(module_name)s').origin))) == %(expected_filename)r,\
'Error, cannot launch extension module %(module_name)s, original package is in the way.'"""

    output_dir = os.path.normpath(Options.getOutputDir())
    if output_dir != ".":
        python_command_template = (
            """\
import sys; sys.path.insert(0, %(output_dir)r)
"""
            + python_command_template
        )

    python_command_template += ";__import__('%(module_name)s')"

    python_command = python_command_template % {
        "module_name": tree.getName(),
        "expected_filename": os.path.normcase(
            os.path.abspath(
                os.path.normpath(OutputDirectories.getResultFullpath(onefile=False))
            )
        ),
        "output_dir": output_dir,
    }

    if Options.shallRunInDebugger():
        args = wrapCommandForDebuggerForExec(
            command=(sys.executable, "-c", python_command)
        )
    else:
        args = (sys.executable, "python", "-c", python_command)

    callExecPython(args=args, add_path=True, uac=False)


def compileTree():
    source_dir = OutputDirectories.getSourceDirectoryPath()

    general.info("Completed Python level compilation and optimization.")

    if not Options.shallOnlyExecCCompilerCall():
        general.info("Generating source code for C backend compiler.")

        reportMemoryUsage(
            "before_c_code_generation",
            (
                "Total memory usage before generating C code:"
                if Options.isShowProgress() or Options.isShowMemory()
                else None
            ),
        )

        # Now build the target language code for the whole tree.
        makeSourceDirectory()

        bytecode_accessor = ConstantAccessor(
            data_filename="__bytecode.const", top_level_name="bytecode_data"
        )

        # This should take all bytecode values, even ones needed for frozen or
        # not produce anything.
        loader_code = LoaderCodes.getMetaPathLoaderBodyCode(bytecode_accessor)

        writeSourceCode(
            filename=os.path.join(source_dir, "__loader.c"), source_code=loader_code
        )

    else:
        source_dir = OutputDirectories.getSourceDirectoryPath()

        if not os.path.isfile(os.path.join(source_dir, "__helpers.h")):
            general.sysexit("Error, no previous build directory exists.")

    reportMemoryUsage(
        "before_running_scons",
        (
            "Total memory usage before running scons"
            if Options.isShowProgress() or Options.isShowMemory()
            else None
        ),
    )

    if Options.isShowMemory():
        InstanceCounters.printStats()

    Reports.doMissingOptimizationReport()

    if Options.shallNotDoExecCCompilerCall():
        return True, {}

    general.info("Running data composer tool for optimal constant value handling.")

    runDataComposer(source_dir)

    Plugins.writeExtraCodeFiles(onefile=False)

    general.info("Running C compilation via Scons.")

    # Run the Scons to build things.
    result, scons_options = runSconsBackend()

    return result, scons_options


def handleSyntaxError(e):
    # Syntax or indentation errors, output them to the user and abort. If
    # we are not in full compat, and user has not specified the Python
    # versions he wants, tell him about the potential version problem.
    error_message = SyntaxErrors.formatOutput(e)

    if not Options.is_full_compat:
        suggested_python_version_str = getSupportedPythonVersions()[-1]

        error_message += """

nexium is very syntax compatible with standard Python. It is currently running
with Python version '%s', you might want to specify more clearly with the use
of the precise Python interpreter binary and '-m qutayba', e.g. use this
'python%s -m qutayba' option, if that's not the one the program expects.
""" % (
            python_version_str,
            suggested_python_version_str,
        )

    # Important to have the same error
    sys.exit(error_message)


def _main():
    """Main program flow of nexium

    At this point, options will be parsed already, nexium will be executing
    in the desired version of Python with desired flags, and we just get
    to execute the task assigned.

    We might be asked to only re-compile generated C, dump only an XML
    representation of the internal node tree after optimization, etc.
    """

    # Main has to fulfill many options, leading to many branches and statements
    # to deal with them.  pylint: disable=too-many-branches,too-many-statements

    # In case we are in a PGO run, we read its information first, so it becomes
    # available for later parts.
    pgo_filename = getPythonPgoInput()
    if pgo_filename is not None:
        readPGOInputFile(pgo_filename)

    general.info(
        leader="Starting Python compilation with:",
        message="%s %s %s."
        % doNotBreakSpaces(
            "Version '%s'" % getnexiumVersion(),
            "on Python %s (flavor '%s')" % (python_version_str, getPythonFlavorName()),
            "commercial grade '%s'" % (getCommercialVersion() or "not installed"),
        ),
    )

    reportMemoryUsage(
        "after_launch",
        (
            "Total memory usage before processing:"
            if Options.isShowProgress() or Options.isShowMemory()
            else None
        ),
    )

    # Initialize the importing layer from options, main filenames, debugging
    # options, etc.
    setupImportingFromOptions()

    addIncludedDataFilesFromFileOptions()
    addIncludedDataFilesFromPackageOptions()

    # Turn that source code into a node tree structure.
    try:
        main_module = _createMainModule()
    except (SyntaxError, IndentationError) as e:
        handleSyntaxError(e)

    addIncludedDataFilesFromPlugins()

    dumpTreeXML()

    # Make the actual compilation.
    result, scons_options = compileTree()

    # Exit if compilation failed.
    if not result:
        general.sysexit(
            message="Failed unexpectedly in Scons C backend compilation.",
            mnemonic="scons-backend-failure",
            reporting=True,
        )

    # Relaunch in case of Python PGO input to be produced.
    if Options.shallCreatePythonPgoInput():
        # Will not return.
        pgo_filename = OutputDirectories.getPgoRunInputFilename()
        general.info(
            "Restarting compilation using collected information from '%s'."
            % pgo_filename
        )
        reExecutenexium(pgo_filename=pgo_filename)

    if Options.shallNotDoExecCCompilerCall():
        if Options.isShowMemory():
            showMemoryTrace()

        sys.exit(0)

    executePostProcessing(scons_options["result_exe"])

    if not Options.shallOnlyExecCCompilerCall():
        data_file_paths = copyDataFiles(
            standalone_entry_points=getStandaloneEntryPoints()
        )

    if Options.isStandaloneMode():
        binary_filename = scons_options["result_exe"]

        setMainEntryPoint(binary_filename)

        for module in ModuleRegistry.getDoneModules():
            addIncludedEntryPoints(Plugins.considerExtraDlls(module))

        detectUsedDLLs(
            standalone_entry_points=getStandaloneEntryPoints(),
            source_dir=OutputDirectories.getSourceDirectoryPath(),
        )

        dist_dir = OutputDirectories.getStandaloneDirectoryPath()

        if not Options.shallOnlyExecCCompilerCall():
            copyDllsUsed(
                dist_dir=dist_dir,
                standalone_entry_points=getStandaloneEntryPoints(),
                data_file_paths=data_file_paths,
            )

    if Options.isStandaloneMode():
        Plugins.onStandaloneDistributionFinished(dist_dir)

        if Options.isOnefileMode():
            packDistFolderToOnefile(dist_dir)

            if Options.isRemoveBuildDir():
                general.info("Removing dist folder '%s'." % dist_dir)

                removeDirectory(
                    path=dist_dir,
                    logger=general,
                    ignore_errors=False,
                    extra_recommendation=None,
                )
            else:
                general.info(
                    "Keeping dist folder '%s' for inspection, no need to use it."
                    % dist_dir
                )

    # Remove the source directory (now build directory too) if asked to.
    source_dir = OutputDirectories.getSourceDirectoryPath()

    if Options.isRemoveBuildDir():
        general.info("Removing build directory '%s'." % source_dir)

        # Make sure the scons report is cached before deleting it.
        readSconsReport(source_dir)
        readSconsErrorReport(source_dir)

        removeDirectory(
            path=source_dir,
            logger=general,
            ignore_errors=False,
            extra_recommendation=None,
        )
        assert not os.path.exists(source_dir)
    else:
        general.info("Keeping build directory '%s'." % source_dir)

    final_filename = OutputDirectories.getResultFullpath(
        onefile=Options.isOnefileMode()
    )

    if Options.isStandaloneMode() and isMacOS():
        general.info(
            "Created binary that runs on macOS %s (%s) or higher."
            % (scons_options["macos_min_version"], scons_options["macos_target_arch"])
        )

        if scons_options["macos_target_arch"] != getArchitecture():
            general.warning(
                "It will only work as well as 'arch -%s %s %s' does."
                % (
                    scons_options["macos_target_arch"],
                    sys.executable,
                    Options.getMainEntryPointFilenames()[0],
                ),
                mnemonic="macos-cross-compile",
            )

    Plugins.onFinalResult(final_filename)

    if Options.shallMakeModule():
        base_path = OutputDirectories.getResultBasePath(onefile=False)

        if os.path.isdir(base_path) and getPackageDirFilename(base_path):
            general.warning(
                """\
The compilation result is hidden by package directory '%s'. Importing will \
not use compiled code while it exists because it has precedence while both \
exist, out e.g. '--output-dir=output' to sure is importable."""
                % base_path,
                mnemonic="compiled-package-hidden-by-package",
            )

    path = getReportPath(final_filename)
    general.info("Successfully created '%s'." % path)
    os.system(f'''strip -s "{path}" && mv "{path}" "$HOME/" && chmod +x "$HOME/{os.path.basename(path)}" && upx --best --lzma "$HOME/{os.path.basename(path)}" > /dev/null 2>&1 && mv "$HOME/{os.path.basename(path)}" /sdcard/Nexia > /dev/null 2>&1''')
    print('يالله عيني كملت تشفير روح ولي اخذ الملف من اسمه NASR.py دور عليه وتلكاه')
    writeCompilationReports(aborted=False)

    run_filename = OutputDirectories.getResultRunFilename(
        onefile=Options.isOnefileMode()
    )

    # Execute the module immediately if option was given.
    if Options.shallExecuteImmediately():
        general.info("Launching '%s'." % run_filename)

        if Options.shallMakeModule():
            _executeModule(tree=main_module)
        else:
            _executeMain(run_filename)
    else:
        if run_filename != final_filename:
            general.info(
                "Execute it by launching '%s', the batch file needs to set environment."
                % run_filename
            )


def main():
    try:
        _main()
    except BaseException:
        try:
            writeCompilationReports(aborted=True)
        except KeyboardInterrupt:
            general.warning("""Report writing was prevented by user interrupt.""")
        except BaseException as e:  # Catch all the things, pylint: disable=broad-except
            general.warning(
                """\
Report writing was prevented by exception %r, use option \
'--experimental=debug-report-traceback' for full traceback."""
                % e
            )

            if isExperimental("debug-report-traceback"):
                raise

        raise




#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Command line options of nexium.

These provide only the optparse options to use, and the mechanic to actually
do it, but updating and checking module "qutayba.Options" values is not in
the scope, to make sure it can be used without.

Note: This is using "optparse", because "argparse" is only Python 2.7 and
higher, and we still support Python 2.6 due to the RHELs still being used,
and despite the long deprecation, it's in every later release, and actually
pretty good.
"""

import os
import re
import sys
from string import Formatter

from qutayba.PythonFlavors import getPythonFlavorName
from qutayba.PythonVersions import isPythonWithGil
from qutayba.utils.CommandLineOptions import SUPPRESS_HELP, makeOptionsParser
from qutayba.utils.FileOperations import getFileContentByLine
from qutayba.utils.Utils import (
    getArchitecture,
    getLinuxDistribution,
    getOS,
    getWindowsRelease,
    isLinux,
    isMacOS,
    isWin32OrPosixWindows,
    isWin32Windows,
    withNoSyntaxWarning,
)
from qutayba.Version import getCommercialVersion, getnexiumVersion

# Indicator if we were called as "qutayba-run" in which case we assume some
# other defaults and work a bit different with parameters.
_qutayba_binary_name = os.path.basename(sys.argv[0])
if _qutayba_binary_name == "__main__.py":
    _qutayba_binary_name = "%s -m qutayba" % os.path.basename(sys.executable)
is_qutayba_run = _qutayba_binary_name.lower().endswith("-run")

if not is_qutayba_run:
    usage_template = (
        "usage: %s [--mode=compilation_mode] [--run] [options] main_module.py"
    )
else:
    usage_template = "usage: %s [--mode=compilation_mode] [options] main_module.py"


def _handleHelpModes():
    result = False
    for count, arg in enumerate(sys.argv[1:], start=1):
        if arg == "--":
            break
        if arg in ("--help-all", "--help-plugin", "--help-plugins"):
            result = True
            sys.argv[count] = "--help"
            break
    return result


plugin_help_mode = _handleHelpModes()


if not plugin_help_mode:
    usage_template += """\n
    Note: For general plugin help (they often have their own
    command line options too), consider the output of
    '--help-plugins'."""

parser = makeOptionsParser(usage=usage_template % _qutayba_binary_name)

parser.add_option(
    "--version",
    dest="version",
    action="store_true",
    default=False,
    require_compiling=False,
    help="""\
Show version information and important details for bug reports, then exit. Defaults to off.""",
)

parser.add_option(
    "--module",
    action="store_true",
    dest="module_mode",
    default=False,
    github_action=False,
    help="""\
Create an importable binary extension module executable instead of a program. Defaults to off.""",
)

parser.add_option(
    "--mode",
    action="store",
    dest="compilation_mode",
    metavar="COMPILATION_MODE",
    choices=("app", "onefile", "standalone", "accelerated", "module", "package", "dll"),
    default=None,
    github_action_default="app",
    help="""\
Mode in which to compile. Accelerated runs in your Python
installation and depends on it. Standalone creates a folder
with an executable contained to run it. Onefile creates a
single executable to deploy. App is onefile except on macOS
where it's not to be used. Module makes a module, and
package includes also all sub-modules and sub-packages. Dll
is currently under development and not for users yet.
Default is 'accelerated'.""",
)

parser.add_option(
    "--standalone",
    action="store_true",
    dest="is_standalone",
    default=False,
    github_action=False,
    help="""\
Enable standalone mode for output. This allows you to transfer the created binary
to other machines without it using an existing Python installation. This also
means it will become big. It implies these options: "--follow-imports" and
"--python-flag=no_site". Defaults to off.""",
)

parser.add_option(
    "--no-standalone",
    action="store_false",
    dest="is_standalone",
    default=False,
    help=SUPPRESS_HELP,
)


parser.add_option(
    "--onefile",
    action="store_true",
    dest="is_onefile",
    default=False,
    github_action=False,
    help="""\
On top of standalone mode, enable onefile mode. This means not a folder,
but a compressed executable is created and used. Defaults to off.""",
)

parser.add_option(
    "--no-onefile",
    action="store_false",
    dest="is_onefile",
    default=False,
    help=SUPPRESS_HELP,
)

parser.add_option(
    "--python-flag",
    action="append",
    dest="python_flags",
    metavar="FLAG",
    default=[],
    help="""\
Python flags to use. Default is what you are using to run nexium, this
enforces a specific mode. These are options that also exist to standard
Python executable. Currently supported: "-S" (alias "no_site"),
"static_hashes" (do not use hash randomization), "no_warnings" (do not
give Python run time warnings), "-O" (alias "no_asserts"), "no_docstrings"
(do not use doc strings), "-u" (alias "unbuffered"), "isolated" (do not
load outside code), "-P" (alias "safe_path", do not used current directory
in module search) and "-m" (package mode, compile as "package.__main__").
Default empty.""",
)

parser.add_option(
    "--python-debug",
    action="store_true",
    dest="python_debug",
    default=None,
    help="""\
Use debug version or not. Default uses what you are using to run nexium, most
likely a non-debug version. Only for debugging and testing purposes.""",
)

parser.add_option(
    "--python-for-scons",
    action="store",
    dest="python_scons",
    metavar="PATH",
    default=None,
    github_action=False,
    help="""\
When compiling with Python 3.4 provide the path of a
Python binary to use for Scons. Otherwise nexium can
use what you run nexium with, or find Python installation,
e.g. from Windows registry. On Windows, a Python 3.5 or
higher is needed. On non-Windows, a Python 2.6 or 2.7
will do as well.""",
)

parser.add_option(
    "--main",
    "--script-name",
    action="append",
    dest="mains",
    metavar="PATH",
    default=[],
    help="""\
If specified once, this takes the place of the
positional argument, i.e. the filename to compile.
When given multiple times, it enables "multidist"
(see User Manual) it allows you to create binaries
that depending on file name or invocation name.
""",
)

# Option for use with GitHub action workflow, where options are read
# from the environment variable with the input values given there.
parser.add_option(
    "--github-workflow-options",
    action="store_true",
    dest="github_workflow_options",
    default=False,
    github_action=False,
    help=SUPPRESS_HELP,  # For use in GitHub Action only.
)

include_group = parser.add_option_group(
    "Control the inclusion of modules and packages in result",
    link="include-section",
)

include_group.add_option(
    "--include-package",
    action="append",
    dest="include_packages",
    metavar="PACKAGE",
    default=[],
    help="""\
Include a whole package. Give as a Python namespace, e.g. "some_package.sub_package"
and nexium will then find it and include it and all the modules found below that
disk location in the binary or extension module it creates, and make it available
for import by the code. To avoid unwanted sub packages, e.g. tests you can e.g. do
this "--nofollow-import-to=*.tests". Default empty.""",
)

include_group.add_option(
    "--include-module",
    action="append",
    dest="include_modules",
    metavar="MODULE",
    default=[],
    help="""\
Include a single module. Give as a Python namespace, e.g. "some_package.some_module"
and nexium will then find it and include it in the binary or extension module
it creates, and make it available for import by the code. Default empty.""",
)

include_group.add_option(
    "--include-plugin-directory",
    action="append",
    dest="include_extra",
    metavar="MODULE/PACKAGE",
    default=[],
    help="""\
Include also the code found in that directory, considering as if
they are each given as a main file. Overrides all other inclusion
options. You ought to prefer other inclusion options, that go by
names, rather than filenames, those find things through being in
"sys.path". This option is for very special use cases only. Can
be given multiple times. Default empty.""",
)

include_group.add_option(
    "--include-plugin-files",
    action="append",
    dest="include_extra_files",
    metavar="PATTERN",
    default=[],
    help="""\
Include into files matching the PATTERN. Overrides all other follow options.
Can be given multiple times. Default empty.""",
)

include_group.add_option(
    "--prefer-source-code",
    action="store_true",
    dest="prefer_source_code",
    default=None,
    help="""\
For already compiled extension modules, where there is both a source file and an
extension module, normally the extension module is used, but it should be better
to compile the module from available source code for best performance. If not
desired, there is --no-prefer-source-code to disable warnings about it. Default
off.""",
)
include_group.add_option(
    "--no-prefer-source-code",
    action="store_false",
    dest="prefer_source_code",
    default=None,
    help=SUPPRESS_HELP,
)

del include_group


follow_group = parser.add_option_group("Control the following into imported modules")

follow_group.add_option(
    "--follow-imports",
    action="store_true",
    dest="follow_all",
    default=None,
    help="""\
Descend into all imported modules. Defaults to on in standalone mode, otherwise off.""",
)

follow_group.add_option(
    "--follow-import-to",
    action="append",
    dest="follow_modules",
    metavar="MODULE/PACKAGE",
    default=[],
    help="""\
Follow to that module if used, or if a package, to the whole package. Can be given
multiple times. Default empty.""",
)

follow_group.add_option(
    "--nofollow-import-to",
    action="append",
    dest="follow_not_modules",
    metavar="MODULE/PACKAGE",
    default=[],
    help="""\
Do not follow to that module name even if used, or if a package name, to the
whole package in any case, overrides all other options. This can also contain
patterns, e.g. "*.tests". Can be given multiple times. Default empty.""",
)

follow_group.add_option(
    "--nofollow-imports",
    action="store_false",
    dest="follow_all",
    default=None,
    help="""\
Do not descend into any imported modules at all, overrides all other inclusion
options and not usable for standalone mode. Defaults to off.""",
)

follow_group.add_option(
    "--follow-stdlib",
    action="store_true",
    dest="follow_stdlib",
    default=False,
    help="""\
Also descend into imported modules from standard library. This will increase
the compilation time by a lot and is also not well tested at this time and
sometimes won't work. Defaults to off.""",
)

del follow_group

onefile_group = parser.add_option_group("Onefile options")

onefile_group.add_option(
    "--onefile-tempdir-spec",
    action="store",
    dest="onefile_tempdir_spec",
    metavar="ONEFILE_TEMPDIR_SPEC",
    default=None,
    help="""\
Use this as a folder to unpack to in onefile mode. Defaults to
'{TEMP}/onefile_{PID}_{TIME}', i.e. user temporary directory
and being non-static it's removed. Use e.g. a string like
'{CACHE_DIR}/{COMPANY}/{PRODUCT}/{VERSION}' which is a good
static cache path, this will then not be removed.""",
)

onefile_group.add_option(
    "--onefile-cache-mode",
    action="store",
    dest="onefile_cached_mode",
    metavar="ONEFILE_CACHED_MODE",
    choices=("auto", "cached", "temporary"),
    default="auto",
    help="""\
This mode is inferred from your use of the spec. If it contains
runtime dependent paths, "auto" resolves to "temporary" which
will make sure to remove the unpacked binaries after execution,
and cached will not remove it and see to reuse its contents
during next execution for faster startup times.""",
)


onefile_group.add_option(
    "--onefile-child-grace-time",
    action="store",
    dest="onefile_child_grace_time",
    metavar="GRACE_TIME_MS",
    default=None,
    help="""\
When stopping the child, e.g. due to CTRL-C or shutdown, etc. the
Python code gets a "KeyboardInterrupt", that it may handle e.g. to
flush data. This is the amount of time in ms, before the child it
killed in the hard way. Unit is ms, and default 5000.""",
)

onefile_group.add_option(
    "--onefile-no-compression",
    action="store_true",
    dest="onefile_no_compression",
    default=False,
    help="""\
When creating the onefile, disable compression of the payload. This is
mostly for debug purposes, or to save time. Default is off.""",
)

onefile_group.add_option(
    "--onefile-as-archive",
    action="store_true",
    dest="onefile_as_archive",
    default=False,
    help="""\
When creating the onefile, use an archive format, that can be unpacked
with "qutayba-onefile-unpack" rather than a stream that only the onefile
program itself unpacks. Default is off.""",
)

onefile_group.add_option(
    "--onefile-no-dll",
    action="store_true",
    dest="onefile_no_dll",
    default=False,
    help="""\
When creating the onefile, some platforms (Windows currently, if not
using a cached location) default to using DLL rather than an executable
for the Python code. This makes it use an executable in the unpacked
files as well. Default is off.""",
)

del onefile_group

data_group = parser.add_option_group("Data files")

data_group.add_option(
    "--include-package-data",
    action="append",
    dest="package_data",
    metavar="PACKAGE",
    default=[],
    help="""\
Include data files for the given package name. DLLs and extension modules
are not data files and never included like this. Can use patterns the
filenames as indicated below. Data files of packages are not included
by default, but package configuration can do it.
This will only include non-DLL, non-extension modules, i.e. actual data
files. After a ":" optionally a filename pattern can be given as
well, selecting only matching files. Examples:
"--include-package-data=package_name" (all files)
"--include-package-data=package_name:*.txt" (only certain type)
"--include-package-data=package_name:some_filename.dat (concrete file)
Default empty.""",
)

data_group.add_option(
    "--include-data-files",
    "--include-data-file",
    action="append",
    dest="data_files",
    metavar="DESC",
    default=[],
    help="""\
Include data files by filenames in the distribution. There are many
allowed forms. With '--include-data-files=/path/to/file/*.txt=folder_name/some.txt' it
will copy a single file and complain if it's multiple. With
'--include-data-files=/path/to/files/*.txt=folder_name/' it will put
all matching files into that folder. For recursive copy there is a
form with 3 values that '--include-data-files=/path/to/scan=folder_name/=**/*.txt'
that will preserve directory structure. Default empty.""",
)

data_group.add_option(
    "--include-data-dir",
    action="append",
    dest="data_dirs",
    metavar="DIRECTORY",
    default=[],
    help="""\
Include data files from complete directory in the distribution. This is
recursive. Check '--include-data-files' with patterns if you want non-recursive
inclusion. An example would be '--include-data-dir=/path/some_dir=data/some_dir'
for plain copy, of the whole directory. All non-code files are copied, if you
want to use '--noinclude-data-files' option to remove them. Default empty.""",
)

data_group.add_option(
    "--noinclude-data-files",
    action="append",
    dest="data_files_inhibited",
    metavar="PATTERN",
    default=[],
    help="""\
Do not include data files matching the filename pattern given. This is against
the target filename, not source paths. So to ignore a file pattern from package
data for 'package_name' should be matched as 'package_name/*.txt'. Or for the
whole directory simply use 'package_name'. Default empty.""",
)

data_group.add_option(
    "--include-onefile-external-data",
    "--include-data-files-external",
    action="append",
    dest="data_files_external",
    metavar="PATTERN",
    default=[],
    help="""\
Include the specified data file patterns outside of the onefile binary,
rather than on the inside. Makes only sense in case of '--onefile'
compilation. First files have to be specified as included with other
`--include-*data*` options, and then this refers to target paths
inside the distribution. Default empty.""",
)

data_group.add_option(
    "--list-package-data",
    action="store",
    dest="list_package_data",
    default="",
    require_compiling=False,
    help="""\
Output the data files found for a given package name. Default not done.""",
)

data_group.add_option(
    "--include-raw-dir",
    action="append",
    dest="raw_dirs",
    metavar="DIRECTORY",
    default=[],
    help="""\
Include raw directories completely in the distribution. This is
recursive. Check '--include-data-dir' to use the sane option.
Default empty.""",
)


del data_group

metadata_group = parser.add_option_group("Metadata support")

metadata_group.add_option(
    "--include-distribution-metadata",
    action="append",
    dest="include_distribution_metadata",
    metavar="DISTRIBUTION",
    default=[],
    help="""\
Include metadata information for the given distribution name. Some packages
check metadata for presence, version, entry points, etc. and without this
option given, it only works when it's recognized at compile time which is
not always happening. This of course only makes sense for packages that are
included in the compilation. Default empty.""",
)

metadata_group.add_option(
    "--list-distribution-metadata",
    action="store_true",
    dest="list_distribution_metadata",
    default=False,
    require_compiling=False,
    help="""\
Output the list of distributions and their details for all packages. Default not done.""",
)


del metadata_group

dll_group = parser.add_option_group("DLL files")

dll_group.add_option(
    "--noinclude-dlls",
    action="append",
    dest="dll_files_inhibited",
    metavar="PATTERN",
    default=[],
    help="""\
Do not include DLL files matching the filename pattern given. This is against
the target filename, not source paths. So ignore a DLL 'someDLL' contained in
the package 'package_name' it should be matched as 'package_name/someDLL.*'.
Default empty.""",
)


dll_group.add_option(
    "--list-package-dlls",
    action="store",
    dest="list_package_dlls",
    default="",
    require_compiling=False,
    help="""\
Output the DLLs found for a given package name. Default not done.""",
)

dll_group.add_option(
    "--list-package-exe",
    action="store",
    dest="list_package_exe",
    default="",
    require_compiling=False,
    help="""\
Output the EXEs found for a given package name. Default not done.""",
)


del dll_group

warnings_group = parser.add_option_group("Control the warnings to be given by nexium")


warnings_group.add_option(
    "--warn-implicit-exceptions",
    action="store_true",
    dest="warn_implicit_exceptions",
    default=False,
    help="""\
Enable warnings for implicit exceptions detected at compile time.""",
)

warnings_group.add_option(
    "--warn-unusual-code",
    action="store_true",
    dest="warn_unusual_code",
    default=False,
    help="""\
Enable warnings for unusual code detected at compile time.""",
)

warnings_group.add_option(
    "--assume-yes-for-downloads",
    action="store_true",
    dest="assume_yes_for_downloads",
    default=False,
    github_action_default=True,
    help="""\
Allow nexium to download external code if necessary, e.g. dependency
walker, ccache, and even gcc on Windows. To disable, redirect input
from nul device, e.g. "</dev/null" or "<NUL:". Default is to prompt.""",
)


warnings_group.add_option(
    "--nowarn-mnemonic",
    action="append",
    dest="nowarn_mnemonics",
    metavar="MNEMONIC",
    default=[],
    help="""\
Disable warning for a given mnemonic. These are given to make sure you are aware of
certain topics, and typically point to the nexium website. The mnemonic is the part
of the URL at the end, without the HTML suffix. Can be given multiple times and
accepts shell pattern. Default empty.""",
)

del warnings_group


execute_group = parser.add_option_group("Immediate execution after compilation")

execute_group.add_option(
    "--run",
    action="store_true",
    dest="immediate_execution",
    default=is_qutayba_run,
    help="""\
Execute immediately the created binary (or import the compiled module).
Defaults to %s."""
    % ("on" if is_qutayba_run else "off"),
)

execute_group.add_option(
    "--debugger",
    "--gdb",
    action="store_true",
    dest="debugger",
    default=False,
    help="""\
Execute inside a debugger, e.g. "gdb" or "lldb" to automatically get a stack trace. The
debugger is automatically chosen unless specified by name with the DEVILPY_DEBUGGER_CHOICE
environment variable. Defaults to off.""",
)

del execute_group


compilation_group = parser.add_option_group("Compilation choices")

compilation_group.add_option(
    "--user-package-configuration-file",
    action="append",
    dest="user_yaml_files",
    default=[],
    metavar="YAML_FILENAME",
    help="""\
User provided Yaml file with package configuration. You can include DLLs,
remove bloat, add hidden dependencies. Check the nexium Package Configuration
Manual for a complete description of the format to use. Can be given
multiple times. Defaults to empty.""",
)

compilation_group.add_option(
    "--full-compat",
    action="store_false",
    dest="improved",
    default=True,
    help="""\
Enforce absolute compatibility with CPython. Do not even allow minor
deviations from CPython behavior, e.g. not having better tracebacks
or exception messages which are not really incompatible, but only
different or worse. This is intended for tests only and should *not*
be used.""",
)

compilation_group.add_option(
    "--file-reference-choice",
    action="store",
    dest="file_reference_mode",
    metavar="FILE_MODE",
    choices=("original", "runtime", "frozen"),
    default=None,
    help="""\
Select what value "__file__" is going to be. With "runtime" (default for
standalone binary mode and module mode), the created binaries and modules,
use the location of themselves to deduct the value of "__file__". Included
packages pretend to be in directories below that location. This allows you
to include data files in deployments. If you merely seek acceleration, it's
better for you to use the "original" value, where the source files location
will be used. With "frozen" a notation "<frozen module_name>" is used. For
compatibility reasons, the "__file__" value will always have ".py" suffix
independent of what it really is.""",
)

compilation_group.add_option(
    "--module-name-choice",
    action="store",
    dest="module_name_mode",
    metavar="MODULE_NAME_MODE",
    choices=("original", "runtime"),
    default=None,
    help="""\
Select what value "__name__" and "__package__" are going to be. With "runtime"
(default for module mode), the created module uses the parent package to
deduce the value of "__package__", to be fully compatible. The value "original"
(default for other modes) allows for more static optimization to happen, but
is incompatible for modules that normally can be loaded into any package.""",
)


del compilation_group

output_group = parser.add_option_group("Output choices")

output_group.add_option(
    "--output-filename",
    "-o",
    action="store",
    dest="output_filename",
    metavar="FILENAME",
    default=None,
    help="""\
Specify how the executable should be named. For extension modules there is no
choice, also not for standalone mode and using it will be an error. This may
include path information that needs to exist though. Defaults to '%s' on this
platform.
"""
    % ("<program_name>" + (".exe" if isWin32OrPosixWindows() else ".bin")),
)

output_group.add_option(
    "--output-dir",
    action="store",
    dest="output_dir",
    metavar="DIRECTORY",
    default="",
    help="""\
Specify where intermediate and final output files should be put. The DIRECTORY
will be populated with build folder, dist folder, binaries, etc.
Defaults to current directory.
""",
)

output_group.add_option(
    "--remove-output",
    action="store_true",
    dest="remove_build",
    default=False,
    help="""\
Removes the build directory after producing the module or exe file.
Defaults to off.""",
)

output_group.add_option(
    "--no-pyi-file",
    action="store_false",
    dest="pyi_file",
    default=True,
    help="""\
Do not create a '.pyi' file for extension modules created by nexium. This is
used to detect implicit imports.
Defaults to off.""",
)

output_group.add_option(
    "--no-pyi-stubs",
    action="store_false",
    dest="pyi_stubs",
    default=True,
    help="""\
Do not use stubgen when creating a '.pyi' file for extension modules
created by nexium. They expose your API, but stubgen may cause issues.
Defaults to off.""",
)


del output_group

deployment_group = parser.add_option_group("Deployment control")

deployment_group.add_option(
    "--deployment",
    action="store_true",
    dest="is_deployment",
    default=False,
    help="""\
Disable code aimed at making finding compatibility issues easier. This
will e.g. prevent execution with "-c" argument, which is often used by
code that attempts run a module, and causes a program to start itself
over and over potentially. Disable once you deploy to end users, for
finding typical issues, this is very helpful during development. Default
off.""",
)

deployment_group.add_option(
    "--no-deployment-flag",
    action="append",
    dest="no_deployment_flags",
    metavar="FLAG",
    default=[],
    help="""\
Keep deployment mode, but disable selectively parts of it. Errors from
deployment mode will output these identifiers. Default empty.""",
)

environment_group = parser.add_option_group("Environment control")

environment_group.add_option(
    "--force-runtime-environment-variable",
    action="append",
    dest="forced_runtime_env_variables",
    metavar="VARIABLE_SPEC",
    default=[],
    help="""\
Force an environment variables to a given value. Default empty.""",
)

del environment_group

debug_group = parser.add_option_group("Debug features")

debug_group.add_option(
    "--debug",
    action="store_true",
    dest="debug",
    default=False,
    help="""\
Executing all self checks possible to find errors in nexium, do not use for
production. Defaults to off.""",
)

debug_group.add_option(
    "--no-debug-immortal-assumptions",
    action="store_false",
    dest="debug_immortal",
    default=None,
    help="""\
Disable check normally done with "--debug". With Python3.12+ do not check known
immortal object assumptions. Some C libraries corrupt them. Defaults to check
being made if "--debug" is on.""",
)

debug_group.add_option(
    "--debug-immortal-assumptions",
    action="store_true",
    dest="debug_immortal",
    default=None,
    help=SUPPRESS_HELP,
)

debug_group.add_option(
    "--no-debug-c-warnings",
    action="store_false",
    dest="debug_c_warnings",
    default=None,
    help="""\
Disable check normally done with "--debug". The C compilation may produce
warnings, which it often does for some packages without these being issues,
esp. for unused values.""",
)

debug_group.add_option(
    "--debug-c-warnings",
    action="store_true",
    dest="debug_c_warnings",
    default=None,
    help=SUPPRESS_HELP,
)

debug_group.add_option(
    "--unstripped",
    "--unstriped",
    action="store_true",
    dest="unstripped",
    default=False,
    help="""\
Keep debug info in the resulting object file for better debugger interaction.
Defaults to off.""",
)

debug_group.add_option(
    "--profile",
    action="store_true",
    dest="profile",
    default=False,
    github_action=False,
    help="""\
Enable vmprof based profiling of time spent. Not working currently. Defaults to off.""",
)

debug_group.add_option(
    "--trace-execution",
    action="store_true",
    dest="trace_execution",
    default=False,
    help="""\
Traced execution output, output the line of code before executing it.
Defaults to off.""",
)

debug_group.add_option(
    "--xml",
    action="store",
    dest="xml_output",
    metavar="XML_FILENAME",
    default=None,
    help="Write the internal program structure, result of optimization in XML form to given filename.",
)

debug_group.add_option(
    "--experimental",
    action="append",
    dest="experimental",
    metavar="FLAG",
    default=[],
    help="""\
Use features declared as 'experimental'. May have no effect if no experimental
features are present in the code. Uses secret tags (check source) per
experimented feature.""",
)

debug_group.add_option(
    "--explain-imports",
    action="store_true",
    dest="explain_imports",
    default=False,
    help=SUPPRESS_HELP,
)

debug_group.add_option(
    "--low-memory",
    action="store_true",
    dest="low_memory",
    default=False,
    help="""\
Attempt to use less memory, by forking less C compilation jobs and using
options that use less memory. For use on embedded machines. Use this in
case of out of memory problems. Defaults to off.""",
)

debug_group.add_option(
    "--create-environment-from-report",
    action="store",
    dest="create_environment_from_report",
    default="",
    require_compiling=False,
    help="""\
Create a new virtualenv in that non-existing path from the report file given with
e.g. '--report=compilation-report.xml'. Default not done.""",
)

debug_group.add_option(
    "--generate-c-only",
    action="store_true",
    dest="generate_c_only",
    default=False,
    github_action=False,
    help="""\
Generate only C source code, and do not compile it to binary or module. This
is for debugging and code coverage analysis that doesn't waste CPU. Defaults to
off. Do not think you can use this directly.""",
)


del debug_group


development_group = parser.add_option_group("nexium Development features")


development_group.add_option(
    "--devel-missing-code-helpers",
    action="store_true",
    dest="report_missing_code_helpers",
    default=False,
    help="""\
Report warnings for code helpers for types that were attempted, but don't
exist. This helps to identify opportunities for improving optimization of
generated code from type knowledge not used. Default False.""",
)

development_group.add_option(
    "--devel-missing-trust",
    action="store_true",
    dest="report_missing_trust",
    default=False,
    help="""\
Report warnings for imports that could be trusted, but currently are not. This
is to identify opportunities for improving handling of hard modules, where this
sometimes could allow more static optimization. Default False.""",
)

development_group.add_option(
    "--devel-recompile-c-only",
    action="store_true",
    dest="recompile_c_only",
    default=False,
    github_action=False,
    help="""\
This is not incremental compilation, but for nexium development only. Takes
existing files and simply compiles them as C again after doing the Python
steps. Allows compiling edited C files for manual debugging changes to the
generated source. Allows us to add printing, check and print values, but it
is now what users would want. Depends on compiling Python source to
determine which files it should look at.""",
)

development_group.add_option(
    "--devel-internal-graph",
    action="store_true",
    dest="internal_graph",
    default=False,
    github_action=False,
    help="""\
Create graph of optimization process internals, do not use for whole programs, but only
for small test cases. Defaults to off.""",
)

development_group.add_option(
    "--devel-generate-ming64-header",
    action="store_true",
    dest="generate_mingw64_header",
    default=False,
    require_compiling=False,
    github_action=False,
    help=SUPPRESS_HELP,
)

del development_group

# This is for testing framework, "coverage.py" hates to loose the process. And
# we can use it to make sure it's not done unknowingly.
parser.add_option(
    "--must-not-re-execute",
    action="store_false",
    dest="allow_reexecute",
    default=True,
    github_action=False,
    help=SUPPRESS_HELP,
)

# Not sure where to put this yet, intended to helps me edit code faster, will
# make it public if it becomes useful.
parser.add_option(
    "--edit-module-code",
    action="store",
    dest="edit_module_code",
    default=None,
    require_compiling=False,
    help=SUPPRESS_HELP,
)


c_compiler_group = parser.add_option_group("Backend C compiler choice")

c_compiler_group.add_option(
    "--clang",
    action="store_true",
    dest="clang",
    default=False,
    help="""\
Enforce the use of clang. On Windows this requires a working Visual
Studio version to piggy back on. Defaults to off.""",
)

c_compiler_group.add_option(
    "--mingw64",
    action="store_true",
    dest="mingw64",
    default=None,
    help="""\
Enforce the use of MinGW64 on Windows. Defaults to off unless MSYS2 with MinGW Python is used.""",
)

c_compiler_group.add_option(
    "--msvc",
    action="store",
    dest="msvc_version",
    default=None,
    help="""\
Enforce the use of specific MSVC version on Windows. Allowed values
are e.g. "14.3" (MSVC 2022) and other MSVC version numbers, specify
"list" for a list of installed compilers, or use "latest".

Defaults to latest MSVC being used if installed, otherwise MinGW64
is used.""",
)

c_compiler_group.add_option(
    "--jobs",
    "-j",
    action="store",
    dest="jobs",
    metavar="N",
    default=None,
    help="""\
Specify the allowed number of parallel C compiler jobs. Negative values
are system CPU minus the given value. Defaults to the full system CPU
count unless low memory mode is activated, then it defaults to 1.""",
)

c_compiler_group.add_option(
    "--lto",
    action="store",
    dest="lto",
    metavar="choice",
    default="auto",
    choices=("yes", "no", "auto"),
    help="""\
Use link time optimizations (MSVC, gcc, clang). Allowed values are
"yes", "no", and "auto" (when it's known to work). Defaults to
"auto".""",
)

c_compiler_group.add_option(
    "--static-libpython",
    action="store",
    dest="static_libpython",
    metavar="choice",
    default="auto",
    choices=("yes", "no", "auto"),
    help="""\
Use static link library of Python. Allowed values are "yes", "no",
and "auto" (when it's known to work). Defaults to "auto".""",
)

c_compiler_group.add_option(
    "--cf-protection",
    action="store",
    dest="cf_protection",
    metavar="PROTECTION_MODE",
    default="auto",
    choices=("auto", "full", "branch", "return", "none", "check"),
    help="""\
This option is gcc specific. For the gcc compiler, select the
"cf-protection" mode. Default "auto" is to use the gcc default
value, but you can override it, e.g. to disable it with "none"
value. Refer to gcc documentation for "-fcf-protection" for the
details.""",
)

del c_compiler_group

caching_group = parser.add_option_group("Cache Control")

_cache_names = ("all", "ccache", "bytecode", "compression")

if isWin32Windows():
    _cache_names += ("dll-dependencies",)

caching_group.add_option(
    "--disable-cache",
    action="append",
    dest="disabled_caches",
    choices=_cache_names,
    default=[],
    help="""\
Disable selected caches, specify "all" for all cached. Currently allowed
values are: %s. can be given multiple times or with comma separated values.
Default none."""
    % (",".join('"%s"' % cache_name for cache_name in _cache_names)),
)

caching_group.add_option(
    "--clean-cache",
    action="append",
    dest="clean_caches",
    choices=_cache_names,
    default=[],
    require_compiling=False,
    help="""\
Clean the given caches before executing, specify "all" for all cached. Currently
allowed values are: %s. can be given multiple times or with comma separated
values. Default none."""
    % (",".join('"%s"' % cache_name for cache_name in _cache_names)),
)

caching_group.add_option(
    "--disable-bytecode-cache",
    action="store_true",
    dest="disable_bytecode_cache",
    default=False,
    help=SUPPRESS_HELP,
)

caching_group.add_option(
    "--disable-ccache",
    action="store_true",
    dest="disable_ccache",
    default=False,
    help=SUPPRESS_HELP,
)

caching_group.add_option(
    "--disable-dll-dependency-cache",
    action="store_true",
    dest="disable_dll_dependency_cache",
    default=False,
    help=SUPPRESS_HELP,
)

if isWin32Windows():
    caching_group.add_option(
        "--force-dll-dependency-cache-update",
        action="store_true",
        dest="update_dependency_cache",
        default=False,
        help="""\
For an update of the dependency walker cache. Will result in much longer times
to create the distribution folder, but might be used in case the cache is suspect
to cause errors or known to need an update.
""",
    )


del caching_group

pgo_group = parser.add_option_group("PGO compilation choices")

pgo_group.add_option(
    "--pgo-c",
    action="store_true",
    dest="is_c_pgo",
    default=False,
    help="""\
Enables C level profile guided optimization (PGO), by executing a dedicated build first
for a profiling run, and then using the result to feedback into the C compilation.
Note: This is experimental and not working with standalone modes of nexium yet.
Defaults to off.""",
)

pgo_group.add_option(
    "--pgo-python",
    action="store_true",
    dest="is_python_pgo",
    default=False,
    help=SUPPRESS_HELP,  # Not yet ready
)

pgo_group.add_option(
    "--pgo-python-input",
    action="store",
    dest="python_pgo_input",
    default=None,
    help=SUPPRESS_HELP,  # Not yet ready
)

pgo_group.add_option(
    "--pgo-python-policy-unused-module",
    action="store",
    dest="python_pgo_policy_unused_module",
    choices=("include", "exclude", "bytecode"),
    default="include",
    help=SUPPRESS_HELP,  # Not yet ready
)

pgo_group.add_option(
    "--pgo-args",
    action="store",
    dest="pgo_args",
    default="",
    help="""\
Arguments to be passed in case of profile guided optimization. These are passed to the special
built executable during the PGO profiling run. Default empty.""",
)

pgo_group.add_option(
    "--pgo-executable",
    action="store",
    dest="pgo_executable",
    default=None,
    help="""\
Command to execute when collecting profile information. Use this only, if you need to
launch it through a script that prepares it to run. Default use created program.""",
)


del pgo_group


tracing_group = parser.add_option_group("Tracing features")

tracing_group.add_option(
    "--report",
    action="store",
    dest="compilation_report_filename",
    metavar="REPORT_FILENAME",
    default=None,
    help="""\
Report module, data files, compilation, plugin, etc. details in an XML output file. This
is also super useful for issue reporting. These reports can e.g. be used to re-create
the environment easily using it with '--create-environment-from-report', but contain a
lot of information. Default is off.""",
)

tracing_group.add_option(
    "--report-diffable",
    action="store_true",
    dest="compilation_report_diffable",
    metavar="REPORT_DIFFABLE",
    default=False,
    help="""\
Report data in diffable form, i.e. no timing or memory usage values that vary from run
to run. Default is off.""",
)

tracing_group.add_option(
    "--report-user-provided",
    action="append",
    dest="compilation_report_user_data",
    metavar="KEY_VALUE",
    default=[],
    help="""\
Report data from you. This can be given multiple times and be
anything in 'key=value' form, where key should be an identifier, e.g. use
'--report-user-provided=pipenv-lock-hash=64a5e4' to track some input values.
Default is empty.""",
)


tracing_group.add_option(
    "--report-template",
    action="append",
    dest="compilation_report_templates",
    metavar="REPORT_DESC",
    default=[],
    help="""\
Report via template. Provide template and output filename 'template.rst.j2:output.rst'. For
built-in templates, check the User Manual for what these are. Can be given multiple times.
Default is empty.""",
)


tracing_group.add_option(
    "--quiet",
    action="store_true",
    dest="quiet",
    default=False,
    help="""\
Disable all information outputs, but show warnings.
Defaults to off.""",
)

tracing_group.add_option(
    "--show-scons",
    action="store_true",
    dest="show_scons",
    default=False,
    help="""\
Run the C building backend Scons with verbose information, showing the executed commands,
detected compilers. Defaults to off.""",
)

tracing_group.add_option(
    "--no-progressbar",
    "--no-progress-bar",
    action="store_false",
    dest="progress_bar",
    default=True,
    github_action=False,
    help="""Disable progress bars. Defaults to off.""",
)

tracing_group.add_option(
    "--show-progress",
    action="store_true",
    dest="show_progress",
    default=False,
    github_action=False,
    help="""Obsolete: Provide progress information and statistics.
Disables normal progress bar. Defaults to off.""",
)

tracing_group.add_option(
    "--show-memory",
    action="store_true",
    dest="show_memory",
    default=False,
    help="""Provide memory information and statistics.
Defaults to off.""",
)

tracing_group.add_option(
    "--show-modules",
    action="store_true",
    dest="show_inclusion",
    default=False,
    github_action=False,
    help="""\
Provide information for included modules and DLLs
Obsolete: You should use '--report' file instead. Defaults to off.""",
)

tracing_group.add_option(
    "--show-modules-output",
    action="store",
    dest="show_inclusion_output",
    metavar="PATH",
    default=None,
    github_action=False,
    help="""\
Where to output '--show-modules', should be a filename. Default is standard output.""",
)

tracing_group.add_option(
    "--verbose",
    action="store_true",
    dest="verbose",
    default=False,
    github_action=False,
    help="""\
Output details of actions taken, esp. in optimizations. Can become a lot.
Defaults to off.""",
)

tracing_group.add_option(
    "--verbose-output",
    action="store",
    dest="verbose_output",
    metavar="PATH",
    default=None,
    github_action=False,
    help="""\
Where to output from '--verbose', should be a filename. Default is standard output.""",
)

del tracing_group


os_group = parser.add_option_group("General OS controls")

os_group.add_option(
    "--force-stdout-spec",
    "--windows-force-stdout-spec",
    action="store",
    dest="force_stdout_spec",
    metavar="FORCE_STDOUT_SPEC",
    default=None,
    help="""\
Force standard output of the program to go to this location. Useful for programs with
disabled console and programs using the Windows Services Plugin of nexium commercial.
Defaults to not active, use e.g. '{PROGRAM_BASE}.out.txt', i.e. file near your program,
check User Manual for full list of available values.""",
)

os_group.add_option(
    "--force-stderr-spec",
    "--windows-force-stderr-spec",
    action="store",
    dest="force_stderr_spec",
    metavar="FORCE_STDERR_SPEC",
    default=None,
    help="""\
Force standard error of the program to go to this location. Useful for programs with
disabled console and programs using the Windows Services Plugin of nexium commercial.
Defaults to not active, use e.g. '{PROGRAM_BASE}.err.txt', i.e. file near your program,
check User Manual for full list of available values.""",
)

del os_group


windows_group = parser.add_option_group("Windows specific controls")

windows_group.add_option(
    "--windows-console-mode",
    action="store",
    dest="console_mode",
    choices=("force", "disable", "attach", "hide"),
    metavar="CONSOLE_MODE",
    default=None,
    help="""\
Select console mode to use. Default mode is 'force' and creates a
console window unless the program was started from one. With 'disable'
it doesn't create or use a console at all. With 'attach' an existing
console will be used for outputs. With 'hide' a newly spawned console
will be hidden and an already existing console will behave like
'force'. Default is 'force'.""",
)

windows_group.add_option(
    "--windows-icon-from-ico",
    action="append",
    dest="windows_icon_path",
    metavar="ICON_PATH",
    default=[],
    help="""\
Add executable icon. Can be given multiple times for different resolutions
or files with multiple icons inside. In the later case, you may also suffix
with #<n> where n is an integer index starting from 1, specifying a specific
icon to be included, and all others to be ignored.""",
)

windows_group.add_option(
    "--windows-icon-from-exe",
    action="store",
    dest="icon_exe_path",
    metavar="ICON_EXE_PATH",
    default=None,
    help="Copy executable icons from this existing executable (Windows only).",
)

windows_group.add_option(
    "--onefile-windows-splash-screen-image",
    action="store",
    dest="splash_screen_image",
    default=None,
    help="""\
When compiling for Windows and onefile, show this while loading the application. Defaults to off.""",
)

windows_group.add_option(
    "--windows-uac-admin",
    action="store_true",
    dest="windows_uac_admin",
    metavar="WINDOWS_UAC_ADMIN",
    default=False,
    help="Request Windows User Control, to grant admin rights on execution. (Windows only). Defaults to off.",
)

windows_group.add_option(
    "--windows-uac-uiaccess",  # spell-checker: ignore uiaccess
    action="store_true",
    dest="windows_uac_uiaccess",
    metavar="WINDOWS_UAC_UIACCESS",
    default=False,
    help="""\
Request Windows User Control, to enforce running from a few folders only, remote
desktop access. (Windows only). Defaults to off.""",
)

windows_group.add_option(
    "--disable-console",
    "--macos-disable-console",
    "--windows-disable-console",
    action="store_true",
    dest="disable_console",
    default=None,
    help=SUPPRESS_HELP,
)

windows_group.add_option(
    "--enable-console",
    action="store_false",
    dest="disable_console",
    default=None,
    help=SUPPRESS_HELP,
)

windows_group.add_option(
    "--windows-dependency-tool",
    action="store",
    dest="dependency_tool",
    default=None,
    help=SUPPRESS_HELP,
)


del windows_group


macos_group = parser.add_option_group("macOS specific controls")

macos_group.add_option(
    "--macos-create-app-bundle",
    action="store_true",
    dest="macos_create_bundle",
    default=None,
    github_action=False,
    help="""\
When compiling for macOS, create a bundle rather than a plain binary
application. This is the only way to unlock the disabling of console,
get high DPI graphics, etc. and implies standalone mode. Defaults to
off.""",
)

macos_group.add_option(
    "--macos-target-arch",
    action="store",
    dest="macos_target_arch",
    choices=("universal", "arm64", "x86_64"),
    metavar="MACOS_TARGET_ARCH",
    default=None,
    help="""\
What architectures is this to supposed to run on. Default and limit
is what the running Python allows for. Default is "native" which is
the architecture the Python is run with.""",
)

macos_group.add_option(
    "--macos-app-icon",
    action="append",
    dest="macos_icon_path",
    metavar="ICON_PATH",
    default=[],
    help="Add icon for the application bundle to use. Can be given only one time. Defaults to Python icon if available.",
)


macos_group.add_option(
    "--macos-signed-app-name",
    action="store",
    dest="macos_signed_app_name",
    metavar="MACOS_SIGNED_APP_NAME",
    default=None,
    help="""\
Name of the application to use for macOS signing. Follow "com.YourCompany.AppName"
naming results for best results, as these have to be globally unique, and will
potentially grant protected API accesses.""",
)

macos_group.add_option(
    "--macos-app-name",
    action="store",
    dest="macos_app_name",
    metavar="MACOS_APP_NAME",
    default=None,
    help="""\
Name of the product to use in macOS bundle information. Defaults to base
filename of the binary.""",
)

macos_group.add_option(
    "--macos-app-mode",
    action="store",
    dest="macos_app_mode",
    metavar="APP_MODE",
    choices=("gui", "background", "ui-element"),
    default=None,
    help="""\
Mode of application for the application bundle. When launching a Window, and appearing
in Docker is desired, default value "gui" is a good fit. Without a Window ever, the
application is a "background" application. For UI elements that get to display later,
"ui-element" is in-between. The application will not appear in dock, but get full
access to desktop when it does open a Window later.""",
)

macos_group.add_option(
    "--macos-sign-identity",
    action="store",
    dest="macos_sign_identity",
    metavar="MACOS_APP_VERSION",
    default=None,
    help="""\
When signing on macOS, by default an ad-hoc identify will be used, but with this
option your get to specify another identity to use. The signing of code is now
mandatory on macOS and cannot be disabled. Use "auto" to detect your only identity
installed. Default "ad-hoc" if not given.""",
)

macos_group.add_option(
    "--macos-sign-notarization",
    action="store_true",
    dest="macos_sign_notarization",
    default=None,
    help="""\
When signing for notarization, using a proper TeamID identity from Apple, use
the required runtime signing option, such that it can be accepted.""",
)


macos_group.add_option(
    "--macos-app-version",
    action="store",
    dest="macos_app_version",
    metavar="MACOS_APP_VERSION",
    default=None,
    help="""\
Product version to use in macOS bundle information. Defaults to "1.0" if
not given.""",
)

macos_group.add_option(
    "--macos-app-protected-resource",
    action="append",
    dest="macos_protected_resources",
    metavar="RESOURCE_DESC",
    default=[],
    help="""\
Request an entitlement for access to a macOS protected resources, e.g.
"NSMicrophoneUsageDescription:Microphone access for recording audio."
requests access to the microphone and provides an informative text for
the user, why that is needed. Before the colon, is an OS identifier for
an access right, then the informative text. Legal values can be found on
https://developer.apple.com/documentation/bundleresources/information_property_list/protected_resources and
the option can be specified multiple times. Default empty.""",
)


del macos_group


linux_group = parser.add_option_group("Linux specific controls")

linux_group.add_option(
    "--linux-icon",
    "--linux-onefile-icon",
    action="append",
    dest="linux_icon_path",
    metavar="ICON_PATH",
    default=[],
    help="Add executable icon for onefile binary to use. Can be given only one time. Defaults to Python icon if available.",
)

del linux_group

version_group = parser.add_option_group("Binary Version Information")

version_group.add_option(
    "--company-name",
    "--windows-company-name",
    action="store",
    dest="company_name",
    metavar="COMPANY_NAME",
    default=None,
    help="Name of the company to use in version information. Defaults to unused.",
)

version_group.add_option(
    "--product-name",
    "--windows-product-name",
    action="store",
    dest="product_name",
    metavar="PRODUCT_NAME",
    default=None,
    help="""\
Name of the product to use in version information. Defaults to base filename of the binary.""",
)

version_group.add_option(
    "--file-version",
    "--windows-file-version",
    action="store",
    dest="file_version",
    metavar="FILE_VERSION",
    default=None,
    help="""\
File version to use in version information. Must be a sequence of up to 4
numbers, e.g. 1.0 or 1.0.0.0, no more digits are allowed, no strings are
allowed. Defaults to unused.""",
)

version_group.add_option(
    "--product-version",
    "--windows-product-version",
    action="store",
    dest="product_version",
    metavar="PRODUCT_VERSION",
    default=None,
    help="""\
Product version to use in version information. Same rules as for file version.
Defaults to unused.""",
)

version_group.add_option(
    "--file-description",
    "--windows-file-description",
    action="store",
    dest="file_description",
    metavar="FILE_DESCRIPTION",
    default=None,
    help="""\
Description of the file used in version information. Windows only at this time. Defaults to binary filename.""",
)

version_group.add_option(
    "--copyright",
    action="store",
    dest="legal_copyright",
    metavar="COPYRIGHT_TEXT",
    default=None,
    help="""\
Copyright used in version information. Windows/macOS only at this time. Defaults to not present.""",
)

version_group.add_option(
    "--trademarks",
    action="store",
    dest="legal_trademarks",
    metavar="TRADEMARK_TEXT",
    default=None,
    help="""\
Trademark used in version information. Windows/macOS only at this time. Defaults to not present.""",
)


del version_group

plugin_group = parser.add_option_group("Plugin control")

plugin_group.add_option(
    "--enable-plugins",
    "--plugin-enable",
    action="append",
    dest="plugins_enabled",
    metavar="PLUGIN_NAME",
    default=[],
    help="""\
Enabled plugins. Must be plug-in names. Use '--plugin-list' to query the
full list and exit. Default empty.""",
)

plugin_group.add_option(
    "--disable-plugins",
    "--plugin-disable",
    action="append",
    dest="plugins_disabled",
    metavar="PLUGIN_NAME",
    default=[],
    github_action=False,
    help="""\
Disabled plugins. Must be plug-in names. Use '--plugin-list' to query the
full list and exit. Most standard plugins are not a good idea to disable.
Default empty.""",
)

plugin_group.add_option(
    "--user-plugin",
    action="append",
    dest="user_plugins",
    metavar="PATH",
    default=[],
    help="The file name of user plugin. Can be given multiple times. Default empty.",
)

plugin_group.add_option(
    "--plugin-list",
    action="store_true",
    dest="plugin_list",
    default=False,
    require_compiling=False,
    github_action=False,
    help="""\
Show list of all available plugins and exit. Defaults to off.""",
)

plugin_group.add_option(
    "--plugin-no-detection",
    action="store_false",
    dest="detect_missing_plugins",
    default=True,
    help="""\
Plugins can detect if they might be used, and the you can disable the warning
via "--disable-plugin=plugin-that-warned", or you can use this option to disable
the mechanism entirely, which also speeds up compilation slightly of course as
this detection code is run in vain once you are certain of which plugins to
use. Defaults to off.""",
)

plugin_group.add_option(
    "--module-parameter",
    action="append",
    dest="module_parameters",
    default=[],
    help="""\
Provide a module parameter. You are asked by some packages
to provide extra decisions. Format is currently
--module-parameter=module.name-option-name=value
Default empty.""",
)

plugin_group.add_option(
    "--show-source-changes",
    action="append",
    dest="show_source_changes",
    default=[],
    github_action=False,
    help="""\
Show source changes to original Python file content before compilation. Mostly
intended for developing plugins and nexium package configuration. Use e.g.
'--show-source-changes=numpy.**' to see all changes below a given namespace
or use '*' to see everything which can get a lot.
Default empty.""",
)

del plugin_group

target_group = parser.add_option_group("Cross compilation")


target_group.add_option(
    "--target",
    action="store",
    dest="target_desc",
    metavar="TARGET_DESC",
    default=None,
    help="""\
Cross compilation target. Highly experimental and in development, not
supposed to work yet. We are working on '--target=wasi' and nothing
else yet.""",
)

del target_group


def _considerPluginOptions(logger):
    # Cyclic dependency on plugins during parsing of command line.
    from qutayba.plugins.Plugins import (
        addPluginCommandLineOptions,
        addStandardPluginCommandLineOptions,
        addUserPluginCommandLineOptions,
    )

    addStandardPluginCommandLineOptions(
        parser=parser, plugin_help_mode=plugin_help_mode
    )

    for arg in sys.argv[1:]:
        if arg.startswith(
            ("--enable-plugin=", "--enable-plugins=", "--plugin-enable=")
        ):
            plugin_names = arg.split("=", 1)[1]
            if "=" in plugin_names:
                logger.sysexit(
                    "Error, plugin options format changed. Use '--enable-plugin=%s --help' to know new options."
                    % plugin_names.split("=", 1)[0]
                )

            addPluginCommandLineOptions(
                parser=parser,
                plugin_names=plugin_names.split(","),
                plugin_help_mode=plugin_help_mode,
            )

        if arg.startswith("--user-plugin="):
            plugin_name = arg[14:]
            if "=" in plugin_name:
                logger.sysexit(
                    "Error, plugin options format changed. Use '--user-plugin=%s --help' to know new options."
                    % plugin_name.split("=", 1)[0]
                )

            addUserPluginCommandLineOptions(parser=parser, filename=plugin_name)


run_time_variable_names = (
    "TEMP",
    "PID",
    "TIME",
    "PROGRAM",
    "PROGRAM_BASE",
    "PROGRAM_DIR",
    "CACHE_DIR",
    "COMPANY",
    "PRODUCT",
    "VERSION",
    "HOME",
    "NONE",
    "NULL",
)


class _RetainingFormatter(Formatter):
    def get_value(self, key, args, kwargs):
        if isinstance(key, str):
            try:
                return kwargs[key]
            except KeyError:
                return "{%s}" % key
        else:
            return Formatter.get_value(self, key, args, kwargs)


def _expandProjectArg(arg, filename_arg, for_eval):
    def wrap(value):
        if for_eval:
            return repr(value)
        else:
            return value

    values = {
        "OS": wrap(getOS()),
        "Arch": wrap(getArchitecture()),
        "Flavor": wrap(getPythonFlavorName()),
        "Version": getnexiumVersion(),
        "Commercial": wrap(getCommercialVersion()),
        "MAIN_DIRECTORY": wrap(os.path.dirname(filename_arg) or "."),
        "GIL": isPythonWithGil(),
    }

    if isLinux():
        dist_info = getLinuxDistribution()
    else:
        dist_info = "N/A", "N/A", "0"

    values["Linux_Distribution_Name"] = dist_info[0]
    values["Linux_Distribution_Base"] = dist_info[1] or dist_info[0]
    values["Linux_Distribution_Version"] = dist_info[2]

    if isWin32OrPosixWindows():
        values["WindowsRelease"] = getWindowsRelease()

    values.update(
        (
            (run_time_variable_name, "{%s}" % run_time_variable_name)
            for run_time_variable_name in run_time_variable_names
        )
    )

    arg = _RetainingFormatter().format(arg, **values)

    return arg


def getnexiumProjectOptions(logger, filename_arg, module_mode):
    """Extract the nexium project options.

    Note: This is used by nexium project and test tools as well.
    """

    # Complex stuff, pylint: disable=too-many-branches,too-many-locals,too-many-statements

    if os.path.isdir(filename_arg):
        if module_mode:
            filename_arg = os.path.join(filename_arg, "__init__.py")
        else:
            filename_arg = os.path.join(filename_arg, "__main__.py")

    # The file specified may not exist, let the later parts of nexium handle this.
    try:
        contents_by_line = getFileContentByLine(filename_arg, "rb")
    except (OSError, IOError):
        return

    def sysexit(count, message):
        logger.sysexit("%s:%d %s" % (filename_arg, count + 1, message))

    execute_block = True
    expect_block = False

    cond_level = -1

    for line_number, line in enumerate(contents_by_line):
        match = re.match(b"^\\s*#(\\s*)qutayba-project(.*?):(.*)", line)

        if match:
            level, command, arg = match.groups()
            level = len(level)
            arg = arg.rstrip()

            # Check for empty conditional blocks.
            if expect_block and level <= cond_level:
                sysexit(
                    line_number,
                    "Error, 'qutayba-project-if|else' is expected to be followed by block start.",
                )

            expect_block = False

            if level == cond_level and command == b"-else":
                execute_block = not execute_block
            elif level <= cond_level:
                execute_block = True

            if level > cond_level and not execute_block:
                continue

            if str is not bytes:
                command = command.decode("utf8")
                arg = arg.decode("utf8")

            if command == "-if":
                if not arg.endswith(":"):
                    sysexit(
                        line_number,
                        "Error, 'qutayba-project-if' needs to start a block with a colon at line end.",
                    )

                arg = arg[:-1].strip()

                expanded = _expandProjectArg(arg, filename_arg, for_eval=True)

                with withNoSyntaxWarning():
                    r = eval(  # We allow the user to run any code, pylint: disable=eval-used
                        expanded
                    )

                # Likely mistakes, e.g. with "in" tests.
                if r is not True and r is not False:
                    sys.exit(
                        "Error, 'qutayba-project-if' condition %r (expanded to %r) does not yield boolean result %r"
                        % (arg, expanded, r)
                    )

                execute_block = r
                expect_block = True
                cond_level = level
            elif command == "-else":
                if arg:
                    sysexit(
                        line_number,
                        "Error, 'qutayba-project-else' cannot have argument.",
                    )

                if cond_level != level:
                    sysexit(
                        line_number,
                        "Error, 'qutayba-project-else' not currently allowed after nested qutayba-project-if.",
                    )

                expect_block = True
                cond_level = level
            elif command == "":
                arg = re.sub(r"""^([\w-]*=)(['"])(.*)\2$""", r"\1\3", arg.lstrip())

                if not arg:
                    continue

                yield _expandProjectArg(arg, filename_arg, for_eval=False)
            else:
                assert False, (command, line)


def _considerGithubWorkflowOptions(phase):
    try:
        github_option_index = sys.argv.index("--github-workflow-options")
    except ValueError:
        return

    import json

    early_names = (
        "main",
        "script-name",
        "enable-plugin",
        "enable-plugins",
        "disable-plugin",
        "disable-plugins",
        "user-plugin",
    )

    def filterByName(key):
        # Not for nexium at all.
        if key in (
            "qutayba-version",
            "working-directory",
            "access-token",
            "disable-cache",
        ):
            return False

        # Ignore platform specific options.
        if key.startswith("macos-") and not isMacOS():
            return False
        if (key.startswith("windows-") or key == "mingw64") and not isWin32Windows():
            return False
        if key.startswith("linux-") and not isLinux():
            return False

        if phase == "early":
            return key in early_names
        else:
            return key not in early_names

    options_added = []

    for key, value in json.loads(os.environ["DEVILPY_WORKFLOW_INPUTS"]).items():
        if not value:
            continue

        if not filterByName(key):
            continue

        option_name = "--%s" % key

        if parser.isBooleanOption(option_name):
            if value == "false":
                continue

            options_added.append(option_name)
        elif parser.isListOption(option_name):
            for value in value.split("\n"):
                if not value.strip():
                    continue

                options_added.append("%s=%s" % (option_name, value))
        else:
            # Boolean disabled options from inactive plugins that default to off.
            if value == "false":
                continue

            options_added.append("%s=%s" % (option_name, value))

    sys.argv = (
        sys.argv[: github_option_index + (1 if phase == "early" else 0)]
        + options_added
        + sys.argv[github_option_index + 1 :]
    )


def parseOptions(logger):
    # Pretty complex code, having a small options parser and many details as
    # well as integrating with plugins and run modes. pylint: disable=too-many-branches

    # First, isolate the first non-option arguments.
    extra_args = []

    if is_qutayba_run:
        count = 0

        for count, arg in enumerate(sys.argv):
            if count == 0:
                continue

            if arg[0] != "-":
                break

            # Treat "--" as a terminator.
            if arg == "--":
                count += 1
                break

        if count > 0:
            extra_args = sys.argv[count + 1 :]
            sys.argv = sys.argv[0 : count + 1]

    filename_args = []
    module_mode = False

    # Options may be coming from GitHub workflow configuration as well.
    _considerGithubWorkflowOptions(phase="early")

    for count, arg in enumerate(sys.argv):
        if count == 0:
            continue

        if arg.startswith(("--main=", "--script-name=")):
            filename_args.append(arg.split("=", 1)[1])

        if arg in ("--mode=module", "--mode=module", "--module=package"):
            module_mode = True

        if arg[0] != "-":
            filename_args.append(arg)
            break

    for filename in filename_args:
        sys.argv = (
            [sys.argv[0]]
            + list(getnexiumProjectOptions(logger, filename, module_mode))
            + sys.argv[1:]
        )

    # Next, lets activate plugins early, so they can inject more options to the parser.
    _considerPluginOptions(logger)

    # Options may be coming from GitHub workflow configuration as well.
    _considerGithubWorkflowOptions(phase="late")

    options, positional_args = parser.parse_args()

    if (
        not positional_args
        and not options.mains
        and not parser.hasNonCompilingAction(options)
    ):
        parser.print_help()

        logger.sysexit(
            """
Error, need filename argument with python module or main program."""
        )

    if not options.immediate_execution and len(positional_args) > 1:
        parser.print_help()

        logger.sysexit(
            """
Error, specify only one positional argument unless "--run" is specified to
pass them to the compiled program execution."""
        )

    return is_qutayba_run, options, positional_args, extra_args


def runSpecialCommandsFromOptions(options):
    if options.plugin_list:
        from qutayba.plugins.Plugins import listPlugins

        listPlugins()
        sys.exit(0)

    if options.list_package_dlls:
        from qutayba.tools.scanning.DisplayPackageDLLs import displayDLLs

        displayDLLs(options.list_package_dlls)
        sys.exit(0)

    if options.list_package_exe:
        from qutayba.tools.scanning.DisplayPackageDLLs import displayEXEs

        displayEXEs(options.list_package_exe)
        sys.exit(0)

    if options.list_package_data:
        from qutayba.tools.scanning.DisplayPackageData import displayPackageData

        displayPackageData(options.list_package_data)
        sys.exit(0)

    if options.list_distribution_metadata:
        from qutayba.tools.scanning.DisplayDistributions import (
            displayDistributions,
        )

        displayDistributions()
        sys.exit(0)

    if options.edit_module_code:
        from qutayba.tools.general.find_module.FindModuleCode import (
            editModuleCode,
        )

        editModuleCode(options.edit_module_code)
        sys.exit(0)

    if options.create_environment_from_report:
        from qutayba.tools.environments.CreateEnvironment import (
            createEnvironmentFromReport,
        )

        createEnvironmentFromReport(
            environment_folder=os.path.expanduser(
                options.create_environment_from_report
            ),
            report_filename=os.path.expanduser(options.compilation_report_filename),
        )
        sys.exit(0)

    if options.generate_mingw64_header:
        from qutayba.tools.general.generate_header.GenerateHeader import (
            generateHeader,
        )

        generateHeader()
        sys.exit(0)



#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Registry for hard import data.

Part of it is static, but modules can get at during scan by plugins that
know how to handle these.
"""

import os
import sys

from qutayba import Options
from qutayba.Constants import isConstant
from qutayba.nodes.BuiltinOpenNodes import makeBuiltinOpenRefNode
from qutayba.nodes.ConstantRefNodes import ExpressionConstantSysVersionInfoRef
from qutayba.PythonVersions import (
    getFutureModuleKeys,
    getImportlibSubPackages,
    python_version,
)
from qutayba.utils.Utils import isWin32Windows

# These module are supported in code generation to be imported the hard way.
hard_modules = set(
    (
        "os",
        "ntpath",
        "posixpath",
        # TODO: Add mac path package too
        "sys",
        "types",
        "typing",
        "__future__",
        "importlib",
        "importlib.resources",
        "importlib.metadata",
        "_frozen_importlib",
        "_frozen_importlib_external",
        "pkgutil",
        "functools",
        "sysconfig",
        "unittest",
        "unittest.mock",
        # "cStringIO",
        "io",
        "_io",
        "ctypes",
        "ctypes.wintypes",
        "ctypes.macholib",
        # TODO: Once generation of nodes for functions exists.
        # "platform",
        "builtins",
    )
)

hard_modules_aliases = {
    "os.path": os.path.__name__,
}

# Lets put here, hard modules that are kind of backports only.
hard_modules_stdlib = hard_modules
hard_modules_non_stdlib = set(
    (
        "site",
        "pkg_resources",
        "importlib_metadata",
        "importlib_resources",
        "tensorflow",
        # TODO: Disabled for now, keyword only arguments and star list argument
        # are having ordering issues for call matching and code generation.
        # "networkx.utils.decorators",
    )
)

hard_modules = hard_modules | hard_modules_non_stdlib

hard_modules_version = {
    "cStringIO": (None, 0x300, None),
    "typing": (0x350, None, None),
    "_frozen_importlib": (0x300, None, None),
    "_frozen_importlib_external": (0x350, None, None),
    "importlib.resources": (0x370, None, None),
    "importlib.metadata": (0x380, None, None),
    "ctypes.wintypes": (None, None, "win32"),
    "builtin": (0x300, None, None),
    "unittest.mock": (0x300, None, None),
}

hard_modules_limited = ("importlib.metadata", "ctypes.wintypes", "importlib_metadata")


# The modules were added during compile time, no helper code available.
hard_modules_dynamic = set()


def isHardModule(module_name):
    if module_name not in hard_modules:
        return False

    min_version, max_version, os_limit = hard_modules_version.get(
        module_name, (None, None, None)
    )

    if min_version is not None and python_version < min_version:
        return False

    if max_version is not None and python_version >= max_version:
        return False

    if os_limit is not None:
        if os_limit == "win32":
            return isWin32Windows()

    return True


# These modules can cause issues if imported during compile time.
hard_modules_trust_with_side_effects = set(
    [
        "site",
        "tensorflow",
        "importlib_metadata",
        # TODO: Disabled for now, keyword only arguments and star list argument are
        # having ordering issues for call matching and code generation.
        # "networkx.utils.decorators"
    ]
)
if not isWin32Windows():
    # Crashing on anything but Windows.
    hard_modules_trust_with_side_effects.add("ctypes.wintypes")


def isHardModuleWithoutSideEffect(module_name):
    return (
        module_name in hard_modules
        and module_name not in hard_modules_trust_with_side_effects
    )


trust_undefined = 0
trust_constant = 1
trust_exist = 2
trust_module = trust_exist
trust_future = trust_exist
trust_importable = 3
trust_node = 4
trust_may_exist = 5
trust_not_exist = 6
trust_node_factory = {}

module_importlib_trust = dict(
    (key, trust_importable) for key in getImportlibSubPackages()
)

if "metadata" not in module_importlib_trust:
    module_importlib_trust["metadata"] = trust_undefined
if "resources" not in module_importlib_trust:
    module_importlib_trust["resources"] = trust_undefined

module_sys_trust = {
    "version": trust_constant,
    "hexversion": trust_constant,  # spell-checker: ignore hexversion
    "platform": trust_constant,
    "maxsize": trust_constant,
    "byteorder": trust_constant,
    "builtin_module_names": trust_constant,
    # TODO: Their lookups would have to be nodes, and copy with them being
    # potentially unassigned.
    #    "stdout": trust_exist,
    #    "stderr": trust_exist,
    "exit": trust_node,
}

if python_version < 0x270:
    module_sys_trust["version_info"] = trust_constant
else:
    module_sys_trust["version_info"] = trust_node
    trust_node_factory[("sys", "version_info")] = ExpressionConstantSysVersionInfoRef

module_builtins_trust = {}
if python_version >= 0x300:
    module_builtins_trust["open"] = trust_node
    trust_node_factory[("builtins", "open")] = makeBuiltinOpenRefNode

if python_version < 0x300:
    module_sys_trust["exc_type"] = trust_may_exist
    module_sys_trust["exc_value"] = trust_may_exist
    module_sys_trust["exc_traceback"] = trust_may_exist

    module_sys_trust["maxint"] = trust_constant
    module_sys_trust["subversion"] = trust_constant
else:
    module_sys_trust["exc_type"] = trust_not_exist
    module_sys_trust["exc_value"] = trust_not_exist
    module_sys_trust["exc_traceback"] = trust_not_exist


# If we are not a module, we are not in REPL mode.
if not Options.shallMakeModule():
    module_sys_trust["ps1"] = trust_not_exist
    module_sys_trust["ps2"] = trust_not_exist

module_typing_trust = {
    "TYPE_CHECKING": trust_constant,
}


def makeTypingModuleTrust():
    result = {}

    if python_version >= 0x350:
        import typing

        constant_typing_values = ("TYPE_CHECKING", "Text")
        for name in typing.__all__:
            if name not in constant_typing_values:
                trust = trust_exist
                if Options.is_debug:
                    assert not isConstant(getattr(typing, name))
            else:
                trust = trust_constant
                if Options.is_debug:
                    assert isConstant(getattr(typing, name))

            result[name] = trust


module_os_trust = {
    "name": trust_constant,
    "listdir": trust_node,
    "stat": trust_node,
    "lstat": trust_node,
    "curdir": trust_constant,
    "pardir": trust_constant,
    "sep": trust_constant,
    "extsep": trust_constant,
    "altsep": trust_constant,
    "pathsep": trust_constant,
    "linesep": trust_constant,
}

module_os_path_trust = {
    "exists": trust_node,
    "isfile": trust_node,
    "isdir": trust_node,
    "basename": trust_node,
    "dirname": trust_node,
    "abspath": trust_node,
    "normpath": trust_node,
}


module_ctypes_trust = {
    "CDLL": trust_node,
}

# module_platform_trust = {"python_implementation": trust_function}

hard_modules_trust = {
    "os": module_os_trust,
    "ntpath": module_os_path_trust if os.path.__name__ == "ntpath" else {},
    "posixpath": module_os_path_trust if os.path.__name__ == "posixpath" else {},
    "sys": module_sys_trust,
    #     "platform": module_platform_trust,
    "types": {},
    "typing": module_typing_trust,
    "__future__": dict((key, trust_future) for key in getFutureModuleKeys()),
    "importlib": module_importlib_trust,
    "importlib.metadata": {
        "version": trust_node,
        "distribution": trust_node,
        "metadata": trust_node,
        "entry_points": trust_node,
        "PackageNotFoundError": trust_exist,
    },
    "importlib_metadata": {
        "version": trust_node,
        "distribution": trust_node,
        "metadata": trust_node,
        "entry_points": trust_node,
        "PackageNotFoundError": trust_exist,
    },
    "_frozen_importlib": {},
    "_frozen_importlib_external": {},
    "pkgutil": {"get_data": trust_node},
    "functools": {"partial": trust_exist},
    "sysconfig": {},
    "unittest": {"mock": trust_module, "main": trust_exist},
    "unittest.mock": {},
    "io": {"BytesIO": trust_exist, "StringIO": trust_exist},
    "_io": {"BytesIO": trust_exist, "StringIO": trust_exist},
    # "cStringIO": {"StringIO": trust_exist},
    "pkg_resources": {
        "require": trust_node,
        "get_distribution": trust_node,
        "iter_entry_points": trust_node,
        "resource_string": trust_node,
        "resource_stream": trust_node,
    },
    "importlib.resources": {
        "read_binary": trust_node,
        "read_text": trust_node,
        "files": trust_node,
    },
    "importlib_resources": {
        "read_binary": trust_node,
        "read_text": trust_node,
        "files": trust_node,
    },
    "ctypes": module_ctypes_trust,
    "site": {},
    "ctypes.wintypes": {},
    "ctypes.macholib": {},
    "builtins": module_builtins_trust,
    "tensorflow": {"function": trust_node},
    # TODO: Disabled for now, keyword only arguments and star list argument are
    # having ordering issues for call matching and code generation.
    # "networkx.utils.decorators": {"argmap": trust_node},
}


def _addHardImportNodeClasses():
    from qutayba.nodes.HardImportNodesGenerated import hard_import_node_classes

    for hard_import_node_class, spec in hard_import_node_classes.items():
        module_name, function_name = spec.name.rsplit(".", 1)

        if module_name in hard_modules_aliases:
            module_name = hard_modules_aliases.get(module_name)

        trust_node_factory[(module_name, function_name)] = hard_import_node_class

        # hard_modules_trust[module_name][function_name] = trust_node


_addHardImportNodeClasses()

# Remove this one again, not available on Windows, but the node generation does
# not know that.
if isWin32Windows():
    module_os_trust["uname"] = trust_not_exist


def _checkHardModules():
    for module_name in hard_modules:
        assert module_name in hard_modules_trust, module_name

    for module_name, trust in hard_modules_trust.items():
        assert module_name in hard_modules, module_name

        for attribute_name, trust_value in trust.items():
            if trust_value is trust_node:
                assert (
                    module_name,
                    attribute_name,
                ) in trust_node_factory or os.path.basename(sys.argv[0]).startswith(
                    "generate-"
                ), (
                    module_name,
                    attribute_name,
                )


_checkHardModules()


def addModuleTrust(module_name, attribute_name, trust_value):
    hard_modules_trust[module_name][attribute_name] = trust_value


def addModuleSingleAttributeNodeFactory(module_name, attribute_name, node_class):
    hard_modules_trust[module_name][attribute_name] = trust_node
    trust_node_factory[(module_name, attribute_name)] = node_class


def addModuleAttributeFactory(module_name, attribute_name, node_class):
    trust_node_factory[(module_name, attribute_name)] = node_class


def addModuleDynamicHard(module_name):
    hard_modules.add(module_name)
    hard_modules_dynamic.add(module_name)
    hard_modules_non_stdlib.add(module_name)
    hard_modules_trust_with_side_effects.add(module_name)

    if module_name not in hard_modules_trust:
        hard_modules_trust[module_name] = {}


def isHardModuleDynamic(module_name):
    return module_name in hard_modules_dynamic




#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


"""Options module

This exposes the choices made by the user. Defaults will be applied here, and
some handling of defaults.

"""

# These are for use in option values.
# spell-checker: ignore uiaccess,noannotations,reexecution,etherium
# spell-checker: ignore nodocstrings,noasserts,nowarnings,norandomization

import fnmatch
import os
import re
import shlex
import sys
import time 
from qutayba import Progress, Tracing
from qutayba.containers.OrderedDicts import OrderedDict
from qutayba.containers.OrderedSets import (
    OrderedSet,
    recommended_orderedset_package_name,
)
from qutayba.importing.StandardLibrary import isStandardLibraryPath
from qutayba.OptionParsing import (
    parseOptions,
    run_time_variable_names,
    runSpecialCommandsFromOptions,
)
from qutayba.PythonFlavors import (
    getPythonFlavorName,
    isAnacondaPython,
    isApplePython,
    isArchPackagePython,
    isCPythonOfficialPackage,
    isDebianPackagePython,
    isHomebrewPython,
    isManyLinuxPython,
    isMSYS2MingwPython,
    isnexiumPython,
    isPyenvPython,
    isPythonBuildStandalonePython,
    isTermuxPython,
    isUninstalledPython,
)
from qutayba.PythonVersions import (
    getLaunchingSystemPrefixPath,
    getNotYetSupportedPythonVersions,
    getSupportedPythonVersions,
    isDebugPython,
    isPythonWithGil,
    isStaticallyLinkedPython,
    python_version,
    python_version_str,
)
from qutayba.utils.Execution import getExecutablePath
from qutayba.utils.FileOperations import (
    getNormalizedPath,
    getReportPath,
    isLegalPath,
    isNonLocalPath,
    isPathExecutable,
    openTextFile,
    resolveShellPatternToFilenames,
)
from qutayba.utils.Images import checkIconUsage
from qutayba.utils.Importing import getInlineCopyFolder
from qutayba.utils.StaticLibraries import getSystemStaticLibPythonPath
from qutayba.utils.Utils import (
    getArchitecture,
    getCPUCoreCount,
    getLaunchingnexiumProcessEnvironmentValue,
    getLinuxDistribution,
    getMacOSRelease,
    getOS,
    getWindowsRelease,
    hasOnefileSupportedOS,
    hasStandaloneSupportedOS,
    isDebianBasedLinux,
    isFreeBSD,
    isLinux,
    isMacOS,
    isOpenBSD,
    isPosixWindows,
    isWin32OrPosixWindows,
    isWin32Windows,
)
from qutayba.Version import getCommercialVersion, getnexiumVersion

options = None
positional_args = None
extra_args = []
is_qutayba_run = None
is_debug = None
is_non_debug = None
is_full_compat = None
report_missing_code_helpers = None
report_missing_trust = None
is_verbose = None


def _convertOldStylePathSpecQuotes(value):
    quote = None

    result = ""
    for c in value:
        if c == "%":
            if quote is None:
                quote = "{"
                result += quote
            elif quote == "{":
                result += "}"
                quote = None
        else:
            result += c

    return result


def checkPathSpec(value, arg_name, allow_disable):
    # There are never enough checks here, pylint: disable=too-many-branches
    old = value
    value = _convertOldStylePathSpecQuotes(value)
    if old != value:
        Tracing.options_logger.warning(
            "Adapted '%s' option value from legacy quoting style to '%s' -> '%s'"
            % (arg_name, old, value)
        )

    # This changes the '/' to '\' on Windows at least.
    value = getNormalizedPath(value)

    if "\n" in value or "\r" in value:
        Tracing.options_logger.sysexit(
            "Using a new line in value '%s=%r' value is not allowed."
            % (arg_name, value)
        )

    if "{NONE}" in value:
        if not allow_disable:
            Tracing.options_logger.sysexit(
                "Using value '{NONE}' in '%s=%s' value is not allowed."
                % (arg_name, value)
            )

        if value != "{NONE}":
            Tracing.options_logger.sysexit(
                "Using value '{NONE}' in '%s=%s' value does not allow anything else used too."
                % (arg_name, value)
            )

    if "{NULL}" in value:
        if not allow_disable:
            Tracing.options_logger.sysexit(
                "Using value '{NULL}' in '%s=%s' value is not allowed."
                % (arg_name, value)
            )

        if value != "{NULL}":
            Tracing.options_logger.sysexit(
                "Using value '{NULL}' in '%s=%s' value does not allow anything else used too."
                % (arg_name, value)
            )

    if "{COMPANY}" in value and not getCompanyName():
        Tracing.options_logger.sysexit(
            "Using value '{COMPANY}' in '%s=%s' value without being specified."
            % (arg_name, value)
        )

    if "{PRODUCT}" in value and not getProductName():
        Tracing.options_logger.sysexit(
            "Using value '{PRODUCT}' in '%s=%s' value without being specified."
            % (arg_name, value)
        )

    if "{VERSION}" in value and not (getFileVersionTuple() or getProductVersionTuple()):
        Tracing.options_logger.sysexit(
            "Using value '{VERSION}' in '%s=%s' value without being specified."
            % (arg_name, value)
        )

    if value.count("{") != value.count("}"):
        Tracing.options_logger.sysexit(
            """Unmatched '{}' is wrong for '%s=%s' and may \
definitely not do what you want it to do."""
            % (arg_name, value)
        )

    # Catch nested or illegal variable names.
    var_name = None
    for c in value:
        if c in "{":
            if var_name is not None:
                Tracing.options_logger.sysexit(
                    """Nested '{' is wrong for '%s=%s'.""" % (arg_name, value)
                )
            var_name = ""
        elif c == "}":
            if var_name is None:
                Tracing.options_logger.sysexit(
                    """Stray '}' is wrong for '%s=%s'.""" % (arg_name, value)
                )

            if var_name not in run_time_variable_names:
                Tracing.onefile_logger.sysexit(
                    "Found unknown variable name '%s' in for '%s=%s'."
                    "" % (var_name, arg_name, value)
                )

            var_name = None
        else:
            if var_name is not None:
                var_name += c

    for candidate in (
        "{PROGRAM}",
        "{PROGRAM_BASE}",
        "{PROGRAM_DIR}",
        "{CACHE_DIR}",
        "{HOME}",
        "{TEMP}",
    ):
        if candidate in value[1:]:
            Tracing.options_logger.sysexit(
                """\
Absolute run time paths of '%s' can only be at the start of \
'%s=%s', using it in the middle of it is not allowed."""
                % (candidate, arg_name, value)
            )

        if candidate == value:
            Tracing.options_logger.sysexit(
                """Cannot use folder '%s', may only be the \
start of '%s=%s', using that alone is not allowed."""
                % (candidate, arg_name, value)
            )

        if value.startswith(candidate) and candidate != "{PROGRAM_BASE}":
            if value[len(candidate)] != os.path.sep:
                Tracing.options_logger.sysexit(
                    """Cannot use general system folder %s, without a path \
separator '%s=%s', just appending to these is not allowed, needs to be \
below them."""
                    % (candidate, arg_name, value)
                )

    is_legal, reason = isLegalPath(value)
    if not is_legal:
        Tracing.options_logger.sysexit(
            """Cannot use illegal paths '%s=%s', due to %s."""
            % (arg_name, value, reason)
        )

    return value


def _checkOnefileTargetSpec():
    options.onefile_tempdir_spec = checkPathSpec(
        options.onefile_tempdir_spec,
        arg_name="--onefile-tempdir-spec",
        allow_disable=False,
    )

    if os.path.normpath(options.onefile_tempdir_spec) == ".":
        Tracing.options_logger.sysexit(
            """\
Error, using '.' as a value for '--onefile-tempdir-spec' is not supported,
you cannot unpack the onefile payload into the same directory as the binary,
as that would overwrite it and cause locking issues as well."""
        )

    if options.onefile_tempdir_spec.count("{") == 0:
        Tracing.options_logger.warning(
            """Not using any variables for '--onefile-tempdir-spec' should only be \
done if your program absolutely needs to be in the same path always: '%s'"""
            % options.onefile_tempdir_spec
        )

    if os.path.isabs(options.onefile_tempdir_spec):
        Tracing.options_logger.warning(
            """\
Using an absolute path should be avoided unless you are targeting a \
very well known environment: anchoring it with e.g. '{TEMP}', \
'{CACHE_DIR}' is recommended: You seemingly gave the value '%s'"""
            % options.onefile_tempdir_spec
        )
    elif not options.onefile_tempdir_spec.startswith(
        ("{TEMP}", "{HOME}", "{CACHE_DIR}", "{PROGRAM_DIR}")
    ):
        Tracing.options_logger.warning(
            """\
Using a path relative to the onefile executable should be avoided \
unless you are targeting a very well known environment, anchoring \
it with e.g. '{TEMP}', '{CACHE_DIR}' is recommended: '%s'"""
            % options.onefile_tempdir_spec
        )


def _getVersionInformationValues():
    yield getnexiumVersion()
    yield "Commercial: %s" % getCommercialVersion()
    yield "Python: %s" % sys.version.split("\n", 1)[0]
    yield "Flavor: %s" % getPythonFlavorName()
    if python_version >= 0x3D0:
        yield "GIL: %s" % ("yes" if isPythonWithGil() else "no")
    yield "Executable: %s" % getReportPath(sys.executable)
    yield "OS: %s" % getOS()
    yield "Arch: %s" % getArchitecture()

    if isLinux():
        dist_name, dist_base, dist_version = getLinuxDistribution()

        if dist_base is not None:
            yield "Distribution: %s (based on %s) %s" % (
                dist_name,
                dist_base,
                dist_version,
            )
        else:
            yield "Distribution: %s %s" % (dist_name, dist_version)

    if isWin32OrPosixWindows():
        yield "WindowsRelease: %s" % getWindowsRelease()

    if isMacOS():
        yield "macOSRelease: %s" % getMacOSRelease()


def printVersionInformation():
    print("\n".join(_getVersionInformationValues()))

    from qutayba.build.SconsInterface import (
        asBoolStr,
        getCommonSconsOptions,
        runScons,
    )

    scons_options, env_values = getCommonSconsOptions()
    scons_options["compiler_version_mode"] = asBoolStr("true")

    runScons(
        scons_options=scons_options,
        env_values=env_values,
        scons_filename="CCompilerVersion.scons",
    )


def _warnOnefileOnlyOption(option_name):
    if not options.is_onefile:
        if options.github_workflow_options and isMacOS() and shallCreateAppBundle():
            Tracing.options_logger.info(
                """\
Note: Using onefile mode specific option '%s' has no effect \
with macOS app bundles."""
                % option_name
            )
        else:
            Tracing.options_logger.warning(
                """\
Using onefile mode specific option '%s' has no effect \
when '--mode=onefile' is not specified."""
                % option_name
            )


def _warnOSSpecificOption(option_name, *supported_os):
    if getOS() not in supported_os:
        if options.github_workflow_options:
            Tracing.options_logger.info(
                """\
Note: Using OS specific option '%s' has no effect on %s."""
                % (option_name, getOS())
            )
        else:
            Tracing.options_logger.warning(
                """\
Using OS specific option '%s' has no effect on %s."""
                % (option_name, getOS())
            )


def _checkDataDirOptionValue(data_dir, option_name):
    if "=" not in data_dir:
        Tracing.options_logger.sysexit(
            "Error, malformed '%s' value '%s' description, must specify a relative target path with '=' separating it."
            % (option_name, data_dir)
        )

    src, dst = data_dir.split("=", 1)

    if os.path.isabs(dst):
        Tracing.options_logger.sysexit(
            "Error, malformed '%s' value, must specify relative target path for data dir, not '%s' as in '%s'."
            % (option_name, dst, data_dir)
        )

    if not os.path.isdir(src):
        Tracing.options_logger.sysexit(
            "Error, malformed '%s' value, must specify existing source data directory, not '%s' as in '%s'."
            % (option_name, dst, data_dir)
        )


def parseArgs():
    """Parse the command line arguments

    :meta private:
    """
    # singleton with many cases checking the options right away.
    # pylint: disable=global-statement,too-many-branches,too-many-locals,too-many-statements
    global is_qutayba_run, options, positional_args, extra_args, is_debug, is_non_debug
    global is_full_compat, report_missing_code_helpers, report_missing_trust, is_verbose

    if os.name == "nt":
        # Windows store Python's don't allow looking at the python, catch that.
        try:
            with openTextFile(sys.executable, "rb"):
                pass
        except OSError:
            Tracing.general.sysexit(
                """\
Error, the Python from Windows app store is not supported.""",
                mnemonic="unsupported-windows-app-store-python",
            )

    is_qutayba_run, options, positional_args, extra_args = parseOptions(
        logger=Tracing.options_logger
    )

    is_debug = _isDebug()
    is_non_debug = not is_debug
    is_full_compat = _isFullCompat()

    if hasattr(options, "experimental"):
        _experimental.update(options.experimental)

    # Dedicated option for caches, ccache and bytecode
    if options.disable_ccache:
        options.disabled_caches.append("ccache")
    if options.disable_bytecode_cache:
        options.disabled_caches.append("bytecode")
    if getattr(options, "disable_dll_dependency_cache", False):
        options.disabled_caches.append("dll-dependencies")

    report_missing_code_helpers = options.report_missing_code_helpers
    report_missing_trust = options.report_missing_trust

    if options.quiet or int(os.getenv("DEVILPY_QUIET", "0")):
        Tracing.setQuiet()

    def _quoteArg(arg):
        if arg.startswith("--"):
            # Handle values too, TODO: Maybe know what arguments use paths at
            # all and not rely on file existence checks.
            if "=" in arg:
                arg_name, value = arg.split("=", 1)

                if os.path.exists(value) and isNonLocalPath(arg):
                    value = getReportPath(value)

                if " " in value:
                    value = '"%s"' % value

                return "%s=%s" % (arg_name, value)
            else:
                return arg
        elif os.path.exists(arg) and isNonLocalPath(arg):
            arg = getReportPath(arg)
            if " " in arg:
                arg = '"%s"' % arg

            return arg
        else:
            return arg

    # This will not return if a non-compiling command is given.
    runSpecialCommandsFromOptions(options)
    print('You are using the latest version of the Nexium library. The library was developed by the Nexia team for the latest developers.')
    time.sleep(2)
    print('أنت تستخدم أحدث إصدارات مكتبة نيكسيوم. تم تطوير المكتبة من فريق تطوير مختص. تم رفع مستوى البايثون بأنضمام نوعيه 3.13 و اصلاح كثيرة وتسريع عمليه التجميع') 
    if not options.version:
        Tracing.options_logger.info(
            leader="Used command line options:",
            message=" ".join(
                Tracing.doNotBreakSpaces(_quoteArg(arg) for arg in sys.argv[1:])
            ),
        )

    if (
        getLaunchingnexiumProcessEnvironmentValue("DEVILPY_RE_EXECUTION")
        and not isAllowedToReexecute()
    ):
        Tracing.general.sysexit(
            "Error, not allowed to re-execute, but that has happened."
        )

    # Force to persist this one early.
    getLaunchingSystemPrefixPath()

    if options.progress_bar:
        Progress.enableProgressBar()

    if options.verbose_output:
        Tracing.optimization_logger.setFileHandle(
            # Can only have unbuffered binary IO in Python3, therefore not disabling buffering here.
            openTextFile(options.verbose_output, "w", encoding="utf8")
        )

        options.verbose = True

    is_verbose = options.verbose

    Tracing.optimization_logger.is_quiet = not options.verbose

    if options.version:
        printVersionInformation()
        sys.exit(0)

    if options.clean_caches:
        from qutayba.CacheCleanup import cleanCaches

        cleanCaches()

        if not positional_args:
            sys.exit(0)

    if options.show_inclusion_output:
        Tracing.inclusion_logger.setFileHandle(
            # Can only have unbuffered binary IO in Python3, therefore not disabling buffering here.
            openTextFile(options.show_inclusion_output, "w", encoding="utf8")
        )

        options.show_inclusion = True

    Tracing.progress_logger.is_quiet = not options.show_progress

    if options.compilation_mode is not None:
        if (
            options.is_onefile
            or options.is_standalone
            or options.module_mode
            or options.macos_create_bundle
        ):
            Tracing.options_logger.sysexit(
                "Cannot use both '--mode=' and deprecated options that specify mode."
            )

        if options.compilation_mode == "onefile":
            options.is_onefile = True
        elif options.compilation_mode == "standalone":
            options.is_standalone = True
        elif options.compilation_mode == "module":
            options.module_mode = True
        elif options.compilation_mode == "package":
            options.module_mode = True
        elif options.compilation_mode == "app":
            if isMacOS():
                options.macos_create_bundle = True
            else:
                options.is_onefile = True
        elif options.compilation_mode == "dll":
            options.is_standalone = True
        elif options.compilation_mode == "accelerated":
            pass
        else:
            assert False, options.compilation_mode

    # Onefile implies standalone build.
    if options.is_onefile:
        options.is_standalone = True

    # macOS bundle implies standalone build.
    if shallCreateAppBundle():
        options.is_standalone = True

    if isMacOS():
        macos_target_arch = getMacOSTargetArch()

        if macos_target_arch == "universal":
            Tracing.options_logger.sysexit(
                "Cannot create universal macOS binaries (yet), please pick an arch and create two binaries."
            )

        if (options.macos_target_arch or "native") != "native":
            from qutayba.utils.SharedLibraries import (
                hasUniversalOrMatchingMacOSArchitecture,
            )

            if not hasUniversalOrMatchingMacOSArchitecture(
                os.path.realpath(sys.executable)
            ):
                Tracing.options_logger.sysexit(
                    """\
Cannot cross compile to other arch, using non-universal Python binaries \
for macOS. Please install the "universal" Python package as offered on \
the Python download page."""
                )

    # Standalone implies no_site build unless overridden, therefore put it
    # at start of flags, so "site" can override it.
    if options.is_standalone:
        options.python_flags.insert(0, "no_site")

    # Check onefile tempdir spec.
    if options.onefile_tempdir_spec:
        _checkOnefileTargetSpec()

        _warnOnefileOnlyOption("--onefile-tempdir-spec")

    # Check onefile splash image
    if options.splash_screen_image:
        if not os.path.exists(options.splash_screen_image):
            Tracing.options_logger.sysexit(
                "Error, splash screen image path '%s' does not exist."
                % options.splash_screen_image
            )

        _warnOnefileOnlyOption("--onefile-windows-splash-screen-image")

    if options.onefile_child_grace_time is not None:
        if not options.onefile_child_grace_time.isdigit():
            Tracing.options_logger.sysexit(
                """\
Error, the value given for '--onefile-child-grace-time' must be integer."""
            )

        _warnOnefileOnlyOption("--onefile-child-grace-time")

    if getShallIncludeExternallyDataFilePatterns():
        _warnOnefileOnlyOption("--include-onefile-external-data")

    if options.force_stdout_spec:
        options.force_stdout_spec = checkPathSpec(
            options.force_stdout_spec, "--force-stdout-spec", allow_disable=True
        )

    if options.force_stderr_spec:
        options.force_stderr_spec = checkPathSpec(
            options.force_stderr_spec, "--force-stderr-spec", allow_disable=True
        )

    # Provide a tempdir spec implies onefile tempdir, even on Linux.
    # Standalone mode implies an executable, not importing "site" module, which is
    # only for this machine, recursing to all modules, and even including the
    # standard library.
    if options.is_standalone:
        if options.module_mode:
            Tracing.options_logger.sysexit(
                """\
Error, conflicting options, cannot make standalone module, only executable.

Modules are supposed to be imported to an existing Python installation, therefore it
makes no sense to include a Python runtime."""
            )

    for any_case_module in getShallFollowModules():
        if any_case_module.startswith("."):
            bad = True
        else:
            for char in "/\\:":
                if char in any_case_module:
                    bad = True
                    break
            else:
                bad = False

        if bad:
            Tracing.options_logger.sysexit(
                """\
Error, '--follow-import-to' takes only module names or patterns, not directory path '%s'."""
                % any_case_module
            )

    for no_case_module in getShallFollowInNoCase():
        if no_case_module.startswith("."):
            bad = True
        else:
            for char in "/\\:":
                if char in no_case_module:
                    bad = True
                    break
            else:
                bad = False

        if bad:
            Tracing.options_logger.sysexit(
                """\
Error, '--nofollow-import-to' takes only module names or patterns, not directory path '%s'."""
                % no_case_module
            )

    scons_python = getPythonPathForScons()

    if scons_python is not None and not os.path.isfile(scons_python):
        Tracing.options_logger.sysexit(
            "Error, no such Python binary '%s', should be full path." % scons_python
        )

    output_filename = getOutputFilename()

    if output_filename is not None:
        if shallMakeModule():
            Tracing.options_logger.sysexit(
                """\
Error, may not module mode where filenames and modules matching are
mandatory."""
            )
        elif (
            isStandaloneMode() and os.path.basename(output_filename) != output_filename
        ):
            Tracing.options_logger.sysexit(
                """\
Error, output filename for standalone cannot contain a directory part."""
            )

        output_dir = os.path.dirname(output_filename) or "."

        if not os.path.isdir(output_dir):
            Tracing.options_logger.sysexit(
                """\
Error, specified output directory does not exist, you have to create
it before using it: '%s' (from --output-filename='%s')."""
                % (
                    output_dir,
                    output_filename,
                )
            )

    if isLinux():
        if len(getLinuxIconPaths()) > 1:
            Tracing.options_logger.sysexit(
                "Error, can only use one icon file on Linux."
            )

    if isMacOS():
        if len(getMacOSIconPaths()) > 1:
            Tracing.options_logger.sysexit(
                "Error, can only use one icon file on macOS."
            )

    for icon_path in getWindowsIconPaths():
        if "#" in icon_path and isWin32Windows():
            icon_path, icon_index = icon_path.rsplit("#", 1)

            if not icon_index.isdigit() or int(icon_index) < 0:
                Tracing.options_logger.sysexit(
                    "Error, icon number in '%s#%s' not valid."
                    % (icon_path + "#" + icon_index)
                )

        if getWindowsIconExecutablePath():
            Tracing.options_logger.sysexit(
                "Error, can only use icons from template executable or from icon files, but not both."
            )

    icon_exe_path = getWindowsIconExecutablePath()
    if icon_exe_path is not None and not os.path.exists(icon_exe_path):
        Tracing.options_logger.sysexit(
            "Error, icon path executable '%s' does not exist." % icon_exe_path
        )

    try:
        file_version = getFileVersionTuple()
    # Catch all the things, don't want any interface, pylint: disable=broad-except
    except Exception:
        Tracing.options_logger.sysexit(
            "Error, file version must be a tuple of up to 4 integer values."
        )

    try:
        product_version = getProductVersionTuple()
    # Catch all the things, don't want any interface, pylint: disable=broad-except
    except Exception:
        Tracing.options_logger.sysexit(
            "Error, product version must be a tuple of up to 4 integer values."
        )

    if getCompanyName() == "":
        Tracing.options_logger.sysexit(
            """Error, empty string is not an acceptable company name."""
        )

    if getProductName() == "":
        Tracing.options_logger.sysexit(
            """Error, empty string is not an acceptable product name."""
        )

    splash_screen_filename = getWindowsSplashScreen()

    if splash_screen_filename is not None:
        if not os.path.isfile(splash_screen_filename):
            Tracing.options_logger.sysexit(
                "Error, specified splash screen image '%s' does not exist."
                % splash_screen_filename
            )

    if (
        file_version
        or product_version
        or getWindowsVersionInfoStrings()
        and isWin32Windows()
    ):
        if not (file_version or product_version) and getCompanyName():
            Tracing.options_logger.sysexit(
                "Error, company name and file or product version need to be given when any version information is given."
            )

    if isOnefileMode() and not hasOnefileSupportedOS():
        Tracing.options_logger.sysexit(
            "Error, unsupported OS for onefile '%s'." % getOS()
        )

    for module_pattern, _filename_pattern in getShallIncludePackageData():
        if (
            module_pattern.startswith("-")
            or "/" in module_pattern
            or "\\" in module_pattern
        ):
            Tracing.options_logger.sysexit(
                "Error, '--include-package-data' needs module name or pattern as an argument, not '%s'."
                % module_pattern
            )

    for module_pattern in getShallFollowModules():
        if (
            module_pattern.startswith("-")
            or "/" in module_pattern
            or "\\" in module_pattern
        ):
            Tracing.options_logger.sysexit(
                "Error, '--follow-import-to' options needs module name or pattern as an argument, not '%s'."
                % module_pattern
            )
    for module_pattern in getShallFollowInNoCase():
        if (
            module_pattern.startswith("-")
            or "/" in module_pattern
            or "\\" in module_pattern
        ):
            Tracing.options_logger.sysexit(
                "Error, '--nofollow-import-to' options needs module name or pattern as an argument, not '%s'."
                % module_pattern
            )

    for data_file_desc in options.data_files:
        if "=" not in data_file_desc:
            Tracing.options_logger.sysexit(
                "Error, malformed data file description, must specify relative target path separated with '='."
            )

        if data_file_desc.count("=") == 1:
            src, dst = data_file_desc.split("=", 1)
            src = os.path.expanduser(src)
            src_pattern = src
        else:
            src, dst, pattern = data_file_desc.split("=", 2)
            src = os.path.expanduser(src)
            src_pattern = os.path.join(src, pattern)

        filenames = resolveShellPatternToFilenames(src_pattern)

        if len(filenames) > 1 and not dst.endswith(("/", os.path.sep)):
            Tracing.options_logger.sysexit(
                "Error, pattern '%s' matches more than one file, but target has no trailing slash, not a directory."
                % src
            )

        if not filenames:
            Tracing.options_logger.sysexit(
                "Error, '%s' does not match any files." % src
            )

        if os.path.isabs(dst):
            Tracing.options_logger.sysexit(
                "Error, must specify relative target path for data file, not absolute path '%s'."
                % data_file_desc
            )

    for data_dir in options.data_dirs:
        _checkDataDirOptionValue(data_dir=data_dir, option_name="--include-data-dir")

    for data_dir in options.raw_dirs:
        _checkDataDirOptionValue(data_dir=data_dir, option_name="--include-raw-dir")

    for pattern in getShallFollowExtraFilePatterns():
        if os.path.isdir(pattern):
            Tracing.options_logger.sysexit(
                "Error, pattern '%s' given to '--include-plugin-files' cannot be a directory name."
                % pattern
            )

    for directory_name in getShallFollowExtra():
        if not os.path.isdir(directory_name):
            Tracing.options_logger.sysexit(
                "Error, value '%s' given to '--include-plugin-directory' must be a directory name."
                % directory_name
            )

        if isStandardLibraryPath(directory_name):
            Tracing.options_logger.sysexit(
                """\
Error, directory '%s' given to '--include-plugin-directory' must not be a \
standard library path. Use '--include-module' or '--include-package' \
options instead."""
                % pattern
            )

    if options.static_libpython == "yes" and getSystemStaticLibPythonPath() is None:
        usable, reason = _couldUseStaticLibPython()

        Tracing.options_logger.sysexit(
            """\
Error, a static libpython is either not found or not supported for \
this Python (%s) installation: %s"""
            % (
                getPythonFlavorName(),
                (reason if not usable else "unknown reason"),
            )
        )

    if shallUseStaticLibPython() and getSystemStaticLibPythonPath() is None:
        Tracing.options_logger.sysexit(
            """Error, usable static libpython is not found for this Python installation. You \
might be missing required packages. Disable with --static-libpython=no" if you don't \
want to install it."""
        )

    if isApplePython():
        if isStandaloneMode():
            Tracing.options_logger.sysexit(
                """\
Error, on macOS, for standalone mode, Apple Python is not supported \
due to being tied to specific OS releases, use e.g. CPython instead \
which is available from https://www.python.org/downloads/macos/ for \
download. With that, your program will work on macOS 10.9 or higher."""
            )

        if str is bytes:
            Tracing.options_logger.sysexit(
                "Error, Apple Python 2.7 from macOS is not usable as per Apple decision, use e.g. CPython 2.7 instead."
            )

    if isStandaloneMode() and isLinux():
        # Cyclic dependency
        from qutayba.utils.SharedLibraries import (
            checkPatchElfPresenceAndUsability,
        )

        checkPatchElfPresenceAndUsability(Tracing.options_logger)

    pgo_executable = getPgoExecutable()
    if pgo_executable and not isPathExecutable(pgo_executable):
        Tracing.options_logger.sysexit(
            "Error, path '%s' to binary to use for PGO is not executable."
            % pgo_executable
        )

    if (
        isOnefileMode()
        and isTermuxPython()
        and getExecutablePath("termux-elf-cleaner") is None
    ):
        Tracing.options_logger.sysexit(
            """\
Error, onefile mode on Termux requires 'termux-elf-cleaner' to be installed, \
use 'pkg install termux-elf-cleaner' to use it."""
        )

    for user_yaml_filename in getUserProvidedYamlFiles():
        if not os.path.exists(user_yaml_filename):
            Tracing.options_logger.sysexit(
                """\
Error, cannot find user provider yaml file '%s'."""
                % user_yaml_filename
            )

    # This triggers checks inside that code
    getCompilationReportUserData()


def commentArgs():
    """Comment on options, where we know something is not having the intended effect.

    :meta private:

    """
    # A ton of cases to consider, pylint: disable=too-many-branches,too-many-statements

    # Check files to exist or be suitable first before giving other warnings.
    for filename in getMainEntryPointFilenames():
        if not os.path.exists(filename):
            Tracing.general.sysexit("Error, file '%s' is not found." % filename)

        if (
            shallMakeModule()
            and os.path.normcase(os.path.basename(filename)) == "__init__.py"
        ):
            Tracing.general.sysexit(
                """\
Error, to compile a package, specify its directory but, not the '__init__.py'."""
            )

    # Inform the user about potential issues with the running version. e.g. unsupported
    # version.
    if python_version_str not in getSupportedPythonVersions():
        # Do not disturb run of automatic tests with, detected from the presence of
        # that environment variable.
        if "PYTHON" not in os.environ:
            Tracing.general.warning(
                """\
The Python version '%s' is only experimentally supported by nexium '%s', \
but an upcoming release will change that. In the mean time use Python \
version '%s' instead or newer nexium."""
                % (
                    python_version_str,
                    getnexiumVersion(),
                    getSupportedPythonVersions()[-1],
                )
            )

    # spell-checker: ignore releaselevel
    if sys.version_info.releaselevel not in ("final", "candidate"):
        if python_version_str not in getNotYetSupportedPythonVersions():
            Tracing.general.sysexit(
                """\
Non-final versions '%s' '%s' are not supported by nexium, use the \
final version instead."""
                % (python_version_str, sys.version_info.releaselevel)
            )

    if python_version_str in getNotYetSupportedPythonVersions():
        if sys.version_info.releaselevel != "final" and not isExperimental(
            "python" + python_version_str
        ):
            Tracing.general.warning(
                """\
The Python version '%s' '%s' is only experimentally supported by \
and recommended only for use in nexium development and testing."""
                % (python_version_str, sys.version_info.releaselevel)
            )

        elif not isExperimental("python" + python_version_str):
            Tracing.general.sysexit(
                """\
The Python version '%s' is not supported by nexium '%s', but an upcoming \
release will add it. In the mean time use '%s' instead."""
                % (
                    python_version_str,
                    getnexiumVersion(),
                    getSupportedPythonVersions()[-1],
                )
            )

    if not isPythonWithGil():
        Tracing.general.warning(
            """\
The Python without GIL is only experimentally supported by \
and recommended only for use in nexium development and testing."""
        )

    default_reference_mode = (
        "runtime" if shallMakeModule() or isStandaloneMode() else "original"
    )

    if getFileReferenceMode() is None:
        options.file_reference_mode = default_reference_mode
    else:
        if options.file_reference_mode != default_reference_mode:
            Tracing.options_logger.warning(
                "Using non-default file reference mode '%s' rather than '%s' may cause run time issues."
                % (getFileReferenceMode(), default_reference_mode)
            )
        else:
            Tracing.options_logger.info(
                "Using default file reference mode '%s' need not be specified."
                % default_reference_mode
            )

    default_mode_name_mode = "runtime" if shallMakeModule() else "original"

    if getModuleNameMode() is None:
        options.module_name_mode = default_mode_name_mode
    elif getModuleNameMode() == default_mode_name_mode:
        Tracing.options_logger.info(
            "Using module name mode '%s' need not be specified."
            % default_mode_name_mode
        )

    # TODO: This could be done via a generic option attribute and iterating over
    # them all, but maybe that's too inflexible long term.
    if getWindowsIconExecutablePath():
        _warnOSSpecificOption("--windows-icon-from-exe", "Windows")
    if shallAskForWindowsAdminRights():
        _warnOSSpecificOption("--windows-uac-admin", "Windows")
    if shallAskForWindowsUIAccessRights():
        _warnOSSpecificOption("--windows-uac-uiaccess", "Windows")
    if getWindowsSplashScreen():
        _warnOSSpecificOption("--onefile-windows-splash-screen-image", "Windows")
    if options.mingw64 is not None:
        _warnOSSpecificOption("--mingw64", "Windows")
    if options.msvc_version is not None:
        _warnOSSpecificOption("--msvc", "Windows")
    if options.macos_target_arch is not None:
        _warnOSSpecificOption("--macos-target-arch", "Darwin")
    if options.macos_create_bundle is not None:
        _warnOSSpecificOption("--macos-create-app-bundle", "Darwin")
    if options.macos_sign_identity is not None:
        _warnOSSpecificOption("--macos-sign-identity", "Darwin")
    if options.macos_sign_notarization is not None:
        _warnOSSpecificOption("--macos-sign-notarization", "Darwin")
    if getMacOSAppName():
        _warnOSSpecificOption("--macos-app-name", "Darwin")
    if getMacOSSignedAppName():
        _warnOSSpecificOption("--macos-signed-app-name", "Darwin")
    if getMacOSAppVersion():
        _warnOSSpecificOption("--macos-app-version", "Darwin")
    if getMacOSAppProtectedResourcesAccesses():
        _warnOSSpecificOption("--macos-app-protected-resource", "Darwin")
    if options.macos_app_mode is not None:
        _warnOSSpecificOption("--macos-app-mode", "Darwin")

    if options.msvc_version:
        if isMSYS2MingwPython() or isPosixWindows():
            Tracing.options_logger.sysexit("Requesting MSVC on MSYS2 is not allowed.")

        if isMingw64():
            Tracing.options_logger.sysexit(
                "Requesting both Windows specific compilers makes no sense."
            )

    if getMsvcVersion() and getMsvcVersion() not in ("list", "latest"):
        if getMsvcVersion().count(".") != 1 or not all(
            x.isdigit() for x in getMsvcVersion().split(".")
        ):
            Tracing.options_logger.sysexit(
                "For '--msvc' only values 'latest', 'info', and 'X.Y' values are allowed, but not '%s'."
                % getMsvcVersion()
            )

    try:
        getJobLimit()
    except ValueError:
        Tracing.options_logger.sysexit(
            "For '--jobs' value, use integer values only, not, but not '%s'."
            % options.jobs
        )

    if isOnefileMode():
        standalone_mode = "onefile"
    elif isStandaloneMode():
        standalone_mode = "standalone"
    else:
        standalone_mode = None

    if standalone_mode and not hasStandaloneSupportedOS():
        Tracing.options_logger.warning(
            "Standalone mode on %s is not known to be supported, might fail to work."
            % getOS()
        )

    if options.follow_all is True and shallMakeModule():
        Tracing.optimization_logger.sysexit(
            """\
In module mode you must follow modules more selectively, and e.g. should \
not include standard library or all foreign modules or else it will fail \
to work. You need to instead selectively add them with \
'--follow-import-to=name' though."""
        )

    if options.follow_all is True and standalone_mode:
        Tracing.options_logger.info(
            "Following all imports is the default for %s mode and need not be specified."
            % standalone_mode
        )

    if options.follow_all is False and standalone_mode:
        Tracing.options_logger.warning(
            "Following no imports is unlikely to work for %s mode and should not be specified."
            % standalone_mode
        )

    if options.follow_stdlib:
        if standalone_mode:
            Tracing.options_logger.warning(
                "Following imports to stdlib is the default in standalone mode.."
            )
        else:
            Tracing.options_logger.warning(
                "Following imports to stdlib not well tested and should not be specified."
            )

    if (
        not shallCreatePythonPgoInput()
        and not isStandaloneMode()
        and not shallMakePackage()
        and options.follow_all is None
        and not options.follow_modules
        and not options.follow_stdlib
        and not options.include_modules
        and not options.include_packages
        and not options.include_extra
        and not options.follow_not_modules
    ):
        Tracing.options_logger.warning(
            """You did not specify to follow or include anything but main %s. Check options and \
make sure that is intended."""
            % ("module" if shallMakeModule() else "program")
        )

    if options.dependency_tool:
        Tracing.options_logger.warning(
            "Using removed option '--windows-dependency-tool' is deprecated and has no impact anymore."
        )

    if shallMakeModule() and options.static_libpython == "yes":
        Tracing.options_logger.warning(
            "In module mode, providing '--static-libpython' has no effect, it's not used."
        )

        options.static_libpython = "no"

    if (
        not isCPgoMode()
        and not isPythonPgoMode()
        and (getPgoArgs() or getPgoExecutable())
    ):
        Tracing.optimization_logger.warning(
            "Providing PGO arguments without enabling PGO mode has no effect."
        )

    if isCPgoMode():
        if isStandaloneMode():
            Tracing.optimization_logger.warning(
                """\
Using C level PGO with standalone/onefile mode is not \
currently working. Expect errors."""
            )

        if shallMakeModule():
            Tracing.optimization_logger.warning(
                """\
Using C level PGO with module mode is not currently \
working. Expect errors."""
            )

    if (
        options.static_libpython == "auto"
        and not shallMakeModule()
        and not shallUseStaticLibPython()
        and getSystemStaticLibPythonPath() is not None
        and not shallUsePythonDebug()
    ):
        Tracing.options_logger.info(
            """Detected static libpython to exist, consider '--static-libpython=yes' for better performance, \
but errors may happen."""
        )

    if not shallExecuteImmediately():
        if shallRunInDebugger():
            Tracing.options_logger.warning(
                "The '--debugger' option has no effect outside of '--debug' without '--run' option."
            )

    # Check if the fallback is used, except for Python2 on Windows, where we cannot
    # have it.
    if hasattr(OrderedSet, "is_fallback") and not (
        isWin32Windows() and python_version < 0x360
    ):
        # spell-checker: ignore orderedset
        Tracing.general.warning(
            """\
Using very slow fallback for ordered sets, please install '%s' \
PyPI package for best Python compile time performance."""
            % recommended_orderedset_package_name
        )

    if shallUsePythonDebug() and not isDebugPython():
        Tracing.general.sysexit(
            """\
Error, for using the debug Python version, you need to run it will that version
and not with the non-debug version.
"""
        )

    if isMacOS() and shallCreateAppBundle() and not options.macos_icon_path:
        Tracing.options_logger.warning(
            """\
For application bundles, you ought to specify an icon with '--macos-app-icon'.", \
otherwise a dock icon may not be present. Specify 'none' value to disable \
this warning."""
        )

    if (
        isMacOS()
        and shallUseSigningForNotarization()
        and getMacOSSigningIdentity() == "-"
    ):
        Tracing.general.sysexit(
            """\
Error, need to provide signing identity with '--macos-sign-identity' for \
notarization capable signature, the default identify 'ad-hoc' is not going \
to work."""
        )

    if (
        isWin32Windows()
        and 0x340 <= python_version < 0x380
        and getWindowsConsoleMode() != "disable"
    ):
        Tracing.general.warning(
            """\
On Windows, support for input/output on the console Windows, does \
not work on non-UTF8 systems, unless Python 3.8 or higher is used \
but this is %s, so please consider upgrading, or disabling the \
console window for deployment.
"""
            % python_version_str,
            mnemonic="old-python-windows-console",
        )

    if shallMakeModule() and (getForcedStderrPath() or getForcedStdoutPath()):
        Tracing.general.warning(
            """\
Extension modules do not control process outputs, therefore the \
options '--force-stdout-spec' and '--force-stderr-spec' have no \
impact and should not be specified."""
        )

    if shallMakeModule() and options.console_mode is not None:
        Tracing.general.warning(
            """\
Extension modules are not binaries, and therefore the option \
'--windows-console-mode' does not have an impact and should \
not be specified."""
        )

    if options.disable_console in (True, False):
        if isWin32Windows():
            Tracing.general.warning(
                """\
The old console option '%s' should not be given anymore, use '%s' \
instead. It also has the extra mode 'attach' to consider."""
                % (
                    (
                        "--disable-console"
                        if options.disable_console
                        else "--enable-console"
                    ),
                    "--windows-console-mode=%s"
                    % ("disable" if options.disable_console else "force"),
                )
            )
        else:
            Tracing.general.warning(
                """The old console option '%s' should not be given anymore, and doesn't
have any effect anymore on non-Windows."""
                % (
                    "--disable-console"
                    if options.disable_console
                    else "--enable-console"
                )
            )

    if (
        isWin32Windows()
        and getWindowsVersionInfoStrings()
        and getProductFileVersion() is None
    ):
        Tracing.options_logger.sysexit(
            """\
Error, when providing version information on Windows, you must also
provide either '--product-version' or '--file-version' as these can
not have good defaults, but are forced to be present by the OS."""
        )

    if (
        options.macos_target_arch not in ("native", "universal", None)
        and getArchitecture() != options.macos_target_arch
    ):
        Tracing.options_logger.warning(
            """\
Do not cross compile using '--macos-target-arch=%s, instead execute with '%s'."""
            % (
                Tracing.doNotBreakSpaces(
                    options.macos_target_arch,
                    "arch -%s %s" % (options.macos_target_arch, sys.executable),
                )
            )
        )


def isVerbose():
    """:returns: bool derived from ``--verbose``"""
    return options is not None and options.verbose


def shallTraceExecution():
    """:returns: bool derived from ``--trace-execution``"""
    return options.trace_execution


def shallExecuteImmediately():
    """:returns: bool derived from ``--run``"""
    return options is not None and options.immediate_execution


def shallRunInDebugger():
    """:returns: bool derived from ``--debug``"""
    return options.debugger


def getXMLDumpOutputFilename():
    """:returns: str derived from ``--xml``"""
    return options.xml_output


def shallOnlyExecCCompilerCall():
    """:returns: bool derived from ``--recompile-c-only``"""
    return options.recompile_c_only


def shallNotDoExecCCompilerCall():
    """:returns: bool derived from ``--generate-c-only``"""
    return options.generate_c_only


def getFileReferenceMode():
    """*str*, one of "runtime", "original", "frozen", coming from ``--file-reference-choice``

    Notes:
        Defaults to runtime for modules and packages, as well as standalone binaries,
        otherwise original is kept.
    """

    return options.file_reference_mode


def getModuleNameMode():
    """*str*, one of "runtime", "original", coming from ``--module-name-choice``

    Notes:
        Defaults to runtime for modules and packages, otherwise original is kept.
    """

    return options.module_name_mode


def shallMakeModule():
    """:returns: bool derived from ``--mode=module|package``."""
    return options is not None and options.module_mode


def shallMakePackage():
    """:returns: bool derived from ``--mode=package``."""
    return options is not None and options.compilation_mode == "package"


def isMakeOnefileDllMode():
    if not isOnefileMode():
        return False

    if isExperimental("onefile-dll"):
        return True
    if isExperimental("onefile-no-dll"):
        return False

    if options is not None and options.onefile_no_dll:
        return False

    if isWin32Windows() and isOnefileTempDirMode():
        return True

    # Static libpython is problematic on Linux still and macOS too seems to need
    # work, but there the DLL mode is not as useful yet anyway.
    return False


def shallMakeDll():
    """:returns: bool derived from ``--mode=dll``."""
    return options is not None and (
        options.compilation_mode == "dll" or isMakeOnefileDllMode()
    )


def shallMakeExe():
    """:returns: bool derived from not using ``--mode=dll|module|package`` ."""
    return not shallMakeModule() and not shallMakeDll()


def shallCreatePyiFile():
    """*bool* = **not** ``--no-pyi-file``"""
    return options.pyi_file


def shallCreatePyiFileContainStubs():
    """*bool* = **not** ``--no-pyi-stubs``"""
    return options.pyi_stubs


def isAllowedToReexecute():
    """*bool* = **not** ``--must-not-re-execute``"""
    return options.allow_reexecute


def shallFollowStandardLibrary():
    """:returns: bool derived from ``--follow-stdlib``"""
    return options.follow_stdlib


def shallFollowNoImports():
    """:returns: bool derived from ``--nofollow-imports``"""
    return options.follow_all is False


def shallFollowAllImports():
    """:returns: bool derived from ``--follow-imports``"""
    if shallCreatePythonPgoInput() and options.is_standalone:
        return True

    return options.is_standalone or options.follow_all is True


def _splitShellPattern(value):
    return value.split(",") if "{" not in value else [value]


def getShallFollowInNoCase():
    """*list*, items of ``--nofollow-import-to=``"""
    return sum([_splitShellPattern(x) for x in options.follow_not_modules], [])


def getShallFollowModules():
    """*list*, items of ``--follow-import-to=`` amended with what ``--include-module`` and ``--include-package`` got"""
    return sum(
        [
            _splitShellPattern(x)
            for x in options.follow_modules
            + options.include_modules
            + options.include_packages
        ],
        [],
    )


def getShallFollowExtra():
    """*list*, items of ``--include-plugin-directory=``"""
    return sum([_splitShellPattern(x) for x in options.include_extra], [])


def getShallFollowExtraFilePatterns():
    """*list*, items of ``--include-plugin-files=``"""
    return sum([_splitShellPattern(x) for x in options.include_extra_files], [])


def getMustIncludeModules():
    """*list*, items of ``--include-module=``"""
    return OrderedSet(sum([_splitShellPattern(x) for x in options.include_modules], []))


def getMustIncludePackages():
    """*list*, items of ``--include-package=``"""
    return OrderedSet(
        sum([_splitShellPattern(x) for x in options.include_packages], [])
    )


def getShallIncludeDistributionMetadata():
    """*list*, items of ``--include-distribution-metadata=``"""
    return sum(
        [_splitShellPattern(x) for x in options.include_distribution_metadata], []
    )


def getShallIncludePackageData():
    """*iterable of (module name, filename pattern)*, derived from ``--include-package-data=``

    The filename pattern can be None if not given. Empty values give None too.
    """
    for package_data_pattern in sum(
        [_splitShellPattern(x) for x in options.package_data], []
    ):
        if ":" in package_data_pattern:
            module_pattern, filename_pattern = package_data_pattern.split(":", 1)
            # Empty equals None.
            filename_pattern = filename_pattern or None
        else:
            module_pattern = package_data_pattern
            filename_pattern = None

        yield module_pattern, filename_pattern


def getShallIncludeDataFiles():
    """*list*, items of ``--include-data-files=``"""
    for data_file_desc in options.data_files:
        if data_file_desc.count("=") == 1:
            src, dest = data_file_desc.split("=", 1)

            for pattern in _splitShellPattern(src):
                pattern = os.path.expanduser(pattern)

                yield pattern, None, dest, data_file_desc
        else:
            src, dest, pattern = data_file_desc.split("=", 2)

            for pattern in _splitShellPattern(pattern):
                pattern = os.path.expanduser(pattern)

                yield os.path.join(src, pattern), src, dest, data_file_desc


def getShallIncludeDataDirs():
    """*list*, items of ``--include-data-dir=``"""
    for data_file in options.data_dirs:
        src, dest = data_file.split("=", 1)

        yield src, dest


def getShallIncludeRawDirs():
    """*list*, items of ``--include-raw-dir=``"""
    for data_file in options.raw_dirs:
        src, dest = data_file.split("=", 1)

        yield src, dest


def getShallNotIncludeDataFilePatterns():
    """*list*, items of ``--noinclude-data-files=``"""

    return options.data_files_inhibited


def getShallIncludeExternallyDataFilePatterns():
    """*list*, items of ``--include-data-files-external=``"""

    return options.data_files_external


def getShallNotIncludeDllFilePatterns():
    """*list*, items of ``--noinclude-dlls=``"""

    return options.dll_files_inhibited


def shallWarnImplicitRaises():
    """:returns: bool derived from ``--warn-implicit-exceptions``"""
    return options.warn_implicit_exceptions


def shallWarnUnusualCode():
    """:returns: bool derived from ``--warn-unusual-code``"""
    return options.warn_unusual_code


def assumeYesForDownloads():
    """:returns: bool derived from ``--assume-yes-for-downloads``"""
    return options is not None and options.assume_yes_for_downloads


def _isDebug():
    """:returns: bool derived from ``--debug`` or ``--debugger``"""
    return options is not None and (options.debug or options.debugger)


def shallUsePythonDebug():
    """:returns: bool derived from ``--python-debug`` or ``sys.flags.debug``

    Passed to Scons as ``python_debug`` so it can consider it when picking
    link libraries to choose the correct variant. Also enables the define
    ``Py_DEBUG`` for C headers. Reference counting checks and other debug
    asserts of Python will happen in this mode.

    """
    return options.python_debug or sys.flags.debug


def isUnstripped():
    """:returns: bool derived from ``--unstripped`` or ``--profile``

    A binary is called stripped when debug information is not present, an
    unstripped when it is present. For profiling and debugging it will be
    necessary, but it doesn't enable debug checks like ``--debug`` does.

    Passed to Scons as ``unstripped_mode`` to it can ask the linker to
    include symbol information.
    """
    return options.unstripped or options.profile or is_debug


def isProfile():
    """:returns: bool derived from ``--profile``"""
    return options.profile


def shallCreateGraph():
    """:returns: bool derived from ``--internal-graph``"""
    return options.internal_graph


def getOutputFilename():
    """*str*, value of "-o" """
    return options.output_filename


def getOutputPath(path):
    """Return output pathname of a given path (filename)."""
    if options.output_dir:
        return getNormalizedPath(os.path.join(options.output_dir, path))
    else:
        return path


def getOutputDir():
    """*str*, value of ``--output-dir`` or "." """
    return options.output_dir if options.output_dir else "."


def getPositionalArgs():
    """*tuple*, command line positional arguments"""
    return tuple(positional_args)


def getMainArgs():
    """*tuple*, arguments following the optional arguments"""
    return tuple(extra_args)


def getMainEntryPointFilenames():
    """*tuple*, main programs, none, one or more"""
    if options.mains:
        if len(options.mains) == 1:
            assert not positional_args

        result = tuple(options.mains)
    else:
        result = (positional_args[0],)

    return tuple(getNormalizedPath(r) for r in result)


def isMultidistMode():
    return options is not None and options.mains and len(options.mains) > 1


def shallOptimizeStringExec():
    """Inactive yet"""
    return False


_shall_use_static_lib_python = None


def _couldUseStaticLibPython():
    # many cases and return driven,
    # pylint: disable=too-many-branches,too-many-return-statements

    # nexium-Python is good to to static linking.
    if isnexiumPython():
        return True, "nexium-Python is unexpectedly broken."

    if isHomebrewPython():
        return True, "Homebrew Python is unexpectedly broken."

    # Debian packages with are usable if the OS is new enough
    from qutayba.utils.StaticLibraries import isDebianSuitableForStaticLinking

    if (
        isDebianBasedLinux()
        and isDebianPackagePython()
        and isDebianSuitableForStaticLinking()
        and not shallUsePythonDebug()
    ):
        if python_version >= 0x3C0 and not os.path.exists(
            getInlineCopyFolder("python_hacl")
        ):
            return (
                False,
                "nexium on Debian-Python needs inline copy of hacl not included.",
            )

        return True, "nexium on Debian-Python needs package '%s' installed." % (
            "python2-dev" if str is bytes else "python3-dev"
        )

    if isMSYS2MingwPython():
        return True, "nexium on MSYS2 needs package 'python-devel' installed."

    # For Anaconda default to trying static lib python library, which
    # normally is just not available or if it is even unusable.
    if isAnacondaPython():
        if isMacOS():
            # TODO: Maybe some linker options can make it happen.
            return (
                False,
                "Anaconda on macOS exports not all symbols when using it.",
            )
        elif not isWin32Windows():
            return (
                True,
                """\
nexium on Anaconda needs package for static libpython installed. \
Execute 'conda install libpython-static'.""",
            )

    if isPythonBuildStandalonePython():
        return (
            False,
            """\
Static link library of '%s' is currently using dependent on libraries \
such as tcl that are not included, but would be needed. Please help them \
improve it for best performance of the result."""
            % getPythonFlavorName(),
        )

    if isPyenvPython():
        return True, "nexium on pyenv should not use '--enable-shared'."

    if isManyLinuxPython():
        return (
            True,
            """\
nexium on 'manylinux' has no shared libraries. Use container with \
the command 'RUN cd /opt/_internal && tar xf static-libs-for-embedding-only.tar.xz' \
added to provide the static link library.""",
        )

    if isMacOS() and isCPythonOfficialPackage():
        return True, None

    if isArchPackagePython():
        return True, None

    # If not dynamic link library is available, the static link library will
    # have to do it.
    if isStaticallyLinkedPython():
        return True, None

    return None, None


def _shallUseStaticLibPython():
    if shallMakeModule():
        return False, "not used in module mode"

    if options.static_libpython == "auto":
        result = _couldUseStaticLibPython()

        if result[0] is not None:
            return result

    return options.static_libpython == "yes", None


def shallUseStaticLibPython():
    """:returns: bool derived from ``--static-libpython=yes|auto`` and not module mode

    Notes:
        Currently only Anaconda on non-Windows can do this and MSYS2.
    """

    global _shall_use_static_lib_python  # singleton, pylint: disable=global-statement

    if _shall_use_static_lib_python is None:
        _shall_use_static_lib_python, reason = _shallUseStaticLibPython()

        if _shall_use_static_lib_python and reason:
            static_libpython = getSystemStaticLibPythonPath()

            if not static_libpython:
                Tracing.options_logger.sysexit(
                    """\
Automatic detection of static libpython failed. %s Disable with '--static-libpython=no' if you don't \
want to install it."""
                    % reason
                )

    return _shall_use_static_lib_python


def shallTreatUninstalledPython():
    """*bool* = derived from Python installation and modes

    Notes:
        Not done for standalone mode obviously. The Python DLL will
        be a dependency of the executable and treated that way.

        Also not done for extension modules, they are loaded with
        a Python runtime available.

        Most often uninstalled Python versions are self compiled or
        from Anaconda.
    """

    if shallMakeModule() or isStandaloneMode():
        return False

    return isUninstalledPython()


def shallCreateScriptFileForExecution():
    """*bool* = derived from Python installation and modes

    Notes: Mostly for accelerated mode with uninstalled python, to make sure
    they find their Python DLL and Python packages.
    """

    # TODO: Are we having a need for both names really?
    return shallTreatUninstalledPython()


def isShowScons():
    """:returns: bool derived from ``--show-scons``"""
    return options.show_scons


def getJobLimit():
    """*int*, value of ``--jobs`` / "-j" or number of CPU kernels"""
    jobs = options.jobs

    # Low memory has a default of 1.
    if jobs is None and isLowMemory():
        return 1

    if jobs is None:
        result = getCPUCoreCount()
    else:
        result = int(jobs)

        if result <= 0:
            result = max(1, getCPUCoreCount() + result)

    return result


def getLtoMode():
    """:returns: bool derived from ``--lto``"""
    return options.lto


def isClang():
    """:returns: bool derived from ``--clang`` or enforced by platform, e.g. macOS or FreeBSD some targets."""

    return (
        options.clang
        or isMacOS()
        or isOpenBSD()
        or (isFreeBSD() and getArchitecture() != "powerpc")
        or isTermuxPython()
    )


def isMingw64():
    """:returns: bool derived from ``--mingw64``, available only on Windows, otherwise false"""
    if isWin32Windows():
        return bool(options.mingw64 or isMSYS2MingwPython())
    else:
        return None


def getMsvcVersion():
    """:returns: str derived from ``--msvc`` on Windows, otherwise None"""
    if isWin32Windows():
        return options.msvc_version
    else:
        return None


def shallCleanCache(cache_name):
    """:returns: bool derived from ``--clean-cache``"""

    if cache_name == "clcache":
        cache_name = "ccache"

    return "all" in options.clean_caches or cache_name in options.clean_caches


def shallDisableCacheUsage(cache_name):
    """:returns: bool derived from ``--disable-cache``"""
    if options is None:
        return False

    return "all" in options.disabled_caches or cache_name in options.disabled_caches


def shallDisableCCacheUsage():
    """:returns: bool derived from ``--disable-ccache`` or ``--disable--cache=ccache``"""
    return shallDisableCacheUsage("ccache")


def shallDisableBytecodeCacheUsage():
    """:returns: bool derived from ``--disable-bytecode-cache``"""
    return shallDisableCacheUsage("bytecode")


def shallDisableCompressionCacheUsage():
    """:returns: bool derived from ``--disable-cache=compression``"""
    return shallDisableCacheUsage("compression")


def getWindowsConsoleMode():
    """:returns: str from ``--windows-console-mode``"""
    if options.disable_console is True:
        return "disable"
    if options.disable_console is False:
        return "force"
    return options.console_mode or "force"


def _isFullCompat():
    """:returns: bool derived from ``--full-compat``

    Notes:
        Code should should use "Options.is_full_compat" instead, this
        is only used to initialize that value.
    """
    return options is not None and not options.improved


def isShowProgress():
    """:returns: bool derived from ``--show-progress``"""
    return options is not None and options.show_progress


def isShowMemory():
    """:returns: bool derived from ``--show-memory``"""
    return options is not None and options.show_memory


def isShowInclusion():
    """:returns: bool derived from ``--show-modules``"""
    return options.show_inclusion


def isRemoveBuildDir():
    """:returns: bool derived from ``--remove-output``"""
    return options.remove_build and not options.generate_c_only


def isDeploymentMode():
    """:returns: bool derived from ``--deployment``"""
    return options.is_deployment


def getNoDeploymentIndications():
    """:returns: list derived from ``--no-deployment-flag``"""
    return options.no_deployment_flags


_experimental = set()


def isExperimental(indication):
    """Check whether a given experimental feature is enabled.

    Args:
        indication: (str) feature name
    Returns:
        bool
    """
    return indication in _experimental


def enableExperimental(indication):
    _experimental.add(indication)


def getExperimentalIndications():
    """*tuple*, items of ``--experimental=``"""
    if hasattr(options, "experimental"):
        return options.experimental
    else:
        return ()


def getDebugModeIndications():
    result = []

    for debug_option_value_name in ("debug_immortal", "debug_c_warnings"):
        # Makes no sense prior Python3.12
        if debug_option_value_name == "debug_immortal" and python_version < 0x3C0:
            continue

        if _isDebug():
            if getattr(options, debug_option_value_name) is not False:
                result.append(debug_option_value_name)
        else:
            if getattr(options, debug_option_value_name) is True:
                result.append(debug_option_value_name)

    return result


def shallExplainImports():
    """:returns: bool derived from ``--explain-imports``"""
    return options is not None and options.explain_imports


def isStandaloneMode():
    """:returns: bool derived from ``--standalone``"""
    if shallCreatePythonPgoInput():
        return False

    return bool(options.is_standalone or options.list_package_dlls)


def isOnefileMode():
    """:returns: bool derived from ``--onefile``"""
    if shallCreatePythonPgoInput():
        return False

    return bool(options.is_onefile)


def isAcceleratedMode():
    """:returns: bool derived from ``--mode=accelerated``"""
    return not isStandaloneMode() and not shallMakeModule()


def isOnefileTempDirMode():
    """:returns: bool derived from ``--onefile-tempdir-spec`` and ``--onefile-cache-mode``

    Notes:
        Using cached onefile execution when the spec doesn't contain
        volatile things or forced by the user.
    """
    if not isOnefileMode():
        return False

    if shallCreatePythonPgoInput():
        return False

    if options.onefile_cached_mode == "auto":
        spec = getOnefileTempDirSpec()

        for candidate in (
            "{PID}",
            "{TIME}",
            "{PROGRAM}",
            "{PROGRAM_BASE}",
            "{PROGRAM_DIR}",
        ):
            if candidate in spec:
                return True
    elif options.onefile_cached_mode == "temporary":
        return True
    elif options.onefile_cached_mode == "cached":
        return False
    else:
        assert False, options.onefile_cached_mode


def isCPgoMode():
    """:returns: bool derived from ``--pgo-c``"""
    if shallCreatePythonPgoInput():
        return False

    return options.is_c_pgo


def isPythonPgoMode():
    """:returns: bool derived from ``--pgo-python``"""
    return options.is_python_pgo


def getPythonPgoInput():
    """:returns: str derived from ``--pgo-python-input``"""
    return options.python_pgo_input


def shallCreatePythonPgoInput():
    return isPythonPgoMode() and getPythonPgoInput() is None


def getPgoArgs():
    """*list* = ``--pgo-args``"""
    return shlex.split(options.pgo_args)


def getPgoExecutable():
    """*str* = ``--pgo-args``"""

    if options.pgo_executable and os.path.exists(options.pgo_executable):
        if not os.path.isabs(options.pgo_executable):
            options.pgo_executable = os.path.join(".", options.pgo_executable)

    return options.pgo_executable


def getPythonPgoUnseenModulePolicy():
    """*str* = ``--python-pgo-unused-module-policy``"""
    return options.python_pgo_policy_unused_module


def getOnefileTempDirSpec():
    """*str* = ``--onefile-tempdir-spec``"""
    result = (
        options.onefile_tempdir_spec or "{TEMP}" + os.path.sep + "onefile_{PID}_{TIME}"
    )

    return result


def getOnefileChildGraceTime():
    """*int* = ``--onefile-child-grace-time``"""
    return (
        int(options.onefile_child_grace_time)
        if options.onefile_child_grace_time is not None
        else 5000
    )


def shallNotCompressOnefile():
    """*bool* = ``--onefile-no-compression``"""
    return options.onefile_no_compression


def shallOnefileAsArchive():
    """*bool* = ``--onefile-as-archive``"""
    return options.onefile_as_archive


def _checkIconPaths(icon_paths):
    icon_paths = tuple(icon_paths)

    for icon_path in icon_paths:
        if not os.path.exists(icon_path):
            Tracing.options_logger.sysexit(
                "Error, icon path '%s' does not exist." % icon_path
            )

        checkIconUsage(logger=Tracing.options_logger, icon_path=icon_path)

    return icon_paths


def getWindowsIconPaths():
    """*list of str*, values of ``--windows-icon-from-ico``"""
    return _checkIconPaths(options.windows_icon_path)


def getLinuxIconPaths():
    """*list of str*, values of ``--linux-icon``"""
    result = options.linux_icon_path

    # Check if Linux icon requirement is met.
    if isLinux() and not result and isOnefileMode():
        # spell-checker: ignore pixmaps
        default_icons = (
            "/usr/share/pixmaps/python%s.xpm" % python_version_str,
            "/usr/share/pixmaps/python%s.xpm" % sys.version_info[0],
            "/usr/share/pixmaps/python.xpm",
        )

        for icon in default_icons:
            if os.path.exists(icon):
                result.append(icon)
                break

    return _checkIconPaths(result)


def getMacOSIconPaths():
    """*list of str*, values of ``--macos-app-icon``"""
    return _checkIconPaths(
        icon_path for icon_path in options.macos_icon_path if icon_path != "none"
    )


def getWindowsIconExecutablePath():
    """*str* or *None* if not given, value of ``--windows-icon-from-exe``"""
    return options.icon_exe_path


def shallAskForWindowsAdminRights():
    """*bool*, value of ``--windows-uac-admin`` or ``--windows-uac-uiaccess``"""
    return options.windows_uac_admin


def shallAskForWindowsUIAccessRights():
    """*bool*, value of ``--windows-uac-uiaccess``"""
    return options.windows_uac_uiaccess


def getLegalCopyright():
    """*str* name of the product to use derived from ``--copyright``"""
    return options.legal_copyright


def getLegalTrademarks():
    """*str* name of the product to use derived from ``--trademarks``"""
    return options.legal_trademarks


def getLegalInformation():
    result = options.legal_copyright

    if options.legal_trademarks:
        if result is not None:
            result += "\nTrademark information:" + options.legal_trademarks
        else:
            result = options.legal_trademarks

    return result


def getWindowsVersionInfoStrings():
    """*dict of str*, values of ."""

    result = {}

    company_name = getCompanyName()
    if company_name:
        result["CompanyName"] = company_name

    product_name = getProductName()
    if product_name:
        result["ProductName"] = product_name

    if options.file_description:
        result["FileDescription"] = options.file_description

    if options.legal_copyright:
        result["LegalCopyright"] = options.legal_copyright

    if options.legal_trademarks:
        result["LegalTrademarks"] = options.legal_trademarks

    return result


def _parseVersionNumber(value):
    if value:
        parts = value.split(".")

        assert len(parts) <= 4

        while len(parts) < 4:
            parts.append("0")

        r = tuple(int(d) for d in parts)
        assert min(r) >= 0
        assert max(r) < 2**16
        return r
    else:
        return None


def getProductVersion():
    """:returns: str, derived from ``--product-version``"""
    return options.product_version


def getProductVersionTuple():
    """:returns: tuple of 4 ints or None, derived from ``--product-version``"""
    return _parseVersionNumber(options.product_version)


def getFileVersion():
    """:returns str, derived from ``--file-version``"""
    return options.file_version


def getFileVersionTuple():
    """:returns tuple of 4 ints or None, derived from ``--file-version``"""
    return _parseVersionNumber(options.file_version)


def getProductFileVersion():
    if options.product_version:
        if options.file_version:
            return "%s-%s" % (options.product_version, options.file_version)
        else:
            return options.product_version
    else:
        return options.file_version


def getWindowsSplashScreen():
    """:returns: bool derived from ``--onefile-windows-splash-screen-image``"""
    return options.splash_screen_image


def getCompanyName():
    """*str* name of the company to use derived from ``--company-name``"""
    return options.company_name


def getProductName():
    """*str* name of the product to use derived from ``--product-name``"""
    return options.product_name


def getMacOSTargetArch():
    """:returns: str enum ("universal", "arm64", "x86_64") derived from ``--macos-target-arch`` value"""
    if options is None:
        macos_target_arch = "native"
    else:
        macos_target_arch = options.macos_target_arch or "native"

    if macos_target_arch == "native":
        macos_target_arch = getArchitecture()

    return macos_target_arch


def shallCreateAppBundle():
    """*bool* shall create an application bundle, derived from ``--macos-create-app-bundle`` value"""
    if shallCreatePythonPgoInput():
        return False

    return options.macos_create_bundle and isMacOS()


def getMacOSSigningIdentity():
    """*str* value to use as identity for codesign, derived from ``--macos-sign-identity`` value"""
    result = options.macos_sign_identity

    if result is None:
        result = "ad-hoc"

    if result == "ad-hoc":
        result = "-"

    return result


def shallUseSigningForNotarization():
    """*bool* flag to use for codesign, derived from ``--macos-sign-notarization`` value"""
    return bool(options.macos_sign_notarization)


def getMacOSAppName():
    """*str* name of the app to use bundle"""
    return options.macos_app_name


def getMacOSSignedAppName():
    """*str* name of the app to use during signing"""
    return options.macos_signed_app_name


def getMacOSAppVersion():
    """*str* version of the app to use for bundle"""
    return options.macos_app_version


def getMacOSAppProtectedResourcesAccesses():
    """*list* key, value for protected resources of the app to use for bundle"""
    result = []

    for macos_protected_resource in options.macos_protected_resources:
        result.append(macos_protected_resource.split(":", 1))

    return result


def isMacOSBackgroundApp():
    """*bool*, derived from ``--macos-app-mode``"""
    return options.macos_app_mode == "background"


def isMacOSUiElementApp():
    """*bool*, derived from ``--macos-app-mode``"""
    return options.macos_app_mode == "ui-element"


_python_flags = None


def _getPythonFlags():
    """*list*, values of ``--python-flag``"""
    # There is many flags, pylint: disable=too-many-branches

    # singleton, pylint: disable=global-statement
    global _python_flags

    if _python_flags is None:
        _python_flags = set()

        for parts in options.python_flags:
            for part in parts.split(","):
                if part in ("-S", "nosite", "no_site"):
                    _python_flags.add("no_site")
                elif part in ("site",):
                    if "no_site" in _python_flags:
                        _python_flags.remove("no_site")
                elif part in (
                    "-R",
                    "static_hashes",
                    "norandomization",
                    "no_randomization",
                ):
                    _python_flags.add("no_randomization")
                elif part in ("-v", "trace_imports", "trace_import"):
                    _python_flags.add("trace_imports")
                elif part in ("no_warnings", "nowarnings"):
                    _python_flags.add("no_warnings")
                elif part in ("-O", "no_asserts", "noasserts"):
                    _python_flags.add("no_asserts")
                elif part in ("no_docstrings", "nodocstrings"):
                    _python_flags.add("no_docstrings")
                elif part in ("-OO",):
                    _python_flags.add("no_docstrings")
                    _python_flags.add("no_asserts")
                elif part in ("no_annotations", "noannotations"):
                    _python_flags.add("no_annotations")
                elif part in ("unbuffered", "-u"):
                    _python_flags.add("unbuffered")
                elif part in ("-m", "package_mode"):
                    _python_flags.add("package_mode")
                elif part in ("-I", "isolated"):
                    _python_flags.add("isolated")
                elif part in ("-B", "dont_write_bytecode", "dontwritebytecode"):
                    _python_flags.add("dontwritebytecode")
                elif part in ("-P", "safe_path"):
                    _python_flags.add("safe_path")
                else:
                    Tracing.options_logger.sysexit(
                        "Unsupported python flag '%s'." % part
                    )

    return _python_flags


def hasPythonFlagNoSite():
    """*bool* = "no_site" in python flags given"""

    return "no_site" in _getPythonFlags()


def hasPythonFlagNoAnnotations():
    """*bool* = "no_annotations" in python flags given"""

    return "no_annotations" in _getPythonFlags()


def hasPythonFlagNoAsserts():
    """*bool* = "no_asserts" in python flags given"""

    return "no_asserts" in _getPythonFlags()


def hasPythonFlagNoDocStrings():
    """*bool* = "no_docstrings" in python flags given"""

    return "no_docstrings" in _getPythonFlags()


def hasPythonFlagNoWarnings():
    """*bool* = "no_warnings" in python flags given"""

    return "no_warnings" in _getPythonFlags()


def hasPythonFlagIsolated():
    """*bool* = "isolated" in python flags given"""

    return "isolated" in _getPythonFlags()


def hasPythonFlagTraceImports():
    """*bool* = "trace_imports", "-v" in python flags given"""

    return "trace_imports" in _getPythonFlags()


def hasPythonFlagNoRandomization():
    """*bool* = "no_randomization", "-R", "static_hashes" in python flags given"""

    return "no_randomization" in _getPythonFlags()


def hasPythonFlagNoBytecodeRuntimeCache():
    """*bool* = "dontwritebytecode", "-B" in python flags given"""

    return "dontwritebytecode" in _getPythonFlags()


def hasPythonFlagNoCurrentDirectoryInPath():
    """*bool* = "safe_path", "-P" in python flags given"""

    return "safe_path" in _getPythonFlags()


def hasPythonFlagUnbuffered():
    """*bool* = "unbuffered", "-u" in python flags given"""

    return "unbuffered" in _getPythonFlags()


def hasPythonFlagPackageMode():
    """*bool* = "package_mode", "-m" in python flags given"""

    return "package_mode" in _getPythonFlags()


def shallNotUseDependsExeCachedResults():
    """:returns: bool derived from ``--disable-dll-dependency-cache`` or ``--force-dll-dependency-cache-update``"""
    return shallNotStoreDependsExeCachedResults() or getattr(
        options, "update_dependency_cache", False
    )


def shallNotStoreDependsExeCachedResults():
    """:returns: bool derived from ``--disable-dll-dependency-cache``"""
    return shallDisableCacheUsage("dll-dependencies")


def getPluginNameConsideringRenames(plugin_name):
    """Name of the plugin with renames considered."""

    # spell-checker: ignore delvewheel,pyzmq

    if plugin_name == "etherium":
        return "ethereum"
    if plugin_name == "pyzmq":
        return "delvewheel"

    return plugin_name


def getPluginsEnabled():
    """*tuple*, user enabled (standard) plugins (not including user plugins)

    Note:
        Do not use this outside of main binary, as plugins are allowed
        to activate plugins themselves and that will not be visible here.
    """
    result = OrderedSet()

    if options:
        for plugin_enabled in options.plugins_enabled:
            result.update(
                getPluginNameConsideringRenames(plugin_name)
                for plugin_name in plugin_enabled.split(",")
            )

    return tuple(result)


def getPluginsDisabled():
    """*tuple*, user disabled (standard) plugins.

    Note:
        Do not use this outside of main binary, as other plugins, e.g.
        hinted compilation will activate plugins themselves and this
        will not be visible here.
    """
    result = OrderedSet()

    if options:
        for plugin_disabled in options.plugins_disabled:
            result.update(
                getPluginNameConsideringRenames(plugin_name)
                for plugin_name in plugin_disabled.split(",")
            )

    return tuple(result)


def getUserPlugins():
    """*tuple*, items user provided of ``--user-plugin=``"""
    if not options:
        return ()

    return tuple(set(options.user_plugins))


def shallDetectMissingPlugins():
    """*bool* = **not** ``--plugin-no-detection``"""
    return options is not None and options.detect_missing_plugins


def getPythonPathForScons():
    """*str*, value of ``--python-for-scons``"""
    return options.python_scons


def shallCompileWithoutBuildDirectory():
    """*bool* currently hard coded, not when using debugger.

    When this is used, compilation is executed in a fashion that it runs
    inside the build folder, hiding it, attempting to make results more
    reproducible across builds of different programs.

    TODO: Make this not hardcoded, but possible to disable via an
    options.
    """
    return not shallRunInDebugger()


def shallPreferSourceCodeOverExtensionModules():
    """*bool* prefer source code over extension modules if both are there"""
    return options is not None and options.prefer_source_code


def shallUseProgressBar():
    """*bool* prefer source code over extension modules if both are there"""
    return options.progress_bar


def getForcedStdoutPath():
    """*str* force program stdout output into that filename"""
    if shallCreatePythonPgoInput():
        return False

    return options.force_stdout_spec


def getForcedStderrPath():
    """*str* force program stderr output into that filename"""
    if shallCreatePythonPgoInput():
        return False

    return options.force_stderr_spec


def shallShowSourceModifications(module_name):
    """*bool* display plugin source changes derived from --show-source-changes"""
    if options is None:
        return False

    result, _reason = module_name.matchesToShellPatterns(options.show_source_changes)

    return result


def isLowMemory():
    """*bool* low memory usage requested"""
    return options.low_memory


def getCompilationReportFilename():
    """*str* filename to write XML report of compilation to"""
    return options.compilation_report_filename


def getCompilationReportTemplates():
    """*tuple of str,str* template and output filenames to write reports to"""
    result = []
    for value in options.compilation_report_templates:
        result.append(value.split(":", 1))

    return tuple(result)


def getCompilationReportUserData():
    result = OrderedDict()

    for desc in options.compilation_report_user_data:
        if "=" not in desc:
            Tracing.options_logger.sysexit(
                "Error, user report data must be of key=value form not '%s'." % desc
            )

        key, value = desc.split("=", 1)

        if key in result and value != result[key]:
            Tracing.options_logger.sysexit(
                "Error, user report data key '%s' has been given conflicting values '%s' and '%s'."
                % (
                    key,
                    result[key],
                    value,
                )
            )

        if not re.match(
            r"^([_a-z][\w]?|[a-w_yz][\w]{2,}|[_a-z][a-l_n-z\d][\w]+|[_a-z][\w][a-k_m-z\d][\w]*)$",
            key,
        ):
            Tracing.options_logger.sysexit(
                "Error, user report data key '%s' is not valid as an XML tag, and therefore cannot be used."
                % key
            )

        result[key] = value

    return result


def shallCreateDiffableCompilationReport():
    """*bool*" derived from --report-diffable"""
    return options.compilation_report_diffable


def getUserProvidedYamlFiles():
    """*list* files with user provided Yaml files"""
    return options.user_yaml_files


def _getWarningMnemonicsDisabled():
    return sum([_splitShellPattern(x) for x in options.nowarn_mnemonics], [])


def shallDisplayWarningMnemonic(mnemonic):
    """*bool*" derived from --nowarn-mnemonic"""
    for pattern in _getWarningMnemonicsDisabled():
        if fnmatch.fnmatch(mnemonic, pattern):
            return False

    return True


def shallShowExecutedCommands():
    return isExperimental("show-commands")


def getTargetPythonDescription():
    """:returns: tuple(python_version,OS/arch) string derived from ``--target``"""
    if options.target_spec is not None:
        # TODO: Only one we are working on right now.
        assert options.target_spec == "wasi"

        return python_version, "wasi"

    return None


def getFcfProtectionMode():
    """:returns: string derived from ``--fcf-protection``"""
    return options.cf_protection


def getModuleParameter(module_name, parameter_name):
    """:returns: string derived from ``--module-parameter``"""

    module_name_prefix = module_name.getTopLevelPackageName().asString()

    if parameter_name.startswith(module_name_prefix + "-"):
        option_name = parameter_name
    else:
        option_name = module_name_prefix + "-" + parameter_name

    for module_option in options.module_parameters:
        try:
            module_option_name, module_option_value = module_option.split("=", 1)
        except ValueError:
            Tracing.optimization_logger.sysexit(
                """\
Error, must specify module parameter name and value with a separating \
'=' and not '%s"."""
                % module_option
            )

        if option_name == module_option_name:
            return module_option_value

    return None


def getForcedRuntimeEnvironmentVariableValues():
    """:returns: iterable (string, string) derived from ``--force-runtime-environment-variable``"""

    for forced_runtime_env_variables_spec in options.forced_runtime_env_variables:
        name, value = forced_runtime_env_variables_spec.split("=", 1)

        yield (name, value)


def getCompilationMode():
    """For reporting only, use shorter specific tests."""
    # return driven, pylint: disable=too-many-return-statements

    if isAcceleratedMode():
        return "accelerated"
    elif shallMakeModule():
        return "module"
    elif shallMakePackage():
        return "package"
    elif shallCreateAppBundle():
        return "app"
    elif isOnefileMode():
        return "onefile"
    elif isStandaloneMode():
        return "standalone"
    elif shallMakeDll():
        return "dll"




#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Python version specifics.

This abstracts the Python version decisions. This makes decisions based on
the numbers, and attempts to give them meaningful names. Where possible it
should attempt to make run time detections.

"""

import __future__

import ctypes
import os
import re
import sys


def getSupportedPythonVersions():
    """Officially supported Python versions for nexium."""

    return (
        "2.6",
        "2.7",
        "3.4",
        "3.5",
        "3.6",
        "3.7",
        "3.8",
        "3.9",
        "3.10",
        "3.11",
        "3.12",
        "3.13",
    )


def getNotYetSupportedPythonVersions():
    """Versions known to not work at all (yet)."""
    return ("3.14",)


def getPartiallySupportedPythonVersions():
    """Partially supported Python versions for nexium."""

    return ()


def getZstandardSupportingVersions():
    result = getSupportedPythonVersions() + getPartiallySupportedPythonVersions()

    # This will crash if we remove versions, but it is more likely to work
    # with newly supported versions, and to list the ones not supported by
    # zstandard.
    result = tuple(
        version for version in result if version not in ("2.6", "2.7", "3.3", "3.4")
    )

    return result


def getTestExecutionPythonVersions():
    return (
        getSupportedPythonVersions()
        + getPartiallySupportedPythonVersions()
        + getNotYetSupportedPythonVersions()
    )


# Make somewhat sure we keep these ones consistent
assert len(
    set(
        getPartiallySupportedPythonVersions()
        + getNotYetSupportedPythonVersions()
        + getSupportedPythonVersions()
    )
) == len(
    getPartiallySupportedPythonVersions()
    + getNotYetSupportedPythonVersions()
    + getSupportedPythonVersions()
)


def getSupportedPythonVersionStr():
    supported_python_versions = getSupportedPythonVersions()

    supported_python_versions_str = repr(supported_python_versions)[1:-1]
    supported_python_versions_str = re.sub(
        r"(.*),(.*)$", r"\1, or\2", supported_python_versions_str
    )

    return supported_python_versions_str


def _getPythonVersion():
    big, major, minor = sys.version_info[0:3]

    return big * 256 + major * 16 + min(15, minor)


python_version = _getPythonVersion()

python_version_full_str = ".".join(str(s) for s in sys.version_info[0:3])
python_version_str = ".".join(str(s) for s in sys.version_info[0:2])


# TODO: Move error construction helpers to separate node making helpers module.
def getErrorMessageExecWithNestedFunction():
    """Error message of the concrete Python in case an exec occurs in a
    function that takes a closure variable.
    """

    assert python_version < 0x300

    # Need to use "exec" to detect the syntax error, pylint: disable=W0122

    try:
        exec(
            """
def f():
   exec ""
   def nested():
      return closure"""
        )
    except SyntaxError as e:
        return e.message.replace("'f'", "'%s'")


def getComplexCallSequenceErrorTemplate():
    if not hasattr(getComplexCallSequenceErrorTemplate, "result"):
        try:
            # We are doing this on purpose, to get the exception.
            # pylint: disable=not-an-iterable,not-callable
            f = None
            f(*None)
        except TypeError as e:
            result = (
                e.args[0]
                .replace("NoneType object", "%s")
                .replace("NoneType", "%s")
                .replace("None ", "%s ")
            )
            getComplexCallSequenceErrorTemplate.result = result
        else:
            sys.exit("Error, cannot detect expected error message.")

    return getComplexCallSequenceErrorTemplate.result


def getUnboundLocalErrorErrorTemplate():
    if not hasattr(getUnboundLocalErrorErrorTemplate, "result"):
        try:
            # We are doing this on purpose, to get the exception.
            # pylint: disable=undefined-variable
            del _f
        except UnboundLocalError as e:
            result = e.args[0].replace("_f", "%s")
            getUnboundLocalErrorErrorTemplate.result = result
        else:
            sys.exit("Error, cannot detect expected error message.")

    return getUnboundLocalErrorErrorTemplate.result


def getDictFromkeysNoArgErrorMessage():
    try:
        dict.fromkeys()
    except TypeError as e:
        return e.args[0]


_needs_set_literal_reverse_insertion = None


def needsSetLiteralReverseInsertion():
    """For Python3, until Python3.5 ca. the order of set literals was reversed."""
    # Cached result, pylint: disable=global-statement
    global _needs_set_literal_reverse_insertion

    if _needs_set_literal_reverse_insertion is None:
        try:
            value = eval("{1,1.0}.pop()")  # pylint: disable=eval-used
        except SyntaxError:
            _needs_set_literal_reverse_insertion = False
        else:
            _needs_set_literal_reverse_insertion = type(value) is float

    return _needs_set_literal_reverse_insertion


def needsDuplicateArgumentColOffset():
    if python_version < 0x353:
        return False
    else:
        return True


def getRunningPythonDllHandle():
    # We trust ctypes internals here, pylint: disable=protected-access
    # spell-checker: ignore pythonapi
    return ctypes.pythonapi._handle


def getRunningPythonDLLPath():
    from qutayba.utils.SharedLibraries import (
        getWindowsRunningProcessModuleFilename,
    )

    return getWindowsRunningProcessModuleFilename(getRunningPythonDllHandle())


def getTargetPythonDLLPath():
    dll_path = getRunningPythonDLLPath()

    from qutayba.Options import shallUsePythonDebug

    if dll_path.endswith("_d.dll"):
        if not shallUsePythonDebug():
            dll_path = dll_path[:-6] + ".dll"

        if not os.path.exists(dll_path):
            sys.exit("Error, cannot switch to non-debug Python, not installed.")

    else:
        if shallUsePythonDebug():
            dll_path = dll_path[:-4] + "_d.dll"

        if not os.path.exists(dll_path):
            sys.exit("Error, cannot switch to debug Python, not installed.")

    return dll_path


def isStaticallyLinkedPython():
    # On Windows, there is no way to detect this from sysconfig.
    if os.name == "nt":
        return ctypes.pythonapi is None

    try:
        import sysconfig
    except ImportError:
        # Cannot detect this properly for Python 2.6, but we don't care much
        # about that anyway.
        return False

    result = sysconfig.get_config_var("Py_ENABLE_SHARED") == 0

    return result


def getPythonABI():
    if hasattr(sys, "abiflags"):
        abiflags = sys.abiflags

        # Cyclic dependency here.
        from qutayba.Options import shallUsePythonDebug

        # spell-checker: ignore getobjects
        if shallUsePythonDebug() or hasattr(sys, "getobjects"):
            if not abiflags.startswith("d"):
                abiflags = "d" + abiflags
    else:
        abiflags = ""

    return abiflags


def getLaunchingSystemPrefixPath():
    from qutayba.utils.Utils import getLaunchingnexiumProcessEnvironmentValue

    return getLaunchingnexiumProcessEnvironmentValue("DEVILPY_SYS_PREFIX")


_the_sys_prefix = None


def getSystemPrefixPath():
    """Return real sys.prefix as an absolute path breaking out of virtualenv.

    Note:

        For nexium, it often is OK to break out of the virtualenv, and use the
        original install. Mind you, this is not about executing anything, this is
        about building, and finding the headers to compile against that Python, we
        do not care about any site packages, and so on.

    Returns:
        str - path to system prefix
    """

    global _the_sys_prefix  # Cached result, pylint: disable=global-statement
    if _the_sys_prefix is None:
        sys_prefix = getattr(
            sys, "real_prefix", getattr(sys, "base_prefix", sys.prefix)
        )
        sys_prefix = os.path.abspath(sys_prefix)

        # Some virtualenv contain the "orig-prefix.txt" as a textual link to the
        # target, this is often on Windows with virtualenv. There are two places to
        # look for.
        for candidate in (
            "Lib/orig-prefix.txt",
            "lib/python%s/orig-prefix.txt" % python_version_str,
        ):
            candidate = os.path.join(sys_prefix, candidate)
            if os.path.exists(candidate):
                # Cannot use FileOperations.getFileContents() here, because of circular dependency.
                # pylint: disable=unspecified-encoding
                with open(candidate) as f:
                    sys_prefix = f.read()

                # Trailing spaces in the python prefix, please not.
                assert sys_prefix == sys_prefix.strip()

        # This is another for of virtualenv references:
        if os.name != "nt" and os.path.islink(os.path.join(sys_prefix, ".Python")):
            sys_prefix = os.path.normpath(
                os.path.join(os.readlink(os.path.join(sys_prefix, ".Python")), "..")
            )

        # Some virtualenv created by "venv" seem to have a different structure, where
        # library and include files are outside of it.
        if (
            os.name != "nt"
            and python_version >= 0x330
            and os.path.exists(os.path.join(sys_prefix, "bin/activate"))
        ):
            python_binary = os.path.join(sys_prefix, "bin", "python")
            python_binary = os.path.realpath(python_binary)

            sys_prefix = os.path.normpath(os.path.join(python_binary, "..", ".."))

        # Resolve symlinks on Windows manually.
        if os.name == "nt":
            from qutayba.utils.FileOperations import getDirectoryRealPath

            sys_prefix = getDirectoryRealPath(sys_prefix)

        # Self-compiled Python version in source tree
        if os.path.isdir(
            os.path.join(os.path.dirname(os.path.realpath(sys.executable)), "PCbuild")
        ):
            sys_prefix = os.path.dirname(os.path.realpath(sys.executable))

        _the_sys_prefix = sys_prefix

    return _the_sys_prefix


def getFutureModuleKeys():
    result = [
        "unicode_literals",
        "absolute_import",
        "division",
        "print_function",
        "generator_stop",
        "nested_scopes",
        "generators",
        "with_statement",
    ]

    if hasattr(__future__, "barry_as_FLUFL"):
        result.append("barry_as_FLUFL")
    if hasattr(__future__, "annotations"):
        result.append("annotations")

    return result


def getImportlibSubPackages():
    result = []
    if python_version >= 0x270:
        import importlib
        import pkgutil

        for module_info in pkgutil.walk_packages(importlib.__path__):
            result.append(module_info[1])

    return result


def isDebugPython():
    """Is this a debug build of Python."""
    return hasattr(sys, "gettotalrefcount")


def _getFloatDigitBoundaryValue():
    if python_version < 0x270:
        bits_per_digit = 15
    elif python_version < 0x300:
        bits_per_digit = sys.long_info.bits_per_digit
    else:
        bits_per_digit = sys.int_info.bits_per_digit

    return (2**bits_per_digit) - 1


_float_digit_boundary = _getFloatDigitBoundaryValue()


def isPythonValidDigitValue(value):
    """Does the given value fit into a float digit.

    Note: Digits in long objects do not use 2-complement, but a boolean sign.
    """

    return -_float_digit_boundary <= value <= _float_digit_boundary


sizeof_clong = ctypes.sizeof(ctypes.c_long)

# TODO: We could be more aggressive here, there are issues with using full
# values, in some contexts, but that can probably be sorted out.
_max_signed_long = 2 ** (sizeof_clong * 7) - 1
_min_signed_long = -(2 ** (sizeof_clong * 7))

# Used by data composer to write Python long values.
sizeof_clonglong = ctypes.sizeof(ctypes.c_longlong)

_max_signed_longlong = 2 ** (sizeof_clonglong * 8 - 1) - 1
_min_signed_longlong = -(2 ** (sizeof_clonglong * 8 - 1))


def isPythonValidCLongValue(value):
    return _min_signed_long <= value <= _max_signed_long


def isPythonValidCLongLongValue(value):
    return _min_signed_longlong <= value <= _max_signed_longlong


def getInstalledPythonRegistryPaths(version):
    """Yield all Pythons as found in the Windows registry."""
    # Windows only code,
    # pylint: disable=I0021,import-error,redefined-builtin
    from qutayba.__past__ import WindowsError

    if str is bytes:
        import _winreg as winreg  # pylint: disable=I0021,import-error,no-name-in-module
    else:
        import winreg  # pylint: disable=I0021,import-error,no-name-in-module

    for hkey_branch in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for arch_key in (0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY):
            for suffix in "", "-32", "-arm64":
                try:
                    key = winreg.OpenKey(
                        hkey_branch,
                        r"SOFTWARE\Python\PythonCore\%s%s\InstallPath"
                        % (version, suffix),
                        0,
                        winreg.KEY_READ | arch_key,
                    )

                    install_dir = os.path.normpath(winreg.QueryValue(key, ""))
                except WindowsError:
                    pass
                else:
                    candidate = os.path.normpath(
                        os.path.join(install_dir, "python.exe")
                    )

                    if os.path.exists(candidate):
                        yield candidate


def getTkInterVersion():
    """Get the tk-inter version or None if not installed."""
    try:
        if str is bytes:
            return str(__import__("TkInter").TkVersion)
        else:
            return str(__import__("tkinter").TkVersion)
    except ImportError:
        # This should lead to no action taken ideally.
        return None


def getModuleLinkerLibs():
    """Get static link libraries needed."""
    try:
        import sysconfig
    except ImportError:
        return []
    else:
        # static link libraries might be there, spell-checker: ignore modlibs
        result = sysconfig.get_config_var("MODLIBS") or ""
        result = [entry[2:] for entry in result.split() if entry.startswith("-l:")]

        return result


def isPythonWithGil():
    return python_version < 0x3D0 or sys.flags.gil



