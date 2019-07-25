import unittest
import re
import MarkovSG
with open("../sample_texts/undersea.txt") as f:
    undersea = f.read()
    markov_gen = MarkovSG.MarkovGenerator(undersea)


class MarkovSGTest(unittest.TestCase):

    def test_generator(self):
        generator = markov_gen
        sentence = generator.get_sentence()
        assert(len(sentence) > 0)

    def test_word_count(self):
        generator = markov_gen
        sentence = generator.get_sentence(20)
        count = len([word for word in re.split(r"[^\w']+", sentence) if word != ''])
        assert(count == 20)

    def test_seed_text_too_small(self):
        seed_text = "I'm a small text. This is one sentence."
        generator = MarkovSG.MarkovGenerator(seed_text)
        sentence = generator.get_sentence()
        assert(sentence is None)


if __name__ == '__main__':
    unittest.main()
