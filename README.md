# MarkovSG
Marcovian chain random senctence generator
#Code sample
```python
import MarkovSG

# Read text as one giant string
with open("/path/to/my/sample_text.txt") as f:
    text = f.read()

# instanciate the sentence generator
generator = MarkovSG.MarkovGenerator(text)

# Print randomly-generated sentences
for i in range(0, 7):
    print(generator.get_sentence())

# Print randomly-generated 15 words sentences 
for i in range(0, 3):
    print(generator.get_sentence(15))
```