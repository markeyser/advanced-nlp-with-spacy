# Import the English language class
from spacy.lang.en import English
# Create the nlp object
nlp = English()
# Craete a doc object

text = open('../Projects/advanced-nlp-with-spacy/code/american.txt', 'r', encoding='utf-8').read()
doc = nlp(text)
# Iterate over tokens
for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)

myfile = open('../Projects/advanced-nlp-with-spacy/code/american.txt')
content = myfile.read()
mylines = myfile.readlines()

for line in mylines:
    print(line.split()[0])

myfile.seek(0)

mylines
content
import os
os.getcwd()
os.chdir('/Users/marcosaguilerakeyser/Projects/advanced-nlp-with-spacy')
os.getcwd()
