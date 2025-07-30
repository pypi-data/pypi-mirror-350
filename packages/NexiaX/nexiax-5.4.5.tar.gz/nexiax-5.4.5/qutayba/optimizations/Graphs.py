#     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file


""" Graph optimization states.

These are not the graphs you might be thinking of. This is for rending the
progress of optimization into images.
"""

from qutayba import Options
from qutayba.ModuleRegistry import getDoneModules
from qutayba.Tracing import general

graph = None
computation_counters = {}

progressive = False


def _addModuleGraph(module, desc):
    module_graph = module.asGraph(graph, desc)

    return module_graph


def onModuleOptimizationStep(module):
    # Update the graph if active.
    if graph is not None:
        computation_counters[module] = computation_counters.get(module, 0) + 1

        if progressive:
            _addModuleGraph(module, computation_counters[module])


def startGraph():
    # We maintain this globally to make it accessible, pylint: disable=global-statement
    global graph

    if Options.shallCreateGraph():
        try:
            from pygraphviz import AGraph  # pylint: disable=I0021,import-error

            graph = AGraph(name="Optimization", directed=True)
            graph.layout()
        except ImportError:
            general.sysexit("Cannot import pygraphviz module, no graphing capability.")


def endGraph(output_filename):
    if graph is not None:
        for module in getDoneModules():
            _addModuleGraph(module, "final")

        graph.draw(output_filename + ".dot", prog="dot")



