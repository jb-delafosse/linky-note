from linky_note.adapters.markdown.marko_extractor import MarkoExtractor
from linky_note.dto.dto import NotePath


class MarkoExtractorFactory:
    @staticmethod
    def __call__(filename: NotePath) -> MarkoExtractor:
        return MarkoExtractor(filename)
