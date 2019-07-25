import numpy as np
import re
from collections import defaultdict

class MarkovGenerator(object):
    def __init__(self, seed_text):
        self.first_words = self.get_first_words(seed_text)
        self.text_tokens = self.get_text_tokens(seed_text)
        self.markov_graph = self.get_markov_graph(self.text_tokens)

    def get_text_tokens(self, seed_text):
        return [word for word in re.split(r"[^\w']+", seed_text) if word != '']

    def get_first_words(self, seed_text):
        first_words = list()
        for sentence in re.split(r"[.]+", seed_text):
            if sentence != '' and sentence != '..' and sentence != '\n' and sentence != '\n- ':
                words = [word for word in re.split(r"[^\w']+", sentence) if word != '']
                if len(words) > 0:
                    if words[0] not in first_words:
                        first_words.append(words[0].lower())
        return first_words

    def get_markov_graph(self, tokens):
        markov_graph = defaultdict(lambda: defaultdict(int))
        last_word = tokens[0].lower()
        for word in tokens[1:]:
            word = word.lower()
            markov_graph[last_word][word] += 1
            last_word = word
        return markov_graph

    def walk_graph(self, distance=10, start_node=None):
        if distance <= 0:
            return []

        if not start_node:
            start_node = np.random.choice(list(self.markov_graph.keys()))

        weights = np.array(list(self.markov_graph[start_node].values()), dtype=np.float64)
        weights /= weights.sum()
        choices = list(self.markov_graph[start_node].keys())
        chosen_word = np.random.choice(choices, None, p=weights)
        return [chosen_word] + self.walk_graph(distance=distance - 1, start_node=chosen_word)

    def get_sentence(self, word_count=None):
        if word_count is None:
            word_count = np.random.randint(10, 20)

        if len(self.markov_graph) <= word_count:
            return None
        begin_node = np.random.choice(self.first_words)
        sentence_start = begin_node[0].upper() + begin_node[1:]
        sentence = sentence_start + ' ' + ' '.join(self.walk_graph(distance=word_count-1, start_node=begin_node))
        sentence = sentence + '.\n'
        return sentence
