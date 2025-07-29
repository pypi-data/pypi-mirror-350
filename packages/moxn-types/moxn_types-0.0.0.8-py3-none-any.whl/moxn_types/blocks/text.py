from typing import ClassVar, Literal

from moxn_types.blocks.base import BaseContent, BlockType


class TextContentModel(BaseContent):
    block_type: ClassVar[Literal[BlockType.TEXT]] = BlockType.TEXT
    text: str
