# import glossary
# txt = glossary.Text()

# txt.importText(authors="Jan De Pue, Marc Van Meirvenne, and Wim M. Cornelis",
#                caption="Accounting for Surface Refraction in Velocity Semblance Analysis With Air-Coupled GPR",
#                data="IEEE JOURNAL OF SELECTED TOPICS IN APPLIED EARTH OBSERVATIONS AND REMOTE SENSING, VOL. 9, NO. 1, JANUARY 2016",
#                FileName="D:\\Programs\\myGlossary\\Pue(Belguim)2016_Accounting for Surface Refraction in Velocity Semblance Analysis With Air-Coupled GPR.txt")
# txt.printData()
# txt.save("D:\\Programs\\myGlossary\\temp")






#
# def transformText(self):
#     self.textInfo = []
#     paragraphs = self.text.split("\n")
#     paragraphs = [paragraph for paragraph in paragraphs if paragraph != ""]
#     for (k, paragraph) in enumerate(paragraphs):
#         print("%d абзац из %d" % (k + 1, len(paragraphs)))
#         sentences = words_processing.paragraphToSenetences(paragraph)
#         sentencesInfo = []
#         for (e, sentence) in enumerate(sentences):
#             print("%d предложение из %d" % (e + 1, len(sentences)))
#             words = words_processing.sentencesToWords(sentence)
#             wordsInfo = []
#             for word in words:
#                 normalWord = words_processing.getEnglishNormalForm(word)
#                 # normalWord = word
#                 wordsInfo.append({"currentWord": word, "normalWord": normalWord, "isMain": True})
#             if len(wordsInfo) > 0:
#                 sentencesInfo.append({"pairs":
#                                           [{"sentence": sentence, "wordsInfo": wordsInfo, "lineOfWords": None},
#                                            {"sentence": "", "wordsInfo": [], "lineOfWords": None}],
#                                       "correspondences": [],
#                                       "tags": []})
#         if len(sentencesInfo) > 0:
#             self.textInfo.append(({"paragraph": paragraph, "sentencesInfo": sentencesInfo}))


#f.close()

# import glossary
# txt = glossary.Text()
#
# import pickle
# FileName = "D:\\Programs\\myGlossary\\data\\Циммерман.gls"
# f = open(FileName, "rb")
# txt = pickle.load(f)
# f.close()
#
# txt.delDuplicates()
#
# f = open(FileName, "wb")
# pickle.dump(txt, f)
# f.close()

# import pickle
# f = open(FileName, "rb")
# txt = pickle.load(f)
# txt.printData()


# import finder
# Finder = finder.Finder("D:\\Programs\\myGlossary\\data\\")
# Finder.generateWords("D:\\Programs\\myGlossary\\data\\__RESULTS")


# from gtts import gTTS
# tts = gTTS(text="""Once again, Drew was under arrest.
# In 1997, the family moved house yet again.
# I’ll never go there again.
# Can you say that again? I didn’t hear.
# Mr Khan’s busy. Can you try again later?
# He kept repeating the same thing again and again.
# I’ve told you over and over again that you must not tell anyone.""", lang='en')
# tts.save('file.mp3')

import talkey
tts = talkey.Talkey(
    preferred_languages = ['en', 'af', 'el', 'fr'],
    espeak = {
        'languages': {
            'en': {
                'voice': 'english-mb-en1',
                'words_per_minute': 130
            },
        }
    })
tts.say('Old McDonald had a farm')


