from ga_ui import *
import sys
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
        self.gamemode_dict= {'任务':["Scattered Cargo","Lucky Charm Hunt"],
                        '特殊':["火之试炼 N","火之试炼 H","火之试炼 VH"],
                        '团本':["Lvl 50 风妈 H","Lvl 100 风妈 EX","Lvl 70 火高达 H","火高达 EX"],
                        "兑换活动":[],
                        "战货活动":[],
                        "四象降临":[],
                        "古战场":[],
                        "工会战":[],
                        "勇气之地":[],
                        "六道击灭战":[],
                        "转世":[],
                        "转世沙盒":[],
                        "通常":[],
                        "暂停等待":[]}
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