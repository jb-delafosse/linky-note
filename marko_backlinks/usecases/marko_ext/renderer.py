import urllib.parse
from collections import defaultdict

from marko_backlinks.interfaces import references_db


class BacklinkSectionRendererMixin:
    def __init__(self):
        super().__init__()
        self.source_note = None
        self._reference_db = references_db.REFERENCE_DB_FACTORY()

    def render_backlink_section(self, element):
        return ""

    def render_wikilink(self, element):
        return f"[{element.label}]({urllib.parse.quote(element.dest)})"

    def render_wikiimage(self, element):
        image_url = urllib.parse.quote("resources/" + element.image_path)
        return f"![No title]({image_url})"

    def render_document(self, element):
        text = self.render_children(element)  # type: ignore
        db_response = self._reference_db.get_references_that_target(
            references_db.GetReferencesThatTarget(
                note_title=element.source_note.note_title
            )
        )
        ref_dict = defaultdict(list)
        for ref in db_response.references:
            ref_dict[ref.source_note].append(ref.context)
        section_content = ""
        for source_note, contexts in ref_dict.items():
            section_content += f"  * [{source_note.note_title}]({urllib.parse.quote(source_note.note_path)})\n"
            for context in contexts:
                section_content += f"    * {context}\n"
        backlink_section = "## Linked References\n" "\n" f"{section_content}"
        return text + backlink_section
