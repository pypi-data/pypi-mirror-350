import xmltodict

from .text import Text


class XML(Text):
    supported_mime_types = {"text/xml": "xml", "application/xml": "xml", "application/paraview/state": "xml"}

    def __init__(self, **kwargs):
        from ..viewers.xml import XML as XMLViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [XMLViewer]

    @Text.loadable
    def xml(self):
        text = self.text
        xml = xmltodict.parse(text)
        return xml
