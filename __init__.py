# __init__.py
from .quick_image_sequence_process import QuickImageSequenceProcessNode

NODE_CLASS_MAPPINGS = {
    "QuickImageSequenceProcess": QuickImageSequenceProcessNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "QuickImageSequenceProcess": "Quick Image Sequence Process",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]