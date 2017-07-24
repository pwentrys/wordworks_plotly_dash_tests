from utilities.SQL import SQL


class SentenceWorks:
    # OPENNESS = []
    CATEGORIES = []
    TENSES = []

    def __init__(self, data):
        self.data = data
        self.sql = SQL()
        self._custom_init()

    def _custom_init(self):
        if len(SentenceWorks.CATEGORIES) < 1:
            SentenceWorks.CATEGORIES = self.sql.execute_table_cols('category', ['name']).get('name').values
        if len(SentenceWorks.TENSES) < 1:
            SentenceWorks.TENSES = self.sql.execute_table_cols('tense', ['name']).get('name').values

    @staticmethod
    def _format_word(string: str) -> str:
        string = string.lower()
        return string

    def determine_openness(self, string: str):
        return ''

    def determine_category(self, string: str):
        return ''

    def determine_tense(self, string: str):
        return ''

    @staticmethod
    def _extract_from_paragraphs(paragraphs: list):
        result = []
        for paragraph in paragraphs:
            result.extend(SentenceWorks._extract_from_sentences(paragraph))
        return result

    def extract_from_data(self):
        res = self._extract_from_paragraphs(self.data)
        res = set(res)
        return res

    PUNCTUATION_CONTAIN_REPLACE_EMPTY = [',', '"', '<', '>', '(', ')', ';']

    @staticmethod
    def _remove_punctuation(sentence: str):
        sentence = sentence.strip()
        if sentence.endswith('.'):
            sentence = sentence[:-1]
        for replacement in SentenceWorks.PUNCTUATION_CONTAIN_REPLACE_EMPTY:
            if sentence.__contains__(replacement):
                sentence = sentence.replace(replacement, '')
        return sentence

    @staticmethod
    def _extract_from_sentences(paragraph: str):
        result = []
        sentences = paragraph.replace('.\n', '. ')
        sentences = sentences.replace('—', ' ')
        sentences = sentences.split('. ')
        for sentence in sentences:
            result.extend(SentenceWorks._extract_from_sentence(sentence))
        return result

    @staticmethod
    def _extract_from_sentence(sentence: str):
        print(f'SENTENCE: {sentence}')
        sentence = SentenceWorks._remove_punctuation(sentence)
        return sentence.split(' ')

    def close(self):
        self.sql.close()
