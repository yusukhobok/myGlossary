FileName = "test.dsl"

import re

def cleartTags(text):
    return re.sub(r"\[.*?\]", "", text)

def statistics(WordsFileName):
    f = open("__"+WordsFileName, mode="wt")
    f_words = open(WordsFileName)
    sum = 0
    for i, word in enumerate(f_words):
        word = word.replace("\n", "")
        res = parseFile(word)
        if res is None: n = 0
        else: n = len(res[0])
        sum += n
        print(i, word, n, sum)
        f.write("%s;%d;\n" % (word, n))
    print("Sum = %d" % sum)
    f.close()



def parseFile(word):
    f = open(FileName, encoding="utf_16_le")
    lines = f.readlines()
    lines = lines[4:]

    numWord = None
    for i, line in enumerate(lines):
        match = re.search(r"^%s$" % word, line)
        if match is not None:
            numWord = i
            break

    if numWord is not None:
        Example = []
        Info = []
        Collocation = []

        for i, line in enumerate(lines[numWord+1:]):
            match = re.search(r"^[a-zA-Z0-9_\-]+$", line)
            if match is not None:
                break

            match = re.search(r"\[m1\]\[c teal\]\[b\](.*?)\[\/b\]\[\/c\][ ](.*)\[\/m\]", line)
            match_v2 = re.search(r"\[m1\]\[c teal\](.*)\[\/c\] \[c dodgerblue\]", line)
            if match_v2 is not None:
                collocation_v2 = match_v2.group(1)
                collocation_v2 = cleartTags(collocation_v2)
            else:
                continue

            if match is not None:
                # collocation = match.group(1)
                # collocation = cleartTags(collocation)
                match_info = re.search(r"\[c dodgerblue\](.*?)\[i\]", match.group(2))
                if match_info is not None:
                    info = match_info.group(1)
                else:
                    info = ""

                match_examples = re.search(r"\[c dodgerblue\].*\[i\](.*?)\[\/i\]\[\/c\]", match.group(2))
                if match_examples is not None:
                    example = match_examples.group(1)
                    example = cleartTags(example)
                else:
                    continue

                Collocation.append(collocation_v2)
                Info.append(info)
                Example.append(example)
        f.close()
        return (Collocation, Info, Example)
    else:
        f.close()
        return None




from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets

class AnkiWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Карточки для Anki")
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(600, 400)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.edtWord = QtWidgets.QLineEdit("")
        self.edtWord.returnPressed.connect(self.findWord)
        self.btnFind = QtWidgets.QPushButton("Поиск")
        self.btnFind.clicked.connect(self.findWord)
        self.btnSave = QtWidgets.QPushButton("Сохранить Ctrl+S")
        self.btnSave.clicked.connect(self.saveData)
        self.btnSave.setShortcut("Ctrl+S")
        self.btnFixed = QtWidgets.QPushButton("Зафиксировать F12")
        self.btnFixed.clicked.connect(self.fix)
        self.btnFixed.setShortcut("F12")
        self.btnPicture = QtWidgets.QPushButton("Картинка F8")
        self.btnPicture.clicked.connect(self.picture)
        self.btnPicture.setShortcut("F8")
        self.btnTranslate = QtWidgets.QPushButton("Yandex F2")
        self.btnTranslate.clicked.connect(self.translate)
        self.btnTranslate.setShortcut("F2")
        self.btnTranscription = QtWidgets.QPushButton("LDOCE F3")
        self.btnTranscription.clicked.connect(self.transcription)
        self.btnTranscription.setShortcut("F3")
        self.btnAudio = QtWidgets.QPushButton("Audio F4")
        self.btnAudio.clicked.connect(self.recordAudio)
        self.btnAudio.setShortcut("F4")
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.edtWord)
        self.hbox.addWidget(self.btnFind)
        self.hbox.addWidget(self.btnSave)
        self.hbox.addWidget(self.btnFixed)
        self.hbox.addWidget(self.btnPicture)
        self.hbox.addWidget(self.btnTranslate)
        self.hbox.addWidget(self.btnTranscription)
        self.hbox.addWidget(self.btnAudio)

        self.txtData = QtWidgets.QTextEdit()
        self.txtData.setReadOnly(True)
        self.txtData2 = QtWidgets.QTextEdit()

        self.splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        self.splitter1.addWidget(self.txtData)
        self.splitter1.addWidget(self.txtData2)
        self.web = QtWebEngineWidgets.QWebEngineView()
        self.web.load(QtCore.QUrl("https://www.google.ru/"))

        self.splitter2 = QtWidgets.QSplitter(QtCore.Qt.Vertical, self)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.web)

        font = QtGui.QFont()
        font.setPointSize(16)
        self.edtWord.setFont(font)
        self.txtData.setFont(font)
        self.txtData2.setFont(font)
        self.web.setFont(font)
        # self.btnFind.setFont(font)
        # self.btnSave.setFont(font)
        # self.btnFixed.setFont(font)
        # self.btnPicture.setFont(font)
        # self.btnTranslate.setFont(font)
        # self.btnTranscription.setFont(font)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.splitter2)
        # self.vbox.addLayout(self.hboxText)
        # self.vbox.addWidget(self.web)


        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.vbox)

        self.Collocation = None
        self.Info = None
        self.Example = None
        self.word = None


    def refreshText(self):
        self.txtData.clear()
        self.txtData2.clear()
        for (collocation, info, example) in zip(self.Collocation, self.Info, self.Example):
            # self.txtData.append("<b>%s</b>;%s%s" % (collocation, info, example))
            self.txtData.append(collocation + " " + info)
            self.txtData.append("<b>" + example + "</b>")
            self.txtData.append("=======================")
            self.txtData2.append("<b>%s</b>;%s%s" % (example, info, collocation))


    def findWord(self):
        word = self.edtWord.text()
        res = parseFile(word)
        self.word = word
        if res is not None:
            self.Collocation, self.Info, self.Example = res
            # self.GapsCount = [0] * len(self.Collocation)
            self.refreshText()
            # print("\n"*3)
            # for sentence in self.Example:
            #     print(sentence)


    def saveData(self):
        fName = "%s.csv" % self.word
        f = open(fName, "wt", encoding="utf-8")
        f.write(self.txtData2.toPlainText())
        # for (collocation, info, example) in zip(self.Collocation, self.Info, self.Example):
        #     f.write("%s;%s%s\n" % ((example, info, collocation)))
        f.close()


    def fix(self):
        AllText = self.txtData2.toPlainText()
        cursor = self.txtData2.textCursor()
        selText = cursor.selectedText()
        if len(selText) == 0: return

        i1 = cursor.selectionStart()
        i2 = cursor.selectionEnd()
        while (i1 != 0) and (AllText[i1] != "\n"):
            i1 -= 1
        while (i2 != len(AllText)-1) and (AllText[i2] != "\n"):
            i2 += 1

        line = AllText[i1:i2+1]
        num = 1
        while "{{c%d" % num in line:
            num += 1

        NewText = "{{c%d::%s}}" % (num, selText)
        cursor.insertText(NewText)


    def chooseTextWidget(self):
        if self.txtData2.hasFocus():
            txt = self.txtData2
        else:
            txt = self.txtData
        return txt

    def picture(self):
        txt = self.chooseTextWidget()
        text = txt.textCursor().selectedText()
        self.web.load(QtCore.QUrl("https://www.google.ru/search?q=%s&tbm=isch" % text))


    def translate(self):
        txt = self.chooseTextWidget()
        text = txt.textCursor().selectedText()
        text = text.replace(" ", "%20")
        self.web.load(QtCore.QUrl("https://translate.yandex.ru/?lang=en-ru&text=%s" % text))

    def transcription(self):
        txt = self.chooseTextWidget()
        text = txt.textCursor().selectedText()
        match = re.search(r"^\s*[a-zA-Z0-9_\-]+\s*$", text)
        if match is not None:
            self.web.load(QtCore.QUrl("https://www.ldoceonline.com/dictionary/%s" % text))

    def recordAudio(self):
        from gtts import gTTS
        text = "\n".join(self.Example)
        tts = gTTS(text=text, lang='en')
        tts.save("%s.mp3" % self.word)




if __name__ == '__main__':
    import sys
    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook


    # statistics(WordsFileName="words.txt")

    app = QtWidgets.QApplication(sys.argv)
    ankiWindow = AnkiWindow()
    ankiWindow.show()
    sys.exit(app.exec_())