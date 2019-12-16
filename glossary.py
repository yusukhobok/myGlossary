from words_processing import words_processing

class Text():
    def __init__(self, FileName = None):
        self.authors = None
        self.caption = None
        self.year = None
        self.data = None
        self.text = None
        self.textInfo = None
        self.mark = []
        self.coef = 1.0
        if FileName:
            self.importText(FileName)

    def __str__(self):
        return '%s%s_%s' % (self.authors, self.year, self.caption[:5])


    def initOneParagraph(self, sentencesCount):
        self.textInfo = [{"paragraph": self.text, "sentencesInfo": [{"pairs": [{"sentence": "", "wordsInfo": [], "lineOfWords": None}, {"sentence": "", "wordsInfo": [], "lineOfWords": None}], "correspondences": [],"tags": []} for i in range(sentencesCount)]}]


    def getSentencesCount(self):
        k = 0
        for paragraph in self.textInfo:
            for sentence in paragraph["sentencesInfo"]:
                k+=1
        return k


    def importText(self, FileName):
        f = open(FileName, "r", encoding="utf8", errors='ignore')
        self.authors = f.readline()
        self.caption = f.readline()
        self.year = f.readline()
        self.data = f.readline()
        self.text = f.read()
        self.transformText()
        self.calculate()


    def transformText(self):
        self.textInfo = []
        paragraphs = self.text.split("\n")
        paragraphs = [paragraph for paragraph in paragraphs if paragraph != ""]
        for (k, paragraph) in enumerate(paragraphs):
            print("%d абзац из %d" % (k+1, len(paragraphs)))
            sentences = words_processing.paragraphToSenetences(paragraph)
            sentencesInfo = []
            for (e, sentence) in enumerate(sentences):
                print("%d предложение из %d" % (e + 1, len(sentences)))
                words = words_processing.sentencesToWords(sentence)
                wordsInfo = []
                for word in words:
                    normalWord = words_processing.getEnglishNormalForm(word)
                    # normalWord = word
                    wordsInfo.append({"currentWord": word, "normalWord": normalWord, "isMain": True})
                if len(wordsInfo)>0:
                    sentencesInfo.append({"pairs":
                                              [{"sentence": sentence, "wordsInfo": wordsInfo, "lineOfWords": None},
                                               {"sentence": "", "wordsInfo": [], "lineOfWords": None}],
                                          "correspondences": [],
                                          "tags": []})
            if len(sentencesInfo)>0:
                self.textInfo.append(({"paragraph": paragraph, "sentencesInfo": sentencesInfo}))


    def setSentence(self, paragraphNum, sentenceNum, sentence):
        words = words_processing.sentencesToWords(sentence)
        wordsInfo = []
        for word in words:
            normalWord = words_processing.getEnglishNormalForm(word)
            # normalWord = word
            wordsInfo.append({"currentWord": word, "normalWord": normalWord, "isMain": True})
        if len(wordsInfo) == 0: return

        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["pairs"][0]["sentence"] = sentence
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["pairs"][0]["wordsInfo"] = wordsInfo
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["pairs"][0]["lineOfWords"] = None
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["correspondences"] = []


    def setTranslation(self, paragraphNum, sentenceNum, translation):
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["pairs"][1]["sentence"] = translation
        words = words_processing.sentencesToWords(translation)
        translationWordsInfo = []
        for word in words:
            normalWord = words_processing.getRussianNormalForm(word)
            #normalWord = word
            translationWordsInfo.append({"currentWord": word, "normalWord": normalWord, "isMain": True})
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["pairs"][1]["wordsInfo"] = translationWordsInfo
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["pairs"][1]["lineOfWords"] = None
        self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]["correspondences"] = []


    def calculate(self):
        for (k, paragraphInfo) in enumerate(self.textInfo):
            print("%d абзац из %d" % (k+1, len(self.textInfo)))
            for (e, sentenceInfo) in enumerate(paragraphInfo["sentencesInfo"]):
                print("%d предложение из %d" % (e + 1, len(paragraphInfo["sentencesInfo"])))
                for wordInfo in sentenceInfo["pairs"][0]["wordsInfo"]:
                    wordInfo["isMain"] = words_processing.isEnglishMainWord(wordInfo["currentWord"])
                sentenceInfo["pairs"][0]["lineOfWords"] = " ".join([wordInfo["currentWord"] for wordInfo in sentenceInfo["pairs"][0]["wordsInfo"]])

                for wordInfo in sentenceInfo["pairs"][1]["wordsInfo"]:
                    wordInfo["isMain"] = words_processing.isRussianMainWord(wordInfo["currentWord"])
                sentenceInfo["pairs"][1]["lineOfWords"] = " ".join([wordInfo["currentWord"] for wordInfo in sentenceInfo["pairs"][1]["wordsInfo"]])


    def calculateSentence(self, paragraphNum, sentenceNum):
        sentenceInfo = self.textInfo[paragraphNum]["sentencesInfo"][sentenceNum]
        for wordInfo in sentenceInfo["pairs"][0]["wordsInfo"]:
            wordInfo["isMain"] = words_processing.isEnglishMainWord(wordInfo["currentWord"])
        sentenceInfo["pairs"][0]["lineOfWords"] = " ".join([wordInfo["currentWord"] for wordInfo in sentenceInfo["pairs"][0]["wordsInfo"]])

        for wordInfo in sentenceInfo["pairs"][1]["wordsInfo"]:
            wordInfo["isMain"] = words_processing.isRussianMainWord(wordInfo["currentWord"])
        sentenceInfo["pairs"][1]["lineOfWords"] = " ".join([wordInfo["currentWord"] for wordInfo in sentenceInfo["pairs"][1]["wordsInfo"]])



    def delDuplicates(self):
        Pairs = []

        for (k, paragraphInfo) in enumerate(self.textInfo):
            print("%d абзац из %d" % (k+1, len(self.textInfo)))
            newSentencesInfo = []
            for (e, sentenceInfo) in enumerate(paragraphInfo["sentencesInfo"]):
                print("%d предложение из %d" % (e + 1, len(paragraphInfo["sentencesInfo"])))

                eng = sentenceInfo["pairs"][0]["sentence"]
                rus = sentenceInfo["pairs"][1]["sentence"]
                pair = (eng, rus)
                if pair not in Pairs:
                    Pairs.append(pair)
                    print(pair)
                    newSentencesInfo.append(sentenceInfo)
            paragraphInfo["sentencesInfo"] = newSentencesInfo


    def getSentenceWithoutTranslation(self, parNum, sentNum):
        for (i, paragraphInfo) in enumerate(self.textInfo[parNum:]):
            for (j, sentenceInfo) in enumerate(paragraphInfo["sentencesInfo"]):
                if (i>parNum) or ((i==parNum) and (j>sentNum)):
                    if sentenceInfo["pairs"][1]["sentence"] == "":
                        return (i, j)
        return (None, None)


    def getSentenceWithoutTags(self, parNum, sentNum):
        for (i, paragraphInfo) in enumerate(self.textInfo[parNum:]):
            for (j, sentenceInfo) in enumerate(paragraphInfo["sentencesInfo"]):
                if (i>parNum) or ((i==parNum) and (j>sentNum)):
                    if len(sentenceInfo["tags"]) == 0:
                        return (i, j)
        return (None, None)


    def getSentenceWithoutCorrespondences(self, parNum, sentNum):
        for (i, paragraphInfo) in enumerate(self.textInfo[parNum:]):
            for (j, sentenceInfo) in enumerate(paragraphInfo["sentencesInfo"]):
                if (i>parNum) or ((i==parNum) and (j>sentNum)):
                    if sentenceInfo["pairs"][1]["sentence"] != "":
                        if len(sentenceInfo["correspondences"]) == 0:
                            return (i, j)
        return (None, None)



    def delNotEnglishSentences(self):
        import re
        Data = []
        for j, paragraphInfo in enumerate(self.textInfo):
            for k, sentenceInfo in enumerate(paragraphInfo["sentencesInfo"]):
                eng = len(re.findall("[A-Za-zА-Яа-я0-9_\-'`]", sentenceInfo["pairs"][0]["sentence"]))
                not_eng = len(re.findall("[^A-Za-zА-Яа-я0-9_\-'`]",sentenceInfo["pairs"][0]["sentence"]))
                koef = not_eng/(eng+not_eng)
                n = len(sentenceInfo["pairs"][0]["sentence"])
                if (n > 50) and (koef>0.5):
                    Data.append({"koef": koef, "num_paragraph": j, "num_sentence": k})

        def sortByNumber(el):
            return  el["num_paragraph"]*10000 + el["num_sentence"]
        Data.sort(key=sortByNumber, reverse=True)
        for el in Data:
            print(el)
            j = el["num_paragraph"]
            k = el["num_sentence"]
            del (self.textInfo[j]["sentencesInfo"][k])




    # def cut(self):
    #     for j, paragraphInfo in enumerate(self.textInfo):
    #         for k, sentenceInfo in enumerate(paragraphInfo["sentencesInfo"]):
    #             print("%d из %d" % (k + 1, len(paragraphInfo["sentencesInfo"])))
    #             if k < 8800: break
    #             if len(sentenceInfo["correspondences"]) == 0:
    #                 for wordInfo in sentenceInfo["pairs"][0]["wordsInfo"]:
    #                     normalWord = wordInfo["normalWord"]
    #                     if not words_processing.isEnglishMainWord(normalWord):
    #                         del(wordInfo)
    #
    #                 for wordInfo in sentenceInfo["pairs"][1]["wordsInfo"]:
    #                     normalWord = wordInfo["normalWord"]
    #                     if not words_processing.isRussianMainWord(normalWord):
    #                         del(wordInfo)
    #     self.printData()



    def printData(self):
        print("Авторы:", self.authors)
        print("Заглавие:", self.caption)
        print("Год:", self.year)
        print("Выходные данные:", self.data)
        for (i, paragraphInfo) in enumerate(self.textInfo):
            print("%d абзац" % i)
            for (j, sentencesInfo) in enumerate(paragraphInfo["sentencesInfo"]):
                print("\t%d.%d предложение" % (i,j))
                for element in sentencesInfo["pairs"]:
                    print("\t\t%s" % element["sentence"])
                    for (k, wordsInfo) in enumerate(element["wordsInfo"]):
                        print("\t\t%d: %s - %s - %r" % (k, wordsInfo["currentWord"], wordsInfo["normalWord"], wordsInfo["isMain"]))
                    if element["lineOfWords"] is not None:
                        print("\t\tlineOfWords: %s" % element["lineOfWords"])

                # print("\tcorrespondences: ", sentencesInfo["correspondences"])
                # print("\ttags: ", sentencesInfo["tags"])








