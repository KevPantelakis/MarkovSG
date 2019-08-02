# MarkovSG
Marcovian chain random senctences, words and names generator
# Code sample
```python
import MarkovSG

# Read text as one giant string
import MarkovSG
import random

sentence_file = open("sample_texts/undersea.txt")
sentences = sentence_file.read()
sentence_file.close()

name_file = open("Dictionaries/names.txt")
names = name_file.read()
name_file.close()

word_file = open("Dictionaries/words.txt")
words = word_file.read()
word_file.close()

gen = MarkovSG.MarkovChainGenerator(text=sentences, names=names, words=words)
######## OR
# gen = MarkovSG.MarkovChainGenerator()
# gen.train_for_sentence(sentences)
# gen.train_for_words(words)
# gen.train_for_names(names)

print("Names: \n")
for i in range(0, 5):
    print(gen.get_name(name_length=random.randint(3, 9)))

print("\nWords: \n")
for i in range(0, 50):
    print(gen.get_word(word_length=random.randint(4, 10)))

print("\nSentences: \n")
for i in range(0, 5):
    print(gen.get_sentence(word_count=random.randint(7, 15)))
```
