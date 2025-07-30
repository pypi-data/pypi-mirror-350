from solidipes.loaders.file import File


class Text(File):
    """Text file, potentially formatted with markdown"""

    supported_mime_types = {"text/plain": "txt", "application/lammps": ["in", "data"]}

    def __init__(self, **kwargs):
        from ..viewers.text import Text as TextViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [TextViewer]

    @File.loadable
    def text(self):
        text = ""
        with open(self.file_info.path, "r") as f:
            text = f.read()
        return text


class Markdown(Text):
    """Markdown file"""

    supported_mime_types = {"text/markdown": "md"}

    def __init__(self, **kwargs):
        from ..viewers.text import Markdown as MarkdownViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [MarkdownViewer]
