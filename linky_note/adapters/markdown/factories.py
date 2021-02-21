from linky_note.adapters.markdown.marko_extractor import MarkoExtractor


class MarkoExtractorFactory:
    @staticmethod
    def __call__(filename: str) -> MarkoExtractor:
        return MarkoExtractor(filename)
