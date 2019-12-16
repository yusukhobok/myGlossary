import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


# paragraph = """All deteriorate Fig. 1 with.  Also, natural by et al. visual inspection. There Sect. are corrosion, etc. the examples. """
# from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
# punkt_param = PunktParameters()
# punkt_param.abbrev_types = set(['fig', 'etc', 'e', 'e.g', 'al', 'sect', 'chap'])
# sentence_splitter = PunktSentenceTokenizer(punkt_param)
# sentences = sentence_splitter.tokenize(paragraph)
# print(sentences)

# import finder
# Finder = finder.Finder("D:\\Programs\\myGlossary\\data\\")
# Finder.getNotEnglishSentences()




#
# word = "done"
#
# from nltk.corpus import wordnet
# def get_wordnet_pos(treebank_tag):
#     if treebank_tag.startswith('J'):
#         return wordnet.ADJ
#     elif treebank_tag.startswith('V'):
#         return wordnet.VERB
#     elif treebank_tag.startswith('N'):
#         return wordnet.NOUN
#     elif treebank_tag.startswith('R'):
#         return wordnet.ADV
#     else:
#         return ''
# from nltk import pos_tag
# tag = pos_tag([word])
# tag = get_wordnet_pos(tag[0][1])
#
# from nltk.stem import WordNetLemmatizer
# lemmatizer = WordNetLemmatizer()
# normalWord = lemmatizer.lemmatize(word, pos=tag)
# print(normalWord)


# S = "  "
# P = S.strip()
# print(P)

