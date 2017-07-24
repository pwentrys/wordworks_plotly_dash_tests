import pathlib
import re


class ReadWorks:
    RE_CITATION = re.compile(r'\[.*?\]')
    RE_SPACINGS = re.compile(r'(\n+)(?=[a-zA-Z0-9_])')

    @staticmethod
    def read_file(path: str):
        path = pathlib.Path(path)
        if path.is_file():
            return path.read_text(encoding='utf-8')
        return ''

    @staticmethod
    def citation_cleanup(text: str):
        text = ReadWorks.RE_CITATION.sub('', text)
        text = ReadWorks.RE_SPACINGS.sub('\n', text)
        return text
