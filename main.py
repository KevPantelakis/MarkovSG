import MarkovSG
import random


def main():
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

    print("Names: \n")
    for i in range(0, 5):
        print(gen.get_name(random.randint(3, 9)))

    print("\nWords: \n")
    for i in range(0, 50):
        print(gen.get_word(random.randint(4, 10)))

    print("\nSentences: \n")
    for i in range(0, 5):
        print(gen.get_sentence(random.randint(7, 15)))


def prepare_data():
    strings = list()
    with open("Dictionaries/dictionary.txt") as f:
        words = f.read()
        arr = words.split("\n")
        for word in arr:
            flag = True
            is_all_caps = True
            for char in word:
                if char == "." or char == "/":
                    flag = False
                if 97 <= ord(char) <= 122:
                    is_all_caps = False

            if word[-1] == "-":
                flag = False

            if is_all_caps:
                flag = False

            if flag:
                if 65 <= ord(word[0]) <= 90:
                    if "-" in word:
                        # print(word)
                        w = word.lower()
                        strings.append(w)
                if 97 <= ord(word[0]) <= 122:
                    strings.append(word)

    with open("Dictionaries/words.txt", "w+") as f:
        for string in strings:
            f.write(string+"\n")


if __name__ == "__main__":
    main()
