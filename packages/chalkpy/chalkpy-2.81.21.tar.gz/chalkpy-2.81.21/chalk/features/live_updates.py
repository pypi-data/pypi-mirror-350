from __future__ import annotations

from chalk._gen.chalk.graph.v1 import graph_pb2
from chalk.features.feature_set import FeatureSetBase
from chalk.features.resolver import RESOLVER_REGISTRY
from chalk.parsed.to_proto import ToProtoConverter
from chalk.utils import notebook
from chalk.utils.log_with_context import get_logger

_logger = get_logger(__name__)


def build_overlay_graph() -> graph_pb2.OverlayGraph | None:
    if not notebook.is_notebook():
        return None
    graph = ToProtoConverter.convert_graph(
        features_registry={k: v for k, v in FeatureSetBase.registry.items() if not notebook.is_defined_in_module(v)},
        resolver_registry=[x for x in RESOLVER_REGISTRY.get_all_resolvers() if not notebook.is_defined_in_module(x)],
        sql_source_registry=[],
        sql_source_group_registry=[],
        stream_source_registry=[],
        named_query_registry={},
    )
    return graph_pb2.OverlayGraph(feature_sets=graph.feature_sets, resolvers=graph.resolvers)
