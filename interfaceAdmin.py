#-*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QTableView

import glossary

from interfaceQuery import InterfaceQueryWindow
import finder

class InterfaceWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Глоссарий")
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(600, 400)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.lblParagraphNum = QtWidgets.QLabel("Абзац")
        self.edtParagraphNum = QtWidgets.QDoubleSpinBox()
        self.edtParagraphNum.setRange(0, 100000) #!
        self.edtParagraphNum.setValue(0) #!
        self.edtParagraphNum.setSingleStep(1)
        self.edtParagraphNum.setDecimals(0)
        self.edtParagraphNum.valueChanged["double"].connect(self.changeParagraphNum)
        self.hboxParagraphNum = QtWidgets.QHBoxLayout()
        self.hboxParagraphNum.addWidget(self.lblParagraphNum)
        self.hboxParagraphNum.addWidget(self.edtParagraphNum)

        self.lblSentenceNum = QtWidgets.QLabel("Предложение")
        self.edtSentenceNum = QtWidgets.QDoubleSpinBox()
        self.edtSentenceNum.setRange(0, 100000)
        self.edtSentenceNum.setValue(0)
        self.edtSentenceNum.setSingleStep(1)
        self.edtSentenceNum.setDecimals(0)
        self.edtSentenceNum.valueChanged["double"].connect(self.changeSentenceNum)
        self.hboxSentenceNum = QtWidgets.QHBoxLayout()
        self.hboxSentenceNum.addWidget(self.lblSentenceNum)
        self.hboxSentenceNum.addWidget(self.edtSentenceNum)

        self.btnImport = QtWidgets.QPushButton("Импорт...")
        self.btnImport.clicked.connect(self.importText)
        self.btnImport.setShortcut("Ctrl+I")

        self.btnSave = QtWidgets.QPushButton("Сохранить")
        self.btnSave.clicked.connect(self.saveText)
        self.btnSave.setShortcut("Ctrl+S")

        self.btnSaveAs = QtWidgets.QPushButton("Сохранить как...")
        self.btnSaveAs.clicked.connect(self.saveAsText)

        self.btnLoad = QtWidgets.QPushButton("Открыть...")
        self.btnLoad.clicked.connect(self.loadText)
        self.btnLoad.setShortcut("Ctrl+O")

        self.btnInfo = QtWidgets.QPushButton("Информация...")
        self.btnInfo.clicked.connect(self.editInfo)

        self.btnAllSource = QtWidgets.QPushButton("Весь источник...")
        self.btnAllSource.clicked.connect(self.allSource)

        # self.btnCalc = QtWidgets.QPushButton("Расчеты")
        # self.btnCalc.clicked.connect(self.calculate)

        self.chkModeSentence = QtWidgets.QCheckBox()
        self.chkModeSentence.clicked.connect(self.changeModeSentence)
        self.chkModeTranslation = QtWidgets.QCheckBox()
        self.chkModeTranslation.clicked.connect(self.changeModeTranslation)

        self.lblCoef = QtWidgets.QLabel("Коэффициент")
        self.edtCoef = QtWidgets.QDoubleSpinBox()
        self.edtCoef.setRange(0, 1.0) #!
        self.edtCoef.setValue(1.0) #!
        self.edtCoef.setSingleStep(0.1)
        self.edtCoef.setDecimals(2)
        self.edtCoef.valueChanged["double"].connect(self.changeCoef)

        self.btnDelSentence = QtWidgets.QPushButton("Удалить предложение")
        self.btnDelSentence.clicked.connect(self.delSentence)
        self.btnDelSentence.setShortcut("Ctrl+Del")

        self.btnUnionSentence = QtWidgets.QPushButton("Объединить с предыдущим")
        self.btnUnionSentence.clicked.connect(self.unionSentence)

        # self.btnFind = QtWidgets.QPushButton("Поиск")
        # self.btnFind.clicked.connect(self.findQuery)

        self.btnNext = QtWidgets.QPushButton("Вперед")
        self.btnNext.clicked.connect(self.nextSentence)
        self.btnNext.setShortcut("Ctrl+/")

        self.btnLast = QtWidgets.QPushButton("Назад")
        self.btnLast.clicked.connect(self.lastSentence)
        self.btnLast.setShortcut("Ctrl+.")

        self.btnSentenceWithoutTranslation = QtWidgets.QPushButton("Без перевода")
        self.btnSentenceWithoutTranslation.clicked.connect(self.getSentenceWithoutTranslation)

        self.btnSentenceWithoutTags = QtWidgets.QPushButton("Без тегов")
        self.btnSentenceWithoutTags.clicked.connect(self.getSentenceWithoutTags)

        self.btnSentenceWithoutCorrespondences = QtWidgets.QPushButton("Без соответствий")
        self.btnSentenceWithoutCorrespondences.clicked.connect(self.getSentenceWithoutCorrespondences)

        self.hboxMain = QtWidgets.QHBoxLayout()
        self.hboxMain.addWidget(self.btnImport)
        self.hboxMain.addWidget(self.btnSave)
        self.hboxMain.addWidget(self.btnSaveAs)
        self.hboxMain.addWidget(self.btnLoad)
        self.hboxMain.addWidget(self.btnInfo)
        self.hboxMain.addWidget(self.btnAllSource)
        # self.hboxMain.addWidget(self.btnCalc)
        self.hboxMain.addWidget(self.chkModeSentence)
        self.hboxMain.addWidget(self.chkModeTranslation)
        self.hboxMain.addWidget(self.lblCoef)
        self.hboxMain.addWidget(self.edtCoef)
        self.hboxMain.addStretch()

        self.hboxAddress = QtWidgets.QHBoxLayout()
        self.hboxAddress.addLayout(self.hboxParagraphNum)
        self.hboxAddress.addLayout(self.hboxSentenceNum)
        self.hboxAddress.addWidget(self.btnLast)
        self.hboxAddress.addWidget(self.btnNext)
        self.hboxAddress.addWidget(self.btnSentenceWithoutTranslation)
        self.hboxAddress.addWidget(self.btnSentenceWithoutTags)
        self.hboxAddress.addWidget(self.btnSentenceWithoutCorrespondences)
        self.hboxAddress.addWidget(self.btnDelSentence)
        self.hboxAddress.addWidget(self.btnUnionSentence)
        # self.hboxAddress.addWidget(self.btnFind)
        self.hboxAddress.addStretch()

        self.lblSentence = QtWidgets.QLabel("Предложение")
        self.edtSentence = QtWidgets.QLineEdit()
        self.edtSentence.setMaximumHeight(100)
        self.edtSentence.returnPressed.connect(self.saveSentence)
        self.editFont(self.edtSentence)
        self.txtSentence = QtWidgets.QTextEdit()
        self.txtSentence.setVisible(False)
        self.txtSentence.setMaximumHeight(200)
        self.editFont(self.txtSentence)

        self.lblTranslation = QtWidgets.QLabel("Перевод")
        self.edtTranslation = QtWidgets.QLineEdit()
        self.edtTranslation.returnPressed.connect(self.saveTranslation)
        self.editFont(self.edtTranslation)
        self.txtTranslation = QtWidgets.QTextEdit()
        self.txtTranslation.setVisible(False)
        self.txtTranslation.setMaximumHeight(200)
        self.editFont(self.txtTranslation)

        self.lblTags = QtWidgets.QLabel("Теги")
        self.edtTags = QtWidgets.QLineEdit()
        self.edtTags.returnPressed.connect(self.saveTags)
        # self.edtTags.textEdited.connect(self.saveTags)
        self.editFont(self.edtTags)

        self.lstWords = QtWidgets.QListView()
        self.stiWords = QtGui.QStandardItemModel(parent = self)
        self.lstWords.setModel(self.stiWords)
        self.lstWords.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lstWords.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))
        self.editFont(self.lstWords)

        self.lstTranslationWords = QtWidgets.QListView()
        self.stiTranslationWords = QtGui.QStandardItemModel(parent = self)
        self.stiTranslationWords.itemChanged.connect(self.changeRussianWord)
        self.lstTranslationWords.setModel(self.stiTranslationWords)
        self.lstTranslationWords.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lstTranslationWords.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding))
        self.editFont(self.lstTranslationWords)

        self.lstCorrespondences = QtWidgets.QListView()
        self.stiCorrespondences = QtGui.QStandardItemModel(parent = self)
        self.stiCorrespondences.itemChanged.connect(self.changeEnglishWord)
        self.lstCorrespondences.setModel(self.stiCorrespondences)
        self.lstCorrespondences.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lstCorrespondences.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.editFont(self.lstCorrespondences)

        self.hboxPair = QtWidgets.QHBoxLayout()
        self.hboxPair.addWidget(self.lstWords)
        self.hboxPair.addWidget(self.lstTranslationWords)
        self.hboxPair.addWidget(self.lstCorrespondences)
        # self.hboxPair.addStretch()

        self.vboxData = QtWidgets.QVBoxLayout()
        self.vboxData.addWidget(self.lblSentence)
        self.vboxData.addWidget(self.edtSentence)
        self.vboxData.addWidget(self.txtSentence)
        self.vboxData.addWidget(self.lblTranslation)
        self.vboxData.addWidget(self.edtTranslation)
        self.vboxData.addWidget(self.txtTranslation)
        self.vboxData.addWidget(self.lblTags)
        self.vboxData.addWidget(self.edtTags)
        self.vboxData.addLayout(self.hboxPair)

        self.edtIndexResult = QtWidgets.QLineEdit()
        self.edtIndexResult.setMaximumHeight(100)
        self.edtIndexResult.setReadOnly(True)
        self.editFont(self.edtIndexResult)

        self.hboxIndexResult = QtWidgets.QHBoxLayout()
        self.hboxIndexResult.addWidget(self.edtIndexResult)

        self.vboxMain = QtWidgets.QVBoxLayout()
        self.vboxMain.addLayout(self.hboxMain)
        self.vboxMain.addLayout(self.hboxAddress)
        self.vboxMain.addLayout(self.vboxData)
        self.vboxMain.addLayout(self.hboxIndexResult)

        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.vboxMain)

        self.Text = None
        self.ParagraphNum = None
        self.SentenceNum = None
        self.FileName = None

        self.windowQuery = InterfaceQueryWindow(self)
        self.windowQuery.Finder = finder.Finder(QtCore.QDir.currentPath() + "\\data")
        self.windowQuery.cmbTag.addItem("Все теги")
        self.windowQuery.cmbTag.addItems(self.windowQuery.Finder.getTags())
        self.windowQuery.cmbSource.addItem("Все источники")
        self.windowQuery.cmbSource.addItems(self.windowQuery.Finder.getSources())
        self.windowQuery.hide()


    def loadText(self):
        from PyQt5.QtWidgets import QFileDialog
        FileName, _ = QFileDialog.getOpenFileNames(parent=self, caption="Глоссарий",
                                                   filter="Глоссарий (*.gls)", directory="data\\")
        if FileName:
            self.FileName = FileName[0]
            import pickle
            f = open(self.FileName, "rb")
            self.Text = pickle.load(f)
            if not hasattr(self.Text, "coef"):
                setattr(self.Text, "coef", 1.0)
            self.setWindowTitle("Глоссарий: " + self.FileName)
            # self.Text.printData()
            self.Text.delNotEnglishSentences()
            self.init()


    def importText(self):
        from PyQt5.QtWidgets import QFileDialog
        FileName, _ = QFileDialog.getOpenFileNames(parent=self, caption="Исходный текст",
                                                   filter="Текстовый документ (*.txt)", directory="data\\new\\")
        if FileName:
            FileName = FileName[0]
            self.FileName = None
            self.Text = glossary.Text(FileName)
            # self.Text.printData()
            self.init()


    def allSource(self):
        if self.Text is None: return
        window = QtWidgets.QWidget(parent=self)
        window.setWindowTitle(str(self.Text))
        window.setWindowFlags(QtCore.Qt.Window)
        window.resize(600, 400)
        window.setWindowState(QtCore.Qt.WindowMaximized)

        # window.stiSource = QtGui.QStandardItemModel(parent = self)
        # window.tblSource = QTableView()
        # window.tblSource.setModel(window.stiSource)
        # self.editFont(window.tblSource)
        # window.vbox = QtWidgets.QVBoxLayout()
        # window.vbox.addWidget(window.tblSource)
        # window.setLayout(window.vbox)
        #
        #
        # window.stiSource.clear()
        # for (i,paragraph) in enumerate(self.Text.textInfo):
        #     for (j, sentence) in enumerate(paragraph["sentencesInfo"]):
        #         english = sentence["pairs"][0]["sentence"]
        #         russian = sentence["pairs"][1]["sentence"]
        #         item1 = QtGui.QStandardItem("%d" % i)
        #         item2 = QtGui.QStandardItem("%d" % j)
        #         item3 = QtGui.QStandardItem(english)
        #         item4 = QtGui.QStandardItem(russian)
        #         window.stiSource.appendRow([item1, item2, item3, item4])
        #
        # window.stiSource.setHorizontalHeaderLabels(['Абз.', 'Предл.', 'Английский', 'Русский'])

        window.txtResult = QtWebEngineWidgets.QWebEngineView()
        window.vbox = QtWidgets.QVBoxLayout()
        window.vbox.addWidget(window.txtResult)
        window.setLayout(window.vbox)

        S = """
                    <style>
                    table {font-family: sans-serif; font-size: 20px; border-collapse: collapse;}
                    table, tr, td {border: 1px solid black;}
                    b {color: blue}
                    </style>
                    """
        S += '<table width="100%">\n'
        S += '<tr> <td width="5%" class="paragraph">{}</td> <td width="5%" class="sentence">{}</td> <td width="45%" class="eng">{}</td> <td width="45%" class="rus">{}</td></tr>\n'.format(
            "Абз.", "Предл.", "Английский", "Русский")

        for (i,paragraph) in enumerate(self.Text.textInfo):
            for (j, sentence) in enumerate(paragraph["sentencesInfo"]):
                english = sentence["pairs"][0]["sentence"]
                russian = sentence["pairs"][1]["sentence"]
                if j==0:
                    ii = i
                else:
                    ii = ""
                S += '<tr> <td width="5%" class="paragraph">{}</td> <td width="5%" class="sentence">{}</td> <td width="45%" class="eng">{}</td> <td width="45%" class="rus">{}</td></tr>\n'.format(
                    ii, j, english, russian)

        S += "</table>"
        window.txtResult.setHtml(S)




        window.show()




    def editInfo(self):
        if self.Text is None: return
        from DialogWindow import DialogWindow
        dlg = DialogWindow("Информация о тексте")
        authors = dlg.addStringItem("Авторы", self.Text.authors)
        caption = dlg.addStringItem("Название", self.Text.caption)
        year = dlg.addStringItem("Год", self.Text.year)
        data = dlg.addStringItem("Выходные данные", self.Text.data)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            self.Text.authors = authors.text()
            self.Text.caption = caption.text()
            self.Text.year = year.text()
            self.Text.data = data.text()


    def saveText(self):
        if self.Text is None: return
        if self.FileName is None:
            self.saveAsText()
        else:
            self.save()


    def saveAsText(self):
        if self.Text is None: return
        from PyQt5.QtWidgets import QFileDialog
        FileName, _ = QFileDialog.getSaveFileName(parent=self, caption="Глоссарий",
                                                  filter="Глоссарий (*.gls)", directory="data\\")
        if FileName:
            self.FileName = FileName
            self.save()


    def save(self):
        if self.Text is None: return
        if self.FileName is None: return
        import pickle
        f = open(self.FileName, "wb")
        pickle.dump(self.Text, f)
        self.setWindowTitle("Глоссарий: " + self.FileName)
        # self.Text.printData()


    def init(self, isNew = True):
        if self.Text is None: return

        if isNew: self.ParagraphNum = 0
        self.lblParagraphNum.setText("Абзац (из %d)" % len(self.Text.textInfo))
        self.edtParagraphNum.blockSignals(True)
        self.edtParagraphNum.setValue(self.ParagraphNum)
        self.edtParagraphNum.setRange(0, len(self.Text.textInfo) - 1)
        self.edtParagraphNum.blockSignals(False)

        if isNew: self.SentenceNum = 0
        self.lblSentenceNum.setText("Предложение (из %d)" % len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"]))
        self.edtSentenceNum.blockSignals(True)
        self.edtSentenceNum.setValue(self.SentenceNum)
        self.edtSentenceNum.setRange(0, len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"]) - 1)
        self.edtSentenceNum.blockSignals(False)
        self.refresh()


    def refresh(self):
        if self.Text is None: return
        self.edtCoef.setValue(self.Text.coef)

        sentenceInfo = self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]

        self.edtSentence.setText(sentenceInfo["pairs"][0]["sentence"])
        self.txtSentence.setText(sentenceInfo["pairs"][0]["sentence"])

        self.stiWords.clear()
        for word in sentenceInfo["pairs"][0]["wordsInfo"]:
            self.stiWords.appendRow(QtGui.QStandardItem(word["currentWord"]))

        self.edtTranslation.setText(sentenceInfo["pairs"][1]["sentence"])
        self.txtTranslation.setText(sentenceInfo["pairs"][1]["sentence"])
        self.stiTranslationWords.clear()
        for translationWord in sentenceInfo["pairs"][1]["wordsInfo"]:
            self.stiTranslationWords.appendRow(QtGui.QStandardItem(translationWord["currentWord"]))

        tagsString = ", ".join(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["tags"])
        self.edtTags.setText(tagsString)

        self.stiCorrespondences.clear()
        for correspondence in sentenceInfo["correspondences"]:
            englishWords = []
            for n in correspondence["englishNums"]:
                word = sentenceInfo["pairs"][0]["wordsInfo"][n]["currentWord"]
                englishWords.append(word)
                self.stiWords.item(n,0).setEnabled(False)
            englishPhrase = " ".join(englishWords)

            russianWords = []
            for n in correspondence["russianNums"]:
                word = sentenceInfo["pairs"][1]["wordsInfo"][n]["currentWord"]
                russianWords.append(word)
                self.stiTranslationWords.item(n, 0).setEnabled(False)
            russianPhrase = " ".join(russianWords)

            self.stiCorrespondences.appendRow(QtGui.QStandardItem(englishPhrase + " = " + russianPhrase))

        # self.stiCorrespondences.item(0,0).setEnabled(False)


    def keyPressEvent(self, e):
        if self.Text is None: return
        if e.key() == QtCore.Qt.Key_Right:
            if (len(self.lstWords.selectedIndexes()) == 0) or (len(self.lstTranslationWords.selectedIndexes()) == 0): return
            englishNums = [el.row() for el in self.lstWords.selectedIndexes()]
            russianNums = [el.row() for el in self.lstTranslationWords.selectedIndexes()]
            englishNums.sort()
            russianNums.sort()
            self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["correspondences"].append(
                {"englishNums": englishNums, "russianNums": russianNums})
            self.refresh()

        elif (e.key() == QtCore.Qt.Key_Delete) and (self.lstCorrespondences.hasFocus()):
            n = self.lstCorrespondences.currentIndex().row()
            if n>=0:
                del(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["correspondences"][n])
                self.refresh()

        elif (self.txtSentence.hasFocus()) and (e.key() == QtCore.Qt.Key_F10):
            self.edtSentence.setText(self.txtSentence.toPlainText())
            self.saveSentence()

        elif (self.txtTranslation.hasFocus()) and (e.key() == QtCore.Qt.Key_F10):
            self.edtTranslation.setText(self.txtTranslation.toPlainText())
            self.saveTranslation()

        elif (self.edtSentence.hasFocus()) and (e.key() == QtCore.Qt.Key_F8) and (self.edtSentence.hasSelectedText()):
            query = self.edtSentence.selectedText()
            if query.strip() != "":
                self.findQuery(query)
        elif (self.txtSentence.hasFocus()) and (e.key() == QtCore.Qt.Key_F8) and (self.txtSentence.textCursor().hasSelection()):
            query = self.txtSentence.textCursor().selectedText()
            if query.strip() != "":
                self.findQuery(query)

        elif (self.edtTranslation.hasFocus()) and (e.key() == QtCore.Qt.Key_F8) and (self.edtTranslation.hasSelectedText()):
            query = self.edtTranslation.selectedText()
            if query.strip() != "":
                self.findQuery(query)
        elif (self.txtTranslation.hasFocus()) and (e.key() == QtCore.Qt.Key_F8) and (self.txtTranslation.textCursor().hasSelection()):
            query = self.txtTranslation.textCursor().selectedText()
            if query.strip() != "":
                self.findQuery(query)

        elif (self.edtSentence.hasFocus()) and (e.key() == QtCore.Qt.Key_F7) and (self.edtSentence.hasSelectedText()):
            query = self.edtSentence.selectedText()
            if query.strip() != "":
                self.findInIndex(query)
        elif (self.txtSentence.hasFocus()) and (e.key() == QtCore.Qt.Key_F7) and (self.txtSentence.textCursor().hasSelection()):
            query = self.txtSentence.textCursor().selectedText()
            if query.strip() != "":
                self.findInIndex(query)

        elif (self.edtTranslation.hasFocus()) and (e.key() == QtCore.Qt.Key_F7) and (self.edtTranslation.hasSelectedText()):
            query = self.edtTranslation.selectedText()
            if query.strip() != "":
                self.findInIndex(query)
        elif (self.txtTranslation.hasFocus()) and (e.key() == QtCore.Qt.Key_F7) and (self.txtTranslation.textCursor().hasSelection()):
            query = self.txtTranslation.textCursor().selectedText()
            if query.strip() != "":
                self.findInIndex(query)


    def findQuery(self, query):
        self.windowQuery.edtQuery.setText(query)
        self.windowQuery.query()
        self.windowQuery.show()


    def findInIndex(self, query):
        self.windowQuery.Finder.setIndex()
        variants = self.windowQuery.Finder.findInIndex(query)
        self.edtIndexResult.setText("; ".join(variants))


    def saveSentence(self):
        if self.Text is None: return
        self.Text.setSentence(self.ParagraphNum, self.SentenceNum, self.edtSentence.text())
        self.Text.calculateSentence(self.ParagraphNum, self.SentenceNum)
        self.refresh()

    def saveTranslation(self):
        if self.Text is None: return
        self.Text.setTranslation(self.ParagraphNum, self.SentenceNum, self.edtTranslation.text())
        self.Text.calculateSentence(self.ParagraphNum, self.SentenceNum)
        self.refresh()


    def saveTags(self):
        if self.Text is None: return
        tagsString = self.edtTags.text()
        tags = tagsString.split(", ")
        tags = [tag.strip().lower() for tag in tags]
        tags = [tag for tag in tags if tag != ""]
        self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["tags"] = tags
        self.refresh()


    def delSentence(self):
        if self.Text is None: return
        del(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum])
        if self.SentenceNum > 0:
            self.SentenceNum -= 1
        if len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"]) == 0:
            del(self.Text.textInfo[self.ParagraphNum])
            if self.ParagraphNum > 0:
                self.ParagraphNum -= 1
        self.init(False)


    def unionSentence(self):
        if self.Text is None: return
        if self.SentenceNum == 0: return
        english = self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum-1]["pairs"][0]["sentence"]
        russian = self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum-1]["pairs"][1]["sentence"]
        english += " " + self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["pairs"][0]["sentence"]
        russian += " " + self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["pairs"][1]["sentence"]
        self.Text.setSentence(self.ParagraphNum, self.SentenceNum-1, english)
        self.Text.setTranslation(self.ParagraphNum, self.SentenceNum-1, russian)
        self.delSentence()


    def changeParagraphNum(self, value):
        if self.Text is None: return
        if value > len(self.Text.textInfo)-1: return
        self.ParagraphNum = int(value)
        self.edtSentenceNum.blockSignals(True)
        self.edtSentenceNum.setValue(0)
        self.edtSentenceNum.setRange(0, len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"]) - 1)
        self.edtSentenceNum.blockSignals(False)
        self.SentenceNum = 0
        self.refresh()


    def changeSentenceNum(self, value):
        if value > len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"]) - 1: return
        self.SentenceNum = int(value)
        self.refresh()


    def nextSentence(self):
        if self.Text is None: return
        len_paragraphs = len(self.Text.textInfo)
        len_sentences = len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"])
        if self.SentenceNum < len_sentences - 1:
            self.SentenceNum += 1
            self.init(False)
        elif self.ParagraphNum < len_paragraphs - 1:
            self.ParagraphNum += 1
            self.SentenceNum = 0
            self.init(False)
        self.save()


    def lastSentence(self):
        if self.Text is None: return
        if self.SentenceNum > 0:
            self.SentenceNum -= 1
            self.init(False)
        elif self.ParagraphNum > 0:
            self.ParagraphNum -= 1
            self.SentenceNum = len(self.Text.textInfo[self.ParagraphNum]["sentencesInfo"])-1
            self.init(False)
        self.save()


    def editFont(self, edt):
        font = QtGui.QFont()
        font.setPointSize(14)
        edt.setFont(font)


    def changeModeSentence(self):
        if self.Text is None: return
        self.txtSentence.setVisible(self.chkModeSentence.isChecked())
        self.edtSentence.setVisible(not self.chkModeSentence.isChecked())
        if self.chkModeSentence.isChecked():
            self.txtSentence.setText(self.edtSentence.text())
        else:
            self.edtSentence.setText(self.txtSentence.toPlainText())


    def changeModeTranslation(self):
        self.txtTranslation.setVisible(self.chkModeTranslation.isChecked())
        self.edtTranslation.setVisible(not self.chkModeTranslation.isChecked())
        if self.chkModeTranslation.isChecked():
            self.txtTranslation.setText(self.edtTranslation.text())
        else:
            self.edtTranslation.setText(self.txtTranslation.toPlainText())


    def changeCoef(self):
        if self.Text is None: return
        self.Text.coef = self.edtCoef.value()


    def changeRussianWord(self, item):
        if self.Text is None: return
        n = item.row()
        word = self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["pairs"][1]["wordsInfo"][n][
            "currentWord"]
        if word != item.text():
            self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["pairs"][1]["wordsInfo"][n][
                "currentWord"] = item.text()

    def changeEnglishWord(self, item):
        if self.Text is None: return
        n = item.row()
        word = self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["pairs"][0]["wordsInfo"][n][
            "currentWord"]
        if word != item.text():
            self.Text.textInfo[self.ParagraphNum]["sentencesInfo"][self.SentenceNum]["pairs"][0]["wordsInfo"][n][
                "currentWord"] = item.text()


    def getSentenceWithoutTranslation(self):
        if self.Text is None: return
        (parNum, sentNum) = self.Text.getSentenceWithoutTranslation(self.ParagraphNum, self.SentenceNum)
        if parNum is not None:
            self.ParagraphNum = parNum
            self.SentenceNum = sentNum
            self.init(False)


    def getSentenceWithoutTags(self):
        if self.Text is None: return
        (parNum, sentNum) = self.Text.getSentenceWithoutTags(self.ParagraphNum, self.SentenceNum)
        if parNum is not None:
            self.ParagraphNum = parNum
            self.SentenceNum = sentNum
            self.init(False)


    def getSentenceWithoutCorrespondences(self):
        if self.Text is None: return
        (parNum, sentNum) = self.Text.getSentenceWithoutCorrespondences(self.ParagraphNum, self.SentenceNum)
        if parNum is not None:
            self.ParagraphNum = parNum
            self.SentenceNum = sentNum
            self.init(False)





if __name__ == '__main__':
    import sys

    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceWindow()
    window.show()
    sys.exit(app.exec_())