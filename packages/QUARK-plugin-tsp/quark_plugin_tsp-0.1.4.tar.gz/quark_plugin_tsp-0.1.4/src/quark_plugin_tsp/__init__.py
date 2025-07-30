from quark.plugin_manager import factory

from quark_plugin_tsp.tsp_graph_provider import TspGraphProvider
from quark_plugin_tsp.tsp_qubo_mapping_dnx import TspQuboMappingDnx
from quark_plugin_tsp.classical_tsp_solver import ClassicalTspSolver

def register() -> None:
    factory.register("tsp_graph_provider", TspGraphProvider)
    factory.register("tsp_qubo_mapping_dnx", TspQuboMappingDnx)
    factory.register("classical_tsp_solver", ClassicalTspSolver)
