
# Import the English language class
from spacy.lang.en import English

# Create the nlp object
nlp = English()
# Craete a doc object
doc = nlp("Too often the answer to this question resembles the plot of a sci-fi thriller.")
# Iterate over tokensin a doc
for token in doc:
    print(token.text)
# Index into the Doc to get a single token
token = doc[1]
token
# Create a Span
span = doc[1:5]
print(span.text)
# let's get the index of the token
print('Index: ', [token.i for token in doc])
# Other lexical attributes of the Doc object
print([token.is_alpha for token in doc])
print([token.is_punct for token in doc])
print([token.like_num for token in doc])
for token in doc:
    # Check if the token resembles a punctuation
    if token.is_punct:
        # Get the token in the document
        token = doc[token.i]
        # Check if the token's text equals `-`
        if token.text == '-':
            # Print the number token's token SystemExit
            print('Iphone found: ', token.text)

# spaCy statisticall models
# Import spacy
import spacy
# Load the small English models
nlp = spacy.load('en_core_web_sm')
# Proess a text
doc = nlp("Too often the answer to this question resembles the plot of a sci-fi thriller.")
# Iterate over tokens
for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)

from spacy import displacy
displacy.serve(doc, style='dep')

import io

text = open('../Projects/advanced-nlp-with-spacy/code/nyt-text.txt', 'r', encoding='utf-8').read()
doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)
spacy.explain('GPE')



import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
# add match ID "HelloWorld" with no callback and one pattern
pattern = [[{'LOWER': 'hello'}, {'IS_PUNCT': True}, {'LOWER': 'world'}], [{'LOWER': 'hello'}, {'LOWER': 'world'}]]
matcher.add('HelloWorld', None, [[{'LOWER': 'hello'}, {'IS_PUNCT': True}, {'LOWER': 'world'}], [{'LOWER': 'hello'}, {'LOWER': 'world'}]])

doc = nlp(u'Hello, world! Hello world!')
matches = matcher(doc)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id] # get string representation
    span = doc[start:end] # the matched Span
    print(match_id, string_id, start, end, span.text)


import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')
matcher = PhraseMatcher(nlp.vocab)
terminology_list = ['Barack Obama', 'Angela Merkel', 'Washington, D.C.']
# Only run nlp.make_doc to speed things up
patterns = [nlp.make_doc(text) for text in terminology_list]
matcher.add('TerminologyList', None, *patterns)

doc = nlp(u"German Chancellor Angela Merkel and US President Barack Obama "
          u"converse in the Oval Office inside the White House in Washington, D.C.")
matches = matcher(doc)
for match_id, start, end in matches:
    span = doc[start:end]
    print(span.text)
