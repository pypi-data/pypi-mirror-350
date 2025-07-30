import nbformat
from solidipes.loaders.file import File


class Notebook(File):
    """Notebook file, in Jupyter style"""

    supported_mime_types = {"application/jupyter-notebook": "ipynb"}

    def __init__(self, **kwargs):
        from ..viewers.notebook import Notebook as NotebookViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [NotebookViewer]

    @File.loadable
    def notebook(self):
        return nbformat.read(self.file_info.path, as_version=4)
