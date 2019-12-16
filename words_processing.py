from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk import pos_tag
import pymorphy2



class WordsProcessing():
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.rus_morph = pymorphy2.MorphAnalyzer()

        self.punkt_param = PunktParameters()
        self.punkt_param.abbrev_types = set(['fig', 'etc', 'al', 'sect', 'chap', 'eqs'])
        self.sentence_splitter = PunktSentenceTokenizer(self.punkt_param)


    def paragraphToSenetences(self, paragraph):
        sentences = self.sentence_splitter.tokenize(paragraph)
        return sentences


    def getWordnetPos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN


    def sentencesToWords(self, sentence):
        import re
        words = re.split("[^A-Za-zА-Яа-я_\-'`]+", sentence)
        words = [word.strip() for word in words]
        words = [word.lower() for word in words if word != ""]
        words = [word for word in words if re.search("[^A-Za-zА-Яа-я\-'`]", word) is None]
        return words


    def getEnglishNormalForm(self, word):
        treebank_tag = pos_tag([word])
        tag = self.getWordnetPos(treebank_tag[0][1])
        normalWord = self.lemmatizer.lemmatize(word, pos=tag)
        return normalWord


    def isEnglishMainWord(self, word):
        treebank_tag = pos_tag([word])[0][1]
        f = not ((treebank_tag == "IN") or (treebank_tag == "DT") or (treebank_tag == "TO"))
        return f


    def getRussianNormalForm(self, word):
        p = self.rus_morph.parse(word)[0]
        normalWord = p.normal_form
        return normalWord


    def isRussianMainWord(self, word):
        p = self.rus_morph.parse(word)[0]
        pos = p.tag.POS
        return not ((pos == "PREP") or (pos == "CONJ") or (pos == "PRCL") or (pos == "INTJ"))


words_processing = WordsProcessing()


