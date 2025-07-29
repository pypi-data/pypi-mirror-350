from pydantic import TypeAdapter

from moxn_types.blocks.document import PDFContentFromSourceModel
from moxn_types.blocks.image import ImageContentFromSourceModel
from moxn_types.blocks.signed import SignedURLContentModel
from moxn_types.blocks.text import TextContentModel
from moxn_types.blocks.variable import VariableContentModel

ContentBlockModel = (
    ImageContentFromSourceModel
    | PDFContentFromSourceModel
    | SignedURLContentModel
    | TextContentModel
    | VariableContentModel
)

ContentBlockAdapter: TypeAdapter[ContentBlockModel] = TypeAdapter(ContentBlockModel)
