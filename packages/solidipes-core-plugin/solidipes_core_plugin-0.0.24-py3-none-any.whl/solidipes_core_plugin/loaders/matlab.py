from solidipes.loaders.file import File


class MatlabData(File):
    """Matlab .mat file"""

    supported_mime_types = {"application/x-matlab-data": "mat"}

    def __init__(self, **kwargs):
        from ..viewers.matlab import MatlabData as MatlabDataViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [MatlabDataViewer]

    @File.loadable
    def arrays(self):
        import scipy.io

        mat = scipy.io.loadmat(self.file_info.path)
        return mat
