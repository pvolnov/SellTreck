import re
from collections import Counter
import pymorphy2
from app.models.items import Items


class Dictionary:

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    def get_similiar_words(self, text):
        text = re.sub(r'[^а-яa-z\s]+', "", text.replace("\xa0", " ").lower())
        words = re.split(r"\s+", text)
        if len(words) < 2:
            return []
        target = words[-1]
        if len(target) < 2:
            return []
        words = [self.morph.parse(w)[0].normal_form for w in words[:-1]]
        local_dictionary = {}

        options = Items.select(Items.keywords, Items.local_dictionary).where(Items.keywords.contains(words)).limit(120).execute()
        options_words = []
        for o in options:
            local_dictionary.update(o.local_dictionary)
            options_words += o.keywords
        options_words = list(filter(lambda x: re.match("[а-яa-z]+$", x, re.I), options_words))
        counters = Counter(options_words)
        options_words = list(set(options_words))
        sim_words = []

        for w in options_words:
            if re.match(target, w):
                sim_words.append((w, counters[w]))

        sim_words = sorted(sim_words, key=lambda x: x[1], reverse=True)
        sim_words = [r[0] for r in sim_words][:25]

        result = []
        for w in sim_words:
            result.append(local_dictionary[w])

        return result
