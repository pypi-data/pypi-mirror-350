from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata


def setup(app: Sphinx) -> ExtensionMetadata:
    """add this extension and its children to a Sphinx application"""
    return {}
