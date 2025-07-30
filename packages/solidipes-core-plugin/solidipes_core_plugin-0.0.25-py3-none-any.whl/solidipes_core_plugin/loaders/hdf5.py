import h5py
from solidipes.loaders.file import File


class HDF5(File):
    """HDF5 loader"""

    supported_mime_types = {"application/x-hdf5": ["hdf", "h5", "hdf5"], "application/x-hdf": ["h5", "hdf5"]}

    def __init__(self, **kwargs):
        from ..viewers.hdf5 import HDF5 as HDF5Viewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [HDF5Viewer]

    @File.loadable
    def datasets(self):
        return h5py.File(self.file_info.path)
