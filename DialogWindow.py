# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class DialogWindow(QtWidgets.QDialog):
    def __init__(self, caption, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle(caption)
        self.setWindowFlags(QtCore.Qt.Dialog)

        self.btnOK = QtWidgets.QPushButton("ОК")
        self.btnCancel = QtWidgets.QPushButton("Отмена")
        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)
        self.hboxButtons = QtWidgets.QHBoxLayout()
        self.hboxButtons.addWidget(self.btnOK)
        self.hboxButtons.addWidget(self.btnCancel)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.hboxButtons)
        self.setLayout(self.vbox)

    def AddHBox(self, lbl, edt):
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(lbl)
        hbox.addWidget(edt)
        return hbox

    def addBoolItem(self, caption, default):
        lbl = QtWidgets.QLabel(caption)
        chk = QtWidgets.QCheckBox("")
        chk.setChecked(default)

        hbox = self.AddHBox(lbl, chk)
        self.vbox.insertLayout(self.vbox.count() - 1, hbox)
        return chk

    def addFloatItem(self, caption, default, min, max, decimals=3, precision=None):
        if precision is None: precision = 10**(-decimals)
        lbl = QtWidgets.QLabel(caption)
        edt = QtWidgets.QDoubleSpinBox()

        edt.setDecimals(decimals)
        edt.setSingleStep(precision)
        edt.setRange(min, max)
        edt.setValue(default)

        hbox = self.AddHBox(lbl, edt)
        self.vbox.insertLayout(self.vbox.count()-1, hbox)
        return edt

    def addIntItem(self, caption, default, min, max):
        lbl = QtWidgets.QLabel(caption)
        edt = QtWidgets.QDoubleSpinBox()

        edt.setRange(min, max)
        edt.setValue(default)
        edt.setSingleStep(1)
        edt.setDecimals(0)

        hbox = self.AddHBox(lbl, edt)
        self.vbox.insertLayout(self.vbox.count() - 1, hbox)
        return edt

    def addStringItem(self, caption, default=""):
        lbl = QtWidgets.QLabel(caption)
        edt = QtWidgets.QLineEdit()
        edt.setText(default)

        hbox = self.AddHBox(lbl, edt)
        self.vbox.insertLayout(self.vbox.count() - 1, hbox)
        return edt

    def addChoiseItem(self, caption, elements, default=0):
        lbl = QtWidgets.QLabel(caption)
        cmb = QtWidgets.QComboBox()
        cmb.clear()
        cmb.addItems(elements)
        cmb.setCurrentIndex(default)

        hbox = self.AddHBox(lbl, cmb)
        self.vbox.insertLayout(self.vbox.count() - 1, hbox)
        return cmb
