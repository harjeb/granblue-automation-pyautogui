from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem
from PyQt5 import QtWidgets, QtCore
import sys
from PyQt5.QtGui import QStandardItemModel,QStandardItem
from PyQt5.QtWidgets import QStyledItemDelegate, qApp
from PyQt5.QtGui import QPalette,QFontMetrics
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt

class CheckableComboBox(QComboBox):
    # change = QtCore.pyqtSignal(bool)

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                # if index.row() == 0:
                #     if item.checkState() == Qt.Unchecked:
                #         for i in range(self.model().rowCount()):
                #             self.model().item(i).setCheckState(Qt.Checked)
                #     elif item.checkState() == Qt.Checked:
                #         for i in range(self.model().rowCount()):
                #             self.model().item(i).setCheckState(Qt.Unchecked)
                #     else:
                #         for i in range(self.model().rowCount()):
                #             self.model().item(i).setCheckState(Qt.Checked)

                #     return True

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)

                    # if self.selectedrow_num == 0:
                    #     self.model().item(0).setCheckState(Qt.Unchecked)
                    # else:
                    #     self.model().item(0).setCheckState(Qt.PartiallyChecked)
                else:
                    item.setCheckState(Qt.Checked)

                    # if self.selectedrow_num == self.model().rowCount() -1 :
                    #     self.model().item(0).setCheckState(Qt.Checked)
                    # else:
                    #     self.model().item(0).setCheckState(Qt.PartiallyChecked)

                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            # if self.model().item(0).checkState() == Qt.Checked:
            #     texts = self.list[1:]
            #     break
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())

        self.selectedrow_num = len(texts)
        text = ", ".join(texts)
        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)


    def addItems(self, texts, datalist=None):
        self.list = texts
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)


    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            # if self.model().item(0).checkState() == Qt.Checked:
            #     res = self.list[1:]
            #     return res
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res
