from words_processing import words_processing

class Finder():
    def __init__(self, Path):
        self.Path = Path
        self.Glossaries = []
        self.setGlossaries()
        self.index = None
        self.loadIndex()


    def setGlossaries(self):
        import os
        self.Glossaries = []
        for file in os.listdir(self.Path):
            if file.endswith(".gls"):
                FileName = os.path.join(self.Path, file)
                print(FileName)
                import pickle
                f = open(FileName, "rb")
                self.Glossaries.append(pickle.load(f))


    def getTags(self):
        tags = []
        for glossary in self.Glossaries:
            for paragraphInfo in glossary.textInfo:
                for sentencesInfo in paragraphInfo["sentencesInfo"]:
                    for tag in sentencesInfo["tags"]:
                        if not (tag in tags):
                            tags.append(tag)
        return sorted(tags)


    def getSources(self):
        sources = []
        for (i, glossary) in enumerate(self.Glossaries):
            sources.append('%d. %s, %s' % (i+1, glossary.authors.replace("\n", ""), glossary.year.replace("\n", "")))
        return sources


    def getEnglishNormalWords(self, words):
        normalWords = []
        for word in words:
            normalWord = words_processing.getEnglishNormalForm(word)
            normalWords.append(normalWord)
        return normalWords


    def getRussianNormalWords(self, words):
        normalWords = []
        for word in words:
            normalWord = words_processing.getRussianNormalForm(word)
            normalWords.append(normalWord)
        return normalWords


    def find(self, query, isEnglish = False, tag = None, source = None):
        if (query.strip() == "") and (tag is None) and (source is None): return None

        queryWords = words_processing.sentencesToWords(query)
        queryLine = " ".join(queryWords)

        queryMainWords = list(set(queryWords))
        queryNotMainWords = list(set(queryWords))
        if isEnglish:
            queryWordsNormal = self.getEnglishNormalWords(queryWords)
            queryMainWords = [word for word in queryMainWords if words_processing.isEnglishMainWord(word)]
            queryMainWords = list(zip(queryMainWords, self.getEnglishNormalWords(queryMainWords)))
            queryNotMainWords = [word for word in queryNotMainWords if not words_processing.isEnglishMainWord(word)]
            queryNotMainWords = list(zip(queryNotMainWords, self.getEnglishNormalWords(queryNotMainWords)))
        else:
            queryWordsNormal = self.getRussianNormalWords(queryWords)
            queryMainWords = [word for word in queryMainWords if words_processing.isRussianMainWord(word)]
            queryMainWords = list(zip(queryMainWords, self.getRussianNormalWords(queryMainWords)))
            queryNotMainWords = [word for word in queryNotMainWords if not words_processing.isRussianMainWord(word)]
            queryNotMainWords = list(zip(queryNotMainWords, self.getRussianNormalWords(queryNotMainWords)))


        if isEnglish: t = 0
        else: t = 1

        Results = []
        for (ng,glossary) in enumerate(self.Glossaries):
            if (source == None) or (source == ng):
                for i, paragraphInfo in enumerate(glossary.textInfo):
                    for j, sentenceInfo in enumerate(paragraphInfo["sentencesInfo"]):
                        if (tag is not None) and (tag not in sentenceInfo["tags"]): break
                        # if isEnglish and sentenceInfo["pairs"][1]["sentence"] == "": break

                        findingWords = []
                        findingWordsNormal = []
                        S = sentenceInfo["pairs"][t]["lineOfWords"]
                        if S is not None:
                            if query.strip() == "":
                                coef = 1
                            else:
                                p = S.find(queryLine)
                                S2 = " " + S + " "
                                p1 = S2.find(queryLine)
                                p2 = p1 + len(queryLine)
                                if (p!=-1) and (S2[p1-1] == " ") and (S2[p2] == " "):
                                    #Точное вхождение запроса в предложение
                                    coef = 2 + len(queryLine) / len(S)
                                    findingWords = list(set(queryWords))
                                    findingWordsNormal = list(set(queryWordsNormal))
                                    isExact = True
                                else:
                                    isExact = False
                                    #Поиск по главным словам
                                    if len(queryMainWords) == 0:
                                        coef = 0
                                    else:
                                        k = 0
                                        for queryMainWord in queryMainWords:
                                            for wordInfo in sentenceInfo["pairs"][t]["wordsInfo"]:
                                                if wordInfo["isMain"]:
                                                    if queryMainWord[0] == wordInfo["currentWord"]:
                                                        if queryMainWord[1] not in findingWordsNormal:
                                                            findingWords.append(queryMainWord[0])
                                                            findingWordsNormal.append(queryMainWord[1])
                                                            k += 1

                                        for queryMainWord in queryMainWords:
                                            for wordInfo in sentenceInfo["pairs"][t]["wordsInfo"]:
                                                if wordInfo["isMain"]:
                                                    if queryMainWord[1] == wordInfo["normalWord"]:
                                                        if queryMainWord[1] not in findingWordsNormal:
                                                            findingWords.append(queryMainWord[0])
                                                            findingWordsNormal.append(queryMainWord[1])
                                                            k += 0.7

                                        coef = k / len(queryMainWords)


                                    k = 0
                                    for queryNotMainWord in queryNotMainWords:
                                        for wordInfo in sentenceInfo["pairs"][t]["wordsInfo"]:
                                            if wordInfo["isMain"]:
                                                if queryNotMainWord[0] == wordInfo["currentWord"]:
                                                    if queryNotMainWord[1] not in findingWordsNormal:
                                                        findingWords.append(queryNotMainWord[0])
                                                        findingWordsNormal.append(queryNotMainWord[1])
                                                        k += 0.1

                                    for queryNotMainWord in queryNotMainWords:
                                        for wordInfo in sentenceInfo["pairs"][t]["wordsInfo"]:
                                            if wordInfo["isMain"]:
                                                if queryNotMainWord[1] == wordInfo["normalWord"]:
                                                    if queryNotMainWord[1] not in findingWordsNormal:
                                                        findingWords.append(queryNotMainWord[0])
                                                        findingWordsNormal.append(queryNotMainWord[1])
                                                        k += 0.07

                                    coef += k / len(queryMainWords)


                                    #Поиск по неглавным словам

                            if coef >= 0.6:
                                # Впереди должны быть предложения с переводом
                                if isEnglish and sentenceInfo["pairs"][1]["sentence"] != "":
                                    coef += 10
                                try:
                                    coef *= self.Glossaries[ng].coef
                                except AttributeError:
                                    pass

                                if isEnglish:
                                    S1 = "englishNums"
                                    S2 = "russianNums"
                                else:
                                    S1 = "russianNums"
                                    S2 = "englishNums"

                                FirstNums = []
                                SecondNums = []
                                for findingWord, findingWordNormal in zip(findingWords, findingWordsNormal):
                                    # if isEnglish:
                                    #     findingWordNormal = words_processing.getEnglishNormalForm(findingWord)
                                    # else:
                                    #     findingWordNormal = words_processing.getRussianNormalForm(findingWord)

                                    wordNum = -1
                                    for e, wordInfo in enumerate(sentenceInfo["pairs"][t]["wordsInfo"]):
                                        if findingWordNormal == wordInfo["normalWord"]:
                                            wordNum = e
                                            break
                                    if wordNum!=-1:
                                        correspondenceNum = -1
                                        for e, correspondence in enumerate(sentenceInfo["correspondences"]):
                                            if wordNum in correspondence[S1]:
                                                correspondenceNum = e
                                                break
                                        if correspondenceNum != -1:
                                            FirstNums.extend(sentenceInfo["correspondences"][correspondenceNum][S1])
                                            SecondNums.extend(sentenceInfo["correspondences"][correspondenceNum][S2])

                                def generateSentence(Nums, t, findingWordsNormal):
                                    start = 0
                                    GenSentence = sentenceInfo["pairs"][t]["sentence"]
                                    GenSentence_lower = sentenceInfo["pairs"][t]["sentence"].lower()
                                    for e, wordInfo in enumerate(sentenceInfo["pairs"][t]["wordsInfo"]):
                                        word = wordInfo["currentWord"]
                                        p1 = GenSentence_lower.find(word, start)
                                        p2 = p1 + len(word)
                                        if e in Nums:
                                            GenSentence_lower = GenSentence_lower[:p1] + "<b>" + word + "</b>" + GenSentence_lower[p2:]
                                            GenSentence = GenSentence[:p1] + "<b>" + GenSentence[p1:p2] + "</b>" + GenSentence[p2:]
                                            start = p1 + len("<b>" + word + "</b>")
                                        elif wordInfo["normalWord"] in findingWordsNormal:
                                            GenSentence_lower = GenSentence_lower[:p1] + "<b>" + word + "</b>" + GenSentence_lower[p2:]
                                            GenSentence = GenSentence[:p1] + "<b>" + GenSentence[p1:p2] + "</b>" + GenSentence[p2:]
                                            start = p1 + len("<b>" + word + "</b>")
                                        else:
                                            start = p2
                                    return GenSentence

                                FirstNums = list(set(FirstNums))
                                SecondNums = list(set(SecondNums))

                                FirstSentence = generateSentence(FirstNums, t, findingWordsNormal)
                                SecondSentence = generateSentence(SecondNums, 1 - t, [])
                                # if len(FirstNums) > 0:
                                #     FirstSentence = generateSentence(FirstNums, t, findingWordsNormal)
                                # else:
                                #     FirstSentence = sentenceInfo["pairs"][t]["sentence"]
                                # if len(SecondNums) > 0:
                                #     SecondSentence = generateSentence(SecondNums, 1-t, findingWordsNormal)
                                # else:
                                #     SecondSentence = sentenceInfo["pairs"][1-t]["sentence"]

                                if isEnglish:
                                    englishSentence = FirstSentence
                                    russianSentence = SecondSentence
                                else:
                                    russianSentence = FirstSentence
                                    englishSentence = SecondSentence

                                Results.append({"glossary": glossary, "ParagraphNum": i, "SentenceNum": j, "coef": coef,
                                                "englishSentence": englishSentence, "russianSentence": russianSentence})


        def sortByCoef(el):
            return el["coef"]

        Results.sort(key=sortByCoef, reverse=True)
        return Results


    # def cut(self):
    #     for i, glossary  in enumerate(self.Glossaries):
    #         print("%d of %d" % (i+1, len(self.Glossaries)))
    #         glossary.cut()



    def loadIndex(self):
        import os
        if os.path.exists(self.Path+"\\__index"):
            import pickle
            f = open(self.Path+"\\__index", "rb")
            self.index = pickle.load(f)
        else:
            self.setIndex()


    def findInIndex(self, selection):
        import re
        eng = re.findall("[A-Za-z]", selection)
        rus = re.findall("[А-Яа-я]", selection)
        isEnglish = eng > rus

        selectionWords = words_processing.sentencesToWords(selection)
        selectionNormalWords = []
        for word in selectionWords:
            if isEnglish:
                selectionNormalWords.append(words_processing.getEnglishNormalForm(word))
            else:
                selectionNormalWords.append(words_processing.getRussianNormalForm(word))

        if isEnglish:
            t1 = 1
            t2_Normal = 3
            t2_Current = 2
        else:
            t1 = 3
            t2_Normal =1
            t2_Current = 0

        variants = []
        for pair in self.index:
            if len(selectionNormalWords) == len(pair[t1]):
                f = True
                for word, selectionNormalWord in zip(pair[t1], selectionNormalWords):
                    if word != selectionNormalWord:
                        f = False
                        break
                if f:
                    if len(pair[t2_Normal]) == 1:
                        S = " ".join(pair[t2_Normal])
                    else:
                        S = " ".join(pair[t2_Current])

                    for var in variants:
                        if var[0] == S:
                            var[1] += 1
                            break
                    else:
                        variants.append([S, 1])

        def sortByCount(el): return el[1]
        variants.sort(key=sortByCount, reverse=True)
        variants_res = [var[0] for var in variants]

        # variants = list(set(variants))
        return(variants_res)


    def setIndex(self):
        index = []

        for i, glossary  in enumerate(self.Glossaries):
            for j, paragraphInfo in enumerate(glossary.textInfo):
                for k, sentenceInfo in enumerate(paragraphInfo["sentencesInfo"]):
                    for l, correspondence in enumerate(sentenceInfo["correspondences"]):
                        engNums = correspondence["englishNums"]
                        rusNums = correspondence["russianNums"]
                        engWords = []
                        engNormalWords = []
                        for i in engNums:
                            engWords.append(sentenceInfo["pairs"][0]["wordsInfo"][i]["currentWord"])
                            engNormalWords.append(sentenceInfo["pairs"][0]["wordsInfo"][i]["normalWord"])
                        rusWords = []
                        rusNormalWords = []
                        for i in rusNums:
                            rusWords.append(sentenceInfo["pairs"][1]["wordsInfo"][i]["currentWord"])
                            rusNormalWords.append(sentenceInfo["pairs"][1]["wordsInfo"][i]["normalWord"])
                        pair = [engWords, engNormalWords, rusWords, rusNormalWords]
                        index.append(pair)

        import pickle
        f = open(self.Path+"\\__index", "wb")
        pickle.dump(index, f)

        self.index = index


    def getMaxLengthSentences(self, count = 50):
        Data = []
        for i, glossary  in enumerate(self.Glossaries):
            # print("%d of %d" % (i+1, len(self.Glossaries)))
            for j, paragraphInfo in enumerate(glossary.textInfo):
                for k, sentenceInfo in enumerate(paragraphInfo["sentencesInfo"]):
                    Data.append({"length": len(sentenceInfo["pairs"][0]["sentence"]),
                                 "glossary": str(self.Glossaries[i]), "num_paragraph": j, "num_sentence": k})

        def sortByLength(el):
            return el["length"]
        Data.sort(key=sortByLength, reverse=True)
        FilterData =  Data[:count]

        # def sortByGlossary(el):
        #     return el["glossary"]
        # FilterData.sort(key=sortByGlossary, reverse=True)
        return FilterData





    def generateWords(self, FileName):
        englishWords = []
        russianWords = []

        for i, glossary  in enumerate(self.Glossaries):
            print("%d of %d" % (i+1, len(self.Glossaries)))
            for j, paragraphInfo in enumerate(glossary.textInfo):
                for k, sentenceInfo in enumerate(paragraphInfo["sentencesInfo"]):

                    for wordInfo in sentenceInfo["pairs"][0]["wordsInfo"]:
                        if wordInfo["isMain"] and (len(wordInfo["currentWord"])>1):
                            normalWord = wordInfo["normalWord"]
                            for l, word in enumerate(englishWords):
                                if word[0] == normalWord:
                                    word[1] += 1
                                    break
                            else:
                                englishWords.append([normalWord, 1])

                    for wordInfo in sentenceInfo["pairs"][1]["wordsInfo"]:
                        if wordInfo["isMain"] and (len(wordInfo["currentWord"])>1):
                            normalWord = wordInfo["normalWord"]
                            for l, word in enumerate(russianWords):
                                if word[0] == normalWord:
                                    word[1] += 1
                                    break
                            else:
                                russianWords.append([normalWord, 1])


        def sortByCount(el):
            return el[1]

        def sortByName(el):
            return el[0]

        englishWords.sort(key=sortByCount, reverse=True)
        russianWords.sort(key=sortByCount, reverse=True)

        f = open(FileName +"_eng.txt", 'wt')
        for word in englishWords:
            f.write("%s: %d\n" % (word[0], word[1]))
        f.close()

        f = open(FileName +"_rus.txt", 'wt')
        for word in russianWords:
            f.write("%s: %d\n" % (word[0], word[1]))
        f.close()
