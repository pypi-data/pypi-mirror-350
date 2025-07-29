from .text import Text


class YAML(Text):
    supported_mime_types = {"application/yaml": ["yaml", "yml"], "text/plain": ["yaml", "yml"]}

    def __init__(self, **kwargs):
        from ..viewers.xml import XML as XMLViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [XMLViewer]

    @Text.loadable
    def yaml(self):
        text = self.text
        import yaml as yaml_module

        yaml = yaml_module.safe_load(text)
        return yaml
