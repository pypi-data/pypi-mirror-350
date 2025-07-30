from typing import Union

import h5py  # type: ignore
import numpy as np

from . import asynchronous, func


class RandomReplaceText:
    def __init__(self):
        self.digit = np.array(list('0123456789'))
        self.lowercase = np.array(list('abcdefghijklmnopqrstuvwxyz'))
        self.uppercase = np.array(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        ranges = (0x4E00, 0x9FFF), (0x3400, 0x4DBF)
        self.cjk = np.array(func.flatten([list(range(*x)) for x in ranges]))

    def __call__(self, text, prob=0.1):
        def random_replace_character(char):
            if char == ' ' or np.random.ranf() > prob:
                return char
            if '0' <= char <= '9':
                char = np.random.choice(self.digit)
            elif 'a' <= char <= 'z':
                char = np.random.choice(self.lowercase)
            elif 'A' <= char <= 'Z':
                char = np.random.choice(self.uppercase)
            else:
                char = chr(np.random.choice(self.cjk))
            return char

        result = ''
        for ch in text:
            result += random_replace_character(ch)
        return result


class RandomText:
    def __init__(self, chars, random_prob, minlen=5, maxlen=20):
        self._chars = chars if isinstance(chars, np.ndarray) else np.array(list(chars))
        self.random_prob = random_prob
        self._minlen = minlen
        self._maxlen = maxlen

    def __call__(self, text, size):
        if size is None:
            return self.__generate(text, 1)[0]
        else:
            return self.__generate(text, size)

    def __generate(self, text, size):
        if text is not None and size == 1 and np.random.ranf() > self.random_prob:
            return [text]
        texts = []
        for _ in range(size):
            size = np.random.randint(self._minlen, self._maxlen + 1)
            text = ''.join(np.random.choice(self._chars, size=size))
            texts.append(text)
        return texts


class RandomTextWithCorpus:
    @staticmethod
    def language_set(profile):
        if profile == 'en-zh':
            return {'en': 0.4, 'zh-cn': 0.4, 'zh-tw': 0.2}
        elif profile == 'all':
            return None
        else:
            return None

    def __init__(self, corpus, profile='all'):
        file = h5py.File(corpus, 'r')
        self.sentences = file['data']
        self.profile = __class__.language_set(profile) if isinstance(profile, str) else profile

    def __call__(self, size=None, language=None):
        if size is None:
            return self.__generate(1, language=language)[0]
        else:
            return self.__generate(size, language=language)

    def __generate(self, size, language: Union[str, list] | None = None):
        if language is not None:
            languages = [language] if isinstance(language, str) else language
            languages = np.random.choice(languages, size=size)
        elif self.profile is not None:
            languages = np.random.choice(
                list(self.profile.keys()),
                p=list(self.profile.values()),
                size=size,
            )
        else:
            languages = np.random.choice(list(self.sentences), size=size)
        result = []
        for language in languages:
            size = len(self.sentences[language])
            index = np.random.choice(size)
            sentence = RandomTextWithCorpus.__decode(self.sentences[language][index])
            result.append(sentence)
        return result

    @staticmethod
    def __decode(x):
        return x if isinstance(x, str) else x.decode('utf-8')


class RandomTextProducer(asynchronous.DataProducer):
    def __init__(self, random_text, minsize=100, maxsize=3000):
        super(__class__, self).__init__(minsize, maxsize)
        self.random_text = random_text

    def _produce(self):
        texts = self.random_text(size=10)
        self.put(texts)
