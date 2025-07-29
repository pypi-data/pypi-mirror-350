#!/bin/env python
################################################################
import os
import time

import streamlit as st
import yaml

# from solidipes.scanners.scanner_local import ExportScanner
from solidipes.utils import get_study_metadata, logging, set_study_metadata  # get_study_root_path
from solidipes.utils.git_infos import GitInfos
from solidipes.utils.metadata import lang
from solidipes.utils.metadata import licences_data_or_software as licenses
from solidipes.utils.utils import get_zenodo_infos
from streamlit_editable_list import editable_list

from solidipes_core_plugin.utils.zenodo_utils import get_existing_deposition_identifier

from .custom_widgets import EditProgBox, EditTextBox

# from .file_list import FileList
from .uploader import UploaderWidget

DELAY_FIX_BUTTONS = 0.5


print = logging.invalidPrint
logger = logging.getLogger()


class ZenodoInfos:
    def __init__(self, layout):
        self.git_infos = GitInfos()
        self.layout = layout.container()
        self.zenodo_metadata = get_study_metadata()

        self.key = "zenodo_infos"

    def _create_stateful_property(self, property_key):
        streamlit_key_template = property_key + "_{self.key}"

        def getter(self):
            streamlit_key = streamlit_key_template.format(self=self)
            return getattr(st.session_state, streamlit_key, False)

        def setter(self, value):
            streamlit_key = streamlit_key_template.format(self=self)
            st.session_state[streamlit_key] = value

        return property(getter, setter)

    edit_mode = _create_stateful_property(None, "edit_mode")
    must_save = _create_stateful_property(None, "must_save")

    def saveZenodoEntry(self, key, value):
        self.zenodo_metadata[key] = value
        set_study_metadata(self.zenodo_metadata)

    def save_description(self, value):
        self.zenodo_metadata["description"] = value
        set_study_metadata(self.zenodo_metadata)

    def show_edit_button(self):
        st.button("Edit metadata :pencil:", on_click=lambda: setattr(self, "edit_mode", True))

    def show_title(self):
        st.markdown(f"## <center> {self.zenodo_metadata['title']} </center>", unsafe_allow_html=True)

    def edit_title(self):
        st.subheader("Title")
        title = st.text_input("", self.zenodo_metadata["title"], key=f"title_{self.key}", label_visibility="collapsed")

        if self.must_save:
            self.saveZenodoEntry("title", title)

    def format_keywords(self, keywords):
        return "<b>Keywords:</b> " + ", ".join(keywords)

    def show_keywords(self):
        st.markdown(self.format_keywords(self.zenodo_metadata["keywords"]), unsafe_allow_html=True)

    def edit_keywords(self):
        keywords_data = [[k] for k in self.zenodo_metadata["keywords"]]

        input_params = [
            {
                "placeholder": "Keyword",
                "type": "text",
                "value": "",
            },
        ]

        st.subheader("Keywords")
        keywords_data = editable_list(keywords_data, input_params, auto_save=True, key=f"keywords_{self.key}")
        keywords = [k[0] for k in keywords_data]

        if self.must_save:
            self.saveZenodoEntry("keywords", keywords)

    def format_authors(self, authors_data):
        orcid_img = '<img height="15" src="https://zenodo.org/static/images/orcid.svg">'
        authors = []
        affiliations = []
        for auth in authors_data:
            if "affiliation" in auth:
                aff = auth["affiliation"].split(";")
                for e in aff:
                    if e.strip() not in affiliations:
                        affiliations.append(e.strip())

        for auth in authors_data:
            text = ""
            if "orcid" in auth:
                text += f'<a href="https://orcid.org/{auth["orcid"]}">{orcid_img}</a> '
            if "name" in auth:
                text += f'**{auth["name"]}**'
            if "affiliation" in auth:
                text += "$^{"
                aff = auth["affiliation"].split(";")
                aff = [affiliations.index(e.strip()) + 1 for e in aff]
                aff = [str(e) for e in aff]
                text += f'{",".join(aff)}'
                text += "}$"

            authors.append(text)
        formatted = "**<center> " + ", ".join(authors) + " </center>**\n"
        for idx, aff in enumerate(affiliations):
            formatted += f"<center><sup>{idx+1}</sup> <i>{aff}</i></center>\n"
        return formatted

    def show_creators(self):
        st.markdown(self.format_authors(self.zenodo_metadata["creators"]), unsafe_allow_html=True)

    def edit_creators(self):
        creators_data = [
            [
                a.get("name", ""),
                a.get("affiliation", ""),
                a.get("orcid", ""),
            ]
            for a in self.zenodo_metadata["creators"]
        ]

        input_params = [
            {
                "placeholder": "Name",
                "type": "text",
                "value": "",
            },
            {
                "placeholder": "Affiliations, separated by ;",
                "type": "text",
                "value": "",
            },
            {
                "placeholder": "ORCID",
                "type": "text",
                "value": "",
            },
        ]

        st.subheader("Authors")
        creators_data = editable_list(creators_data, input_params, auto_save=True, key=f"creators_{self.key}")
        if not self.must_save:
            return

        creators = []
        for creator in creators_data:
            creator_dict = {}
            creator_dict["name"] = creator[0]
            if creator[1] != "":
                creator_dict["affiliation"] = creator[1]
            if creator[2] != "":
                creator_dict["orcid"] = creator[2]
            creators.append(creator_dict)

        for e in creators:
            if e["name"] == "":
                raise RuntimeError("An author needs mandatorily a name")

        self.saveZenodoEntry("creators", creators)

    def show_general_metadata(self):
        entries = [
            f"**Upload type**: {self.zenodo_metadata['upload_type']}",
            f"**License**: {self.zenodo_metadata['license']}",
            f"**Language**: {self.zenodo_metadata['language']}",
        ]
        if "doi" in self.zenodo_metadata:
            entries.append(f"**DOI**: {self.zenodo_metadata['doi']}")
        st.markdown("  \n".join(entries))

    def edit_general_metadata(self):
        st.subheader("General Metadata")
        upload_type = self.edit_upload_type()
        license = self.edit_license()
        language = self.edit_language()
        doi = self.edit_doi()

        if not self.must_save:
            return

        if doi != "":
            self.saveZenodoEntry("doi", doi)
        elif "doi" in self.zenodo_metadata:
            del self.zenodo_metadata["doi"]
        self.saveZenodoEntry("upload_type", upload_type)
        self.saveZenodoEntry("license", license)
        self.saveZenodoEntry("language", language)

    def edit_upload_type(self):
        options = [
            "publication",
            "poster",
            "presentation",
            "dataset",
            "image",
            "video",
            "software",
            "lesson",
            "physicalobject",
            "other",
        ]
        value = self.zenodo_metadata["upload_type"]
        return st.selectbox("Upload type", options=options, index=options.index(value))

    def edit_license(self):
        options = [_l[0] for _l in licenses]
        fmt_map = dict(licenses)

        value = self.zenodo_metadata["license"]
        return st.selectbox(
            "License", options=options, index=options.index(value), format_func=lambda x: fmt_map[x] + f" ({x})"
        )

    def edit_language(self):
        options = [_l[0] for _l in lang]
        fmt_map = dict(lang)

        value = self.zenodo_metadata["language"]
        return st.selectbox("Language", options=options, index=options.index(value), format_func=lambda x: fmt_map[x])

    def edit_doi(self):
        value = ""
        if "doi" in self.zenodo_metadata:
            value = self.zenodo_metadata["doi"]

        return st.text_input("DOI", value=value, placeholder="put a reserved doi if you have one")

    def show_related_identifiers(self):
        rels_dicts = self.zenodo_metadata.get("related_identifiers", [])
        if len(rels_dicts) == 0:
            return

        formatted = "**Related Identifiers**  \n"

        for r in rels_dicts:
            formatted += f"- {r['relation']} {r['identifier']} ({r['resource_type']})\n"

        st.markdown(formatted)

    def edit_related_identifiers(self):
        rels_dicts = self.zenodo_metadata.get("related_identifiers", [])
        rels_lists = [
            [
                r["relation"],
                r["resource_type"],
                r["identifier"],
            ]
            for r in rels_dicts
        ]

        input_params = [
            {
                "placeholder": "Relation",
                "list": "relations",
                "value": "",
                "options": [
                    "isCitedBy",
                    "cites",
                    "isSupplementTo",
                    "isSupplementedBy",
                    "isContinuedBy",
                    "continues",
                    "isDescribedBy",
                    "describes",
                    "hasMetadata",
                    "isMetadataFor",
                    "isNewVersionOf",
                    "isPreviousVersionOf",
                    "isPartOf",
                    "hasPart",
                    "isReferencedBy",
                    "references",
                    "isDocumentedBy",
                    "documents",
                    "isCompiledBy",
                    "compiles",
                    "isVariantFormOf",
                    "isOriginalFormof",
                    "isIdenticalTo",
                    "isAlternateIdentifier",
                    "isReviewedBy",
                    "reviews",
                    "isDerivedFrom",
                    "isSourceOf",
                    "requires",
                    "isRequiredBy",
                    "isObsoletedBy",
                    "obsolete",
                ],
            },
            {
                "placeholder": "Type",
                "list": "resource_types",
                "value": "",
                "options": [
                    "publication-annotationcollection",
                    "publication-book",
                    "publication-section",
                    "publication-conferencepaper",
                    "publication-datamanagementplan",
                    "publication-article",
                    "publication-patent",
                    "publication-preprint",
                    "publication-deliverable",
                    "publication-milestone",
                    "publication-proposal",
                    "publication-report",
                    "publication-softwaredocumentation",
                    "publication-taxonomictreatment",
                    "publication-technicalnote",
                    "publication-thesis",
                    "publication-workingpaper",
                    "publication-other",
                    "software",
                ],
            },
            {
                "placeholder": "Identifier",
                "type": "text",
                "value": "",
            },
        ]

        st.subheader("Additional Relations")
        rels_lists = editable_list(rels_lists, input_params, auto_save=True, key=f"related_identifiers_{self.key}")
        if not self.must_save:
            return

        rels_dicts = [
            {
                "relation": r[0],
                "resource_type": r[1],
                "identifier": r[2],
            }
            for r in rels_lists
        ]
        self.saveZenodoEntry("related_identifiers", rels_dicts)

    def textbox(self, key, **kwargs):
        EditTextBox(self.zenodo_metadata[key], caption=key.capitalize(), key=key, **kwargs)

    def description_box(self, **kwargs):
        desc = self.zenodo_metadata["description"]
        with st.expander("**Description**", expanded=True):
            EditProgBox(desc, language="markdown", key="description", on_apply=self.save_description, **kwargs)

    def show(self):
        with self.layout:
            # Must show editable form temporarily to save new metadata
            erasable = st.empty()
            with erasable:
                self.show_editable()

            if not self.edit_mode:
                erasable.empty()
                self.show_formatted()

            self.description_box()
            self.raw_editor()

    def show_formatted(self):
        self.show_edit_button()
        self.show_title()
        self.show_creators()
        self.show_keywords()
        self.show_general_metadata()
        self.show_related_identifiers()

    def show_editable(self):
        with st.form(f"form_{self.key}"):
            self.edit_title()
            self.edit_creators()
            self.edit_keywords()
            self.edit_general_metadata()
            self.edit_related_identifiers()
            self.must_save = False
            st.form_submit_button("Save", on_click=self.close_editable)

    def close_editable(self):
        self.edit_mode = False
        self.must_save = True

    def raw_editor(self):
        with self.layout.expander("**Additional Raw Metadata** (Zenodo YAML format)", expanded=False):
            st.markdown("You can edit the metadata below")
            st.markdown(
                "*Description of the Zenodo metadata can be found"
                " [here](https://github.com/zenodo/developers.zenodo.org"
                "/blob/master/source/includes/resources/deposit/"
                "_representation.md#deposit-metadata)*"
            )
            st.markdown("---")

            zenodo_metadata = get_study_metadata()
            metadata = zenodo_metadata.copy()

            for k in [
                "title",
                "creators",
                "keywords",
                "language",
                "upload_type",
                "license",
                "description",
                "related_identifiers",
            ]:
                if k in metadata:
                    del metadata[k]
            if metadata:
                zenodo_content = yaml.safe_dump(metadata)
            else:
                zenodo_content = ""

            def save(x):
                metadata = yaml.safe_load(x)
                zenodo_metadata.update(metadata)
                set_study_metadata(zenodo_metadata)

            EditProgBox(
                zenodo_content, language="yaml", disable_view=True, on_apply=lambda x: save(x), key="zenodo_raw"
            )


