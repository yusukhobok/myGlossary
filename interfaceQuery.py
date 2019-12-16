from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import glossary
import finder


class InterfaceQueryWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Поиск")
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(600, 400)
        self.setWindowState(QtCore.Qt.WindowMaximized)

        self.btnSetPath = QtWidgets.QPushButton("Задать путь...")
        self.btnSetPath.clicked.connect(self.setPath)
        self.btnIndex = QtWidgets.QPushButton("Переиндексировать")
        self.btnIndex.clicked.connect(self.setIndex)
        # self.chkEnglish = QtWidgets.QCheckBox("English")
        # self.chkEnglish.setChecked(True)Qtwebkit
        self.cmbTag = QtWidgets.QComboBox()
        self.cmbSource = QtWidgets.QComboBox()
        self.btnGo = QtWidgets.QPushButton("Перейти")
        self.btnGo.clicked.connect(self.go)
        self.hBoxPath = QtWidgets.QHBoxLayout()
        self.hBoxPath.addWidget(self.btnSetPath)
        self.hBoxPath.addWidget(self.btnIndex)
        # self.hBoxPath.addWidget(self.chkEnglish)
        self.hBoxPath.addWidget(self.cmbTag)
        self.hBoxPath.addWidget(self.cmbSource)
        self.hBoxPath.addWidget(self.btnGo)

        self.hBoxPath.addStretch()

        self.edtQuery = QtWidgets.QLineEdit()
        self.edtQuery.returnPressed.connect(self.query)
        self.edtQuery.setText("")
        self.editFont(self.edtQuery)
        self.btnFind = QtWidgets.QPushButton("Поиск")
        self.btnFind.clicked.connect(self.query)
        self.hBoxQuery = QtWidgets.QHBoxLayout()
        self.hBoxQuery.addWidget(self.edtQuery)
        self.hBoxQuery.addWidget(self.btnFind)
        #self.hBoxQuery.addStretch()

        self.edtIndexResult = QtWidgets.QLineEdit("")
        self.editFont(self.edtIndexResult)
        self.edtIndexResult.setReadOnly(True)
        self.hBoxIndexResult = QtWidgets.QHBoxLayout()
        self.hBoxIndexResult.addWidget(self.edtIndexResult)

        self.txtResult = QtWebEngineWidgets.QWebEngineView()
        # self.viewResult = QtWidgets.QTableView()

        self.vboxMain = QtWidgets.QVBoxLayout()
        self.vboxMain.addLayout(self.hBoxPath)
        self.vboxMain.addLayout(self.hBoxQuery)
        self.vboxMain.addLayout(self.hBoxIndexResult)
        self.vboxMain.addWidget(self.txtResult)
        # self.vboxMain.addWidget(self.viewResult)
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.vboxMain)
        self.edtQuery.setFocus()

        # self.modelResult = QtGui.QStandardItemModel(0, 3)
        # self.viewResult.setModel(self.modelResult)
        # self.viewResult.setAlternatingRowColors(True)
        # self.viewResult.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        # self.viewResult.resizeRowsToContents()
        # self.viewResult.setWordWrap(True)
        # self.viewResult.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # self.viewResult.horizontalHeader().setStretchLastSection(True)

        self.Finder = None


    def setPath(self):
        dirName = QtWidgets.QFileDialog.getExistingDirectory(parent=self)
        if dirName == "": return
        self.Finder = finder.Finder(dirName)
        self.setWindowTitle("Поиск: " + dirName)
        self.cmbTag.clear()
        self.cmbTag.addItem("Все теги")
        self.cmbTag.addItems(self.Finder.getTags())
        self.cmbSource.clear()
        self.cmbSource.addItem("Все источники")
        self.cmbSource.addItems(self.Finder.getSources())


    def setIndex(self):
        if self.Finder is None: return
        self.Finder.setIndex()


    def go(self):
        if self.Finder is None: return
        if self.txtResult.hasSelection():
            S = self.txtResult.selectedText()
            self.edtQuery.setText(S)
            self.query()


    def query(self):
        if self.Finder is None: return

        if self.cmbTag.currentIndex() == 0:
            tag = None
        else:
            n = self.cmbTag.currentIndex()
            tag = self.cmbTag.itemText(n)

        if self.cmbSource.currentIndex() == 0:
            numSource = None
        else:
            numSource = self.cmbSource.currentIndex()-1

        if self.edtQuery.text().strip() == "":
            isEnlish = True
        else:
            import re
            eng = re.findall("[A-Za-z]", self.edtQuery.text())
            rus = re.findall("[А-Яа-я]", self.edtQuery.text())
            isEnlish = eng > rus

        Result = self.Finder.find(self.edtQuery.text(), isEnlish, tag=tag, source=numSource)
        if Result is not None:
            # self.modelResult.removeRows(0, self.modelResult.rowCount())
            # for res in Result:
            #     item_English = QtGui.QStandardItem(res["englishSentence"])
            #     item_English.setEditable(False)
            #     item_Russian = QtGui.QStandardItem(res["russianSentence"])
            #     item_Russian.setEditable(False)
            #     item_Source = QtGui.QStandardItem(str(res["glossary"]))
            #     item_Source.setEditable(False)
            #     self.modelResult.appendRow([item_English, item_Russian, item_Source])

            S = """
            <style>
            table {font-family: sans-serif; font-size: 20px; border-collapse: collapse;}
            table, tr, td {border: 1px solid black;}
            b {color: blue}
            </style>
            """

            S += '<table width="100%">\n'
            for res in Result:
                glossary = res["glossary"]
                ParagraphNum = res["ParagraphNum"]
                SentenceNum = res["SentenceNum"]
                coef = res["coef"]

                sentenceInfo = glossary.textInfo[ParagraphNum]["sentencesInfo"][SentenceNum]
                english = res["englishSentence"]
                russian = res["russianSentence"]

                S += '<tr> <td width="45%" class="eng">{}</td> <td width="45%" class="rus">{}</td> <td width="10%" class="source">{}</td> </tr>\n'.format(english, russian, "%s(%d;%d)" % (str(glossary), ParagraphNum, SentenceNum) )
            S += "</table>"

            self.txtResult.setHtml(S)

        variants = self.Finder.findInIndex(self.edtQuery.text())
        self.edtIndexResult.setText("; ".join(variants))


    def editFont(self, edt):
        font = QtGui.QFont()
        font.setPointSize(20)
        edt.setFont(font)




if __name__ == '__main__':
    import sys

    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook

    app = QtWidgets.QApplication(sys.argv)
    window = InterfaceQueryWindow()
    window.show()

    window.Finder = finder.Finder(QtCore.QDir.currentPath() + "\\data")
    window.cmbTag.addItem("Все теги")
    window.cmbTag.addItems(window.Finder.getTags())
    window.cmbSource.addItem("Все источники")
    window.cmbSource.addItems(window.Finder.getSources())


    sys.exit(app.exec_())