from marko_backlinks.usecases.marko_ext.elements import (
    BacklinkSection,
    Document,
    Heading,
    Link,
    LinkOrEmph,
    Wikiimage,
    Wikilink,
)
from marko_backlinks.usecases.marko_ext.parser import ReferenceParser
from marko_backlinks.usecases.marko_ext.renderer import (
    BacklinkSectionRendererMixin,
)


class ReferencesExtension:
    elements = [
        Document,
        Link,
        LinkOrEmph,
        Heading,
        BacklinkSection,
        Wikilink,
        Wikiimage,
    ]
    parser_mixins = [
        ReferenceParser,
    ]
    renderer_mixins = [
        BacklinkSectionRendererMixin,
    ]
