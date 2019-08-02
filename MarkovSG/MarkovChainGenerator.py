import numpy as np
import re
import random
from collections import defaultdict


class MarkovChainGenerator(object):
    def __init__(self, text=None, names=None, words=None):
        self.first_words = None
        self.markov_sentence_graph = None
        self.markov_name_graph = None
        self.markov_word_graph = None
        if text is not None:
            self.train_for_sentence(text)
        if names is not None:
            self.train_for_names(names)
        if words is not None:
            self.train_for_words(words)

    def train_for_sentence(self, text):
        if text is None:
            raise Exception('Must provide a text(a long book in a single string) to train the generator')
        self.__populate_first_words(text)
        tokens = self.__get_text_tokens(text)
        markov_graph = defaultdict(lambda: defaultdict(int))
        last_word = tokens[0].lower()
        for word in tokens[1:]:
            word = word.lower()
            markov_graph[last_word][word] += 1
            last_word = word
        self.markov_sentence_graph = markov_graph

    def train_for_names(self, names):
        if names is None:
            raise Exception('Must provide a name list(as a string txt file) to train the generator')
        self.markov_name_graph = self.__get_trained_markov(names)

    def train_for_words(self, words):
        if words is None:
            raise Exception('Must provide a words list(as a string txt file(all lower) to train the generator')
        self.markov_word_graph = self.__get_trained_markov(words)

    def __walk_graph(self, graph, distance=10, start_node=None):
        if distance <= 0:
            return []

        if not start_node:
            start_node = np.random.choice(list(graph.keys()))

        weights = np.array(list(graph[start_node].values()), dtype=np.float64)
        weights /= weights.sum()
        choices = list(graph[start_node].keys())
        chosen_word = np.random.choice(choices, None, p=weights)
        return [chosen_word] + self.__walk_graph(graph, distance=distance - 1, start_node=chosen_word)

    def get_sentence(self, word_count=None):
        if self.markov_sentence_graph is None:
            raise Exception('The generator must be trained for sentences before generating them')

        if word_count is None:
            word_count = np.random.randint(10, 20)

        if len(self.markov_sentence_graph) <= word_count:
            return None
        begin_node = np.random.choice(self.first_words)
        sentence_start = begin_node[0].upper() + begin_node[1:]
        sentence = sentence_start + ' ' + ' '.join(self.__walk_graph(self.markov_sentence_graph, distance=word_count - 1,
                                                                     start_node=begin_node))
        sentence = sentence + '.\n'
        return sentence

    def get_name(self, name_length=None):
        if self.markov_name_graph is None:
            raise Exception('The generator must be trained for names before generating them')
        name = self.__get_word(self.markov_name_graph, name_length, chr(random.randint(65, 90)))
        return name

    def get_word(self,word_length=None):
        if self.markov_word_graph is None:
            raise Exception('The generator must be trained for words before generating them')
        name = self.__get_word(self.markov_word_graph, word_length, chr(random.randint(97, 122)))
        return name

    def __get_word(self, graph, length, begin_node):
        if len(graph) <= length:
            raise Exception('Not enough training data')
        if length is None or length <= 0:
            length = np.random.randint(2, 15)
        word = begin_node + ''.join(self.__walk_graph(graph=graph, distance=length - 1, start_node=begin_node))
        return word

    def __get_text_tokens(self, seed_text):
        return [word for word in re.split(r"[^\w']+", seed_text) if word != '']

    def __populate_first_words(self, seed_text):
        first_words = list()
        for sentence in re.split(r"[.]+", seed_text):
            if sentence != '' and sentence != '..' and sentence != '\n' and sentence != '\n- ':
                words = [word for word in re.split(r"[^\w']+", sentence) if word != '']
                if len(words) > 0:
                    if words[0] not in first_words:
                        first_words.append(words[0].lower())
        self.first_words = first_words

    def __get_trained_markov(self, words):
        words_tokens = words.split("\n")
        markov_graph = defaultdict(lambda: defaultdict(int))
        for word in words_tokens:
            last_char = word[0]
            for char in word[1:]:
                markov_graph[last_char][char] += 1
                last_char = char
        return markov_graph
