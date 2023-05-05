from .de_broglie_layouter import DeBroglieLayouter
from .graphviz_layouter import GraphvizLayouter
from .indexable_enums import IndexableEnum


class LayouterType(IndexableEnum):
    GRAPHVIZ = GraphvizLayouter.__name__
    DE_BROGLIE = DeBroglieLayouter.__name__
