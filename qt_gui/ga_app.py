from ga_ui import *
import sys
import os
import json
from PyQt5.QtWidgets import (QApplication,
                            QWidget,
                            QTableWidgetItem,
                            QTableWidget,
                            QHeaderView)
from PyQt5.QtCore import QThread, pyqtSignal,QProcess


class GBF_AutoTool(QWidget, Ui_Form):
    def __init__(self,parent=None):
        super(GBF_AutoTool, self).__init__(parent)
        self.setupUi(self)
        # UI初始化
        try:
            _file = open(f"{os.getcwd()}/data/data_zhcn.json")
        except FileNotFoundError:
            print("[ERROR] Failed to find settings.json. Exiting now...")
            sys.exit(1)

        self.gamemode_dict = json.load(_file)


        self.comboBox.addItems(list(self.gamemode_dict.keys()))
        self.comboBox.activated[str].connect(self.onActivatedText)
        self.comboBox_2.addItems(self.gamemode_dict['任务'])

        self.comboBox_4.addItems(["召唤石多选"])
        self.comboBox_5.addItems(["召唤石多选"])

    @QtCore.pyqtSlot(str)
    def onActivatedText(self, text):
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.gamemode_dict[text])


if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    win=GBF_AutoTool()
    win.show()
    sys.exit(app.exec_())