from rdflib import Graph
from solidipes.loaders.file import File


class RDF(File):
    supported_mime_types = {"text/plain": ["rdf", "ttl"]}

    def __init__(self, **kwargs):
        from ..viewers.rdf import RDF as RDFViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [RDFViewer]

    @File.loadable
    def rdf(self):
        g = Graph()
        g.parse(self.file_info.path)
        return g
