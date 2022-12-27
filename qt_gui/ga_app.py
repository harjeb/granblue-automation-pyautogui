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
            ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
            _file = open(f"{ROOT_PATH}/data/data_zhcn.json",encoding='utf-8')
        except FileNotFoundError:
            print("[ERROR] Failed to find settings.json. Exiting now...")
            sys.exit(1)

        self.gamemode_dict = json.load(_file)


        self.comboBox.addItems(list(self.gamemode_dict.keys()))
        self.comboBox.activated[str].connect(self.onActivatedText)
        self.comboBox_2.addItems(self.gamemode_dict['任务'])

        self.comboBox_4.addItems(["召唤石多选"])
        self.comboBox_5.addItems(["召唤石多选"])

        # 默认勾选项
        # configuration.enableBezierCurveMouseMovement
        self.checkBox_2.setChecked(True)
        self.checkBox_2.clicked.connect(self.onStateChanged)
        # configuration.enableRandomizedDelayBetweenRuns
        self.checkBox_4.setChecked(True)
        self.checkBox_4.clicked.connect(self.onStateChanged)
        #configuration.delayBetweenRunsLowerBound
        self.spinBox_6.setValue(5)
        #configuration.delayBetweenRunsUpperBound
        self.spinBox_7.setValue(20)   

    @QtCore.pyqtSlot(str)
    def onActivatedText(self, text):
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.gamemode_dict[text])

    def onStateChanged(self):
        if self.checkBox_2.isChecked():
            self.doubleSpinBox.setEnabled(True)
        else:
            self.doubleSpinBox.setEnabled(False)
        if self.checkBox_4.isChecked():
            self.spinBox_6.setEnabled(True)
            self.spinBox_7.setEnabled(True)
        else:
            self.spinBox_6.setEnabled(False)
            self.spinBox_7.setEnabled(False)        
            


if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    win=GBF_AutoTool()
    win.show()
    sys.exit(app.exec_())