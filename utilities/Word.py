class Word:
    def __init__(self, raw: str):
        self.raw = raw
        self.noun = raw.endswith("'s")
        self._cleanup_raw()
        self.singular, self.multiple = self._determine_singular_multiple()

    MULTIPLES = [
        'rs',
        's',
    ]

    def _cleanup_raw(self):
        if self.raw.endswith(f'\'s'):
            self.raw = self.raw[:-2]

    def _determine_singular_multiple(self):
        string = self.raw
        singular = string
        multiple = string
        for item in self.MULTIPLES:
            if singular.endswith(item):
                singular = singular[:-1]
        if singular == multiple:
            multiple += 's'
        return singular, multiple

    def __log__(self):
        return f'Raw: {self.raw}\n' \
               f'Singular: {self.singular}\n' \
               f'Multiple: {self.multiple}\n' \
               f'Noun: {self.noun}\n' \
