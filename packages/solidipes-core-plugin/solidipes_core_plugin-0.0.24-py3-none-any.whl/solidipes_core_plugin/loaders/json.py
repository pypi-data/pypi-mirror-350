import json

from solidipes.loaders.file import File


class JSON(File):
    supported_mime_types = {"text/plain": ["json"], "application/json": ["json"]}

    def __init__(self, **kwargs):
        from ..viewers.dictionary import DictViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [DictViewer]

    @File.loadable
    def dict(self):
        _dict = {}
        with open(self.file_info.path) as json_data:
            _dict.update(json.loads(json_data.read()))
        return _dict