################################################################


class ZenodoPublish(UploaderWidget):
    def __init__(self, *args):
        super().__init__(*args)

    def show_submission_panel(self):
        with self.layout.expander("Publish in Zenodo", expanded=True):
            token = st.text_input("Zenodo token", type="password", on_change=self.ensure_submit_detection)
            zenodo_metadata = get_study_metadata()
            cached_zenodo_info = get_zenodo_infos()

            existing_identifier = ""
            if "deposition_identifier" in cached_zenodo_info:
                existing_identifier = cached_zenodo_info["deposition_identifier"]
            if "doi" in zenodo_metadata:
                existing_identifier = zenodo_metadata["doi"]

            if st.checkbox("Use existing identifier", value=bool(existing_identifier)):
                new_deposition = False
                existing_identifier = st.text_input(
                    "Identifier (URL or DOI)", value=existing_identifier, on_change=self.ensure_submit_detection
                )
            else:
                new_deposition = True
                existing_identifier = ""

            if new_deposition:
                sandbox = st.checkbox('Publish in "Sandbox"', value=True)
            else:
                sandbox = bool(existing_identifier) and "sandbox" in existing_identifier

            col1, col2 = st.columns(2)
            if not sandbox:
                col2.markdown(
                    "**Not using Sandbox will submit to the main "
                    "Zenodo website. Please push content with caution "
                    "as it may result in a permanent entry**"
                )

            if "zenodo_publish" not in st.session_state:
                st.session_state.zenodo_publish = []

            if col1.button("Submit draft", type="primary"):
                st.session_state.zenodo_publish = []
                try:
                    self.upload(token, existing_identifier, sandbox=sandbox, new_deposition=new_deposition)
                except Exception as e:
                    self.global_message.error("upload error: " + str(e))

            st.markdown(
                "<span style='font-size:0.85em;'>Note: After sending a draft on Zenodo, the dataset can still be"
                ' modified until the "Publish" button is pressed on Zenodo. Metadata can always be modified, even'
                " after publication.</span>",
                unsafe_allow_html=True,
            )

            if st.session_state.zenodo_publish:
                url = get_existing_deposition_identifier(".")
                st.markdown(f"**Deposition url**: {url}")
                logger.info(st.session_state.zenodo_publish)
                st.code("\n".join(st.session_state.zenodo_publish).replace("[94m", "").replace("[0m", ""))

    def ensure_submit_detection(self):
        """Ensure that clicking on the submit button after editing a text field triggers the button.
        Bug seems to happen because of the st.empty call on the progress bar showing loading files."""

        time.sleep(DELAY_FIX_BUTTONS)

    def upload(self, access_token=None, existing_identifier=None, sandbox=True, new_deposition=False):
        import argparse

        import solidipes_core_plugin.uploaders.zenodo as zenodo_upload

        args = argparse.Namespace()
        args.access_token = access_token
        args.sandbox = sandbox
        args.directory = None
        args._print = self._print
        args.existing_identifier = existing_identifier
        args.new_deposition = new_deposition
        args.tmp_dir = "/tmp" if os.name != "nt" else os.path.expanduser(r"~\AppData\Local\Temp")
        args.no_cleanup = True
        zenodo_upload.main(args)
