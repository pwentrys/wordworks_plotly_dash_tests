"""
        {
            'a': '',
            'an': '',
            'and': '',
            'answers': 'answer',
            'at': '',
            'by': '',
            'from': '',
            'for': '',
            'forums': 'forum',
            'have': '',
            'i': '',
            'in': '',
            'is': '',
            'it': '',
            'motors': 'motor',
            'my': '',
            'of': '',
            'on': '',
            'or': '',
            'that': '',
            'the': '',
            'this': '',
            'to': '',
            'vs': 'versus',
            'watching': 'watch',
            'with': '',
        },
        """
class WordWorks:
    PRE = {
        'begins': {},
        'contains': {
            'space-x': 'spacex',
            '-': ' ',
            "^": '',
            "'s": '',
            "'t": ' not',
            '®': '',
            '’': '',
            '…': '',
            '_': '',
            '"': '',
            '¿': '',
            '?': '',
            '–': ' ',
            "—": '',
            "*": '',
            "=": '',
            "$": '',
            '!': ' ',
            "'": '',
            "~": '',
            "«": '',
            "←": '',
            "”": '',
            "ღ": '',
            "•": '',
            '™': '',
            "“": '',
            ".com": ' ',
            "www.": ' ',
            "+": ' ',
            ",": ' ',
            ";": ' ',
            ".": ' ',
            "/": ' ',
            "\\": ' ',
            ":": ' ',
            "#": ' ',
            "&": ' ',
            "(": ' ',
            ")": ' ',
            '<': '',
            '>': '',
            "@": '',
            "[": '',
            "...": '',
            "]": '',
        },
        'ends': {
            "%": ' percent',
        },
        'is': {},
    }
    POST = {
        'begins': {},
        'contains': {
            "'s": '',
            "+": '',
            ",": '',
            "?": '',
            "/": '',
            "\\": '',
            ":": '',
            "#": '',
            "&": '',
            "(": '',
            ")": '',
            "@": '',
            "[": '',
            "...": '',
            "]": '',
        },
        'ends': {},
        'is': {},

    }

    @staticmethod
    def _preclean_word(word: str) -> str:
        return WordWorks._clean_word(word, WordWorks.PRE)

    @staticmethod
    def _clean_word(word: str, clean_dict: dict) -> str:
        begins = clean_dict['begins']
        contains = clean_dict['contains']
        ends = clean_dict['ends']
        iss = clean_dict['is']
        word = word.lower()
        for begin in begins:
            if word.startswith(begin):
                word = f'{begins[begin]}{word[len(begin):]}'
        for end in ends:
            if word.endswith(end):
                word = f'{word[:-len(end)]}{ends[end]}'
        for contain in contains:
            if word.__contains__(contain):
                word = word.replace(contain, contains[contain])
        for _is in iss:
            if word == _is:
                word = iss[_is]
        return word

    @staticmethod
    def _postclean_word(word: str) -> str:
        return WordWorks._clean_word(word, WordWorks.POST)

    @staticmethod
    def _do_result(item, dictionary):
        item = WordWorks._preclean_word(item)
        if item != '' and item != '-':
            item = WordWorks._postclean_word(item)
            if item != '' and item != '-':
                if dictionary.__contains__(item):
                    dictionary[item] += 1
                else:
                    dictionary.update({item: 1})
        return dictionary

    @staticmethod
    def _do_results(dictionary, items):
        for item in items:
            item = WordWorks._preclean_word(item)
            item_split = item.split(' ')
            for word in item_split:
                dictionary = WordWorks._do_result(word, dictionary)
        return dictionary

    @staticmethod
    def do_dict(results):
        dictionary = {}
        for result in results:
            result = WordWorks._preclean_word(result)
            result_split = result.split(' ')
            dictionary = WordWorks._do_results(dictionary, result_split)
        return dictionary

    @staticmethod
    def _replace_repeating(string: str, char: str, amount: int):
        repeateds = []
        for i in range(amount):
            repeateds.append(char)
        repeated = ''.join(repeateds)
        return string.replace(repeated, f'{char}{char}')

    @staticmethod
    def _check_for_repetition(string: str) -> str:
        last_char = ''
        counter = 0
        replacers = []
        for char in string:
            if last_char == char:
                counter += 1
            else:
                if counter > 2:
                    replacer = [last_char, counter]
                    if not replacers.__contains__(replacer):
                        replacers.append(replacer)
                last_char = char
                counter = 1
        if counter > 2:
            replacer = [last_char, counter]
            if not replacers.__contains__(replacer):
                replacers.append(replacer)

        if len(replacers) > 0:
            for _replacer in replacers:
                string = WordWorks._replace_repeating(string, _replacer[0], _replacer[1])

        return string

    @staticmethod
    def _key_deletes(dictionary: dict, key_list: list) -> dict:
        for key in key_list:
            dictionary.__delitem__(key)
        return dictionary

    @staticmethod
    def _cleanup_dict_repetitioned(dictionary: dict) -> dict:
        keys = dictionary.keys()
        key_deletes = []
        key_list = [_key for _key in keys]
        key_list = sorted(key_list)
        for key in key_list:
            repetitioned = WordWorks._check_for_repetition(key)
            if key != repetitioned:
                if keys.__contains__(repetitioned):
                    dictionary[repetitioned] += dictionary[key]
                else:
                    dictionary[repetitioned] = dictionary[key]
                key_deletes.append(key)
        dictionary = WordWorks._key_deletes(dictionary, key_deletes)
        return dictionary

    @staticmethod
    def _cleanup_dict_singular(string, key_list):
        temp = string
        if string.endswith('es'):
            temp = string[:-2]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ably'):
            temp = f'{string[:-1]}e'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('s'):
            temp = string[:-1]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ted'):
            temp = string[:-2]
            if key_list.__contains__(temp):
                return temp
            temp = string[:-1]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ity'):
            temp = f'{string[:-3]}e'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ily'):
            temp = f'{string[:-3]}y'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ies'):
            temp = f'{string[:-3]}y'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ory'):
            temp = f'{string[:-3]}e'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ves'):
            temp = f'{string[:-3]}f'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ly'):
            temp = string[:-2]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ed'):
            temp = string[:-2]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ive'):
            temp = string[:-3]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ious'):
            temp = f'{string[:-2]}n'
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ions'):
            temp = string[:-1]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ness'):
            temp = string[:-4]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('er'):
            temp = string[:-2]
            if key_list.__contains__(temp):
                return temp
            temp = string[:-1]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ings'):
            temp = string[:-4]
            if key_list.__contains__(temp):
                return temp
        if string.endswith('ing'):
            temp = string[:-3]
            if key_list.__contains__(temp):
                return temp
            temp = f'{string[:-3]}e'
            if key_list.__contains__(temp):
                return temp
        return string

    @staticmethod
    def _cleanup_dict_singularify(dictionary: dict) -> dict:
        keys = dictionary.keys()
        key_deletes = []
        key_list = [_key for _key in keys]
        key_list = sorted(key_list)
        for key in key_list:
            string = WordWorks._cleanup_dict_singular(key, key_list)
            if string != key:
                if key_list.__contains__(string):
                    dictionary[string] += dictionary[key]
                else:
                    dictionary[string] = dictionary[key]
                key_deletes.append(key)
        dictionary = WordWorks._key_deletes(dictionary, key_deletes)
        return dictionary

    @staticmethod
    def do_dicts(resultss):
        dictionary = {}
        for results in resultss:
            for result in results:
                result = WordWorks._preclean_word(result)
                result_split = result.split(' ')
                dictionary = WordWorks._do_results(dictionary, result_split)
        dictionary = WordWorks._cleanup_dict_repetitioned(dictionary)
        dictionary = WordWorks._cleanup_dict_singularify(dictionary)
        return dictionary
