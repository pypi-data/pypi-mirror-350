#!/bin/env python
################################################################
import os
from abc import ABC, abstractmethod

import streamlit as st
from solidipes.scanners.scanner import list_files
from solidipes.scanners.scanner_local import ExportScanner
from solidipes.utils import logging
from solidipes.utils.utils import get_study_root_path

from solidipes_core_plugin.reports.widgets.file_list import FileList

################################################################
print = logging.invalidPrint
logger = logging.getLogger()
################################################################


class UploaderWidget(ABC):
    def __init__(self, layout, global_message, progress_layout):
        self.layout = layout
        self.layout = layout.container()
        self.global_message = global_message
        self.progress_layout = progress_layout

    def show(self):
        self.layout.markdown("")
        self.show_submission_panel()
        self.show_file_list()
        self.show_readme()

    def _print(self, val):
        logger.info(val)
        if "zenodo_publish" not in st.session_state:
            st.session_state.zenodo_publish = []
        st.session_state.zenodo_publish.append(val)

    @abstractmethod
    def show_submission_panel(self):
        pass

    @abstractmethod
    def upload(self, **kwargs):
        pass

    def show_file_list(self):
        self.layout.markdown("# Archive content")
        scanner = ExportScanner()
        progress_layout = self.layout.empty()
        files_layout = self.layout.container()

        found = scanner.get_loader_tree()
        files = list_files(found)

        with files_layout:
            FileList(
                all_found_files=files,
                progress_layout=progress_layout,
                show_curation_cols=False,
            )
        from solidipes_core_plugin.reports.widgets.ignore import IgnoreWidget

        IgnoreWidget(layout=self.layout)

    def show_readme(self):
        with self.layout.expander("Preview of `README.md`", expanded=True):
            readme_path = os.path.join(get_study_root_path(), "README.md")

            if not os.path.isfile(readme_path):
                st.markdown("No README.md file found!")
                return

            readme = open(readme_path, "r").read()
            st.markdown(readme)


################################################################
