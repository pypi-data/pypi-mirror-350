__version__ = '1.0.7'


from .table_block import TableBlockV1_0 as TableBlock
from .text_block import TextBlockV1_0 as TextBlock

__all__ = [
    'TextBlock',
    'TableBlock',
]
