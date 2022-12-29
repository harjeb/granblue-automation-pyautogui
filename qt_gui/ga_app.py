from ga_ui import *
import sys
import time
import os
import json
from PyQt5.QtWidgets import (QApplication,
                            QWidget,
                            QTableWidgetItem,
                            QTableWidget,
                            QFileDialog,
                            QHeaderView,
                            QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal,QProcess
from io import StringIO
import traceback
import socket

def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 80
    logFile = "error.log"
    notice = \
        """An unhandled exception occurred. Please report the problem\n"""\
        """using the error reporting dialog or via email to <%s>.\n"""\
        """A log has been written to "%s".\n\nError information:\n""" % \
        ("harjeb@outlook.com", "")
    versionInfo="2.0.3c"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    tbinfofile = StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sections = [separator, timeString, separator, errmsg, separator, tbinfo]
    msg = '\n'.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    errorbox = QMessageBox()
    errorbox.setText(str(notice)+str(msg)+str(versionInfo))
    errorbox.exec_()

sys.excepthook = excepthook


class GBF_AutoTool(QWidget, Ui_Form):
    def __init__(self,parent=None):
        super(GBF_AutoTool, self).__init__(parent)
        self.setupUi(self)
        # UI初始化
        try:
            self.ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
            _file = open(f"{self.ROOT_PATH}/data/data_zhcn.json",encoding='utf-8')
            _summon = open(f"{self.ROOT_PATH}/data/summons_zhcn.json",encoding='utf-8')
        except FileNotFoundError:
            print("[ERROR] Failed to find settings.json. Exiting now...")
            sys.exit(1)

        self.gamemode_dict = json.load(_file)
        self.summons_dict = json.load(_summon)

        self.summons_list = []
        for v in self.summons_dict.values():
            self.summons_list.extend(v["summons"])

        self.comboBox.addItems(list(self.gamemode_dict.keys()))
        self.comboBox.activated[str].connect(self.onActivatedText)
        self.comboBox_2.addItems(list(self.gamemode_dict['任务'].keys()))
        self.comboBox_2.activated[str].connect(self.onActivatedSubText)
        maps = self.gamemode_dict[self.comboBox.currentText()][self.comboBox_2.currentText()]['map']
        if type(maps) is not list:
            maps = [maps]
        self.comboBox_3.addItems(maps)
        items = self.gamemode_dict[self.comboBox.currentText()][self.comboBox_2.currentText()]['items']
        if type(items) is not list:
            items = [items]
        self.comboBox_6.addItems(items)

        self.comboBox_4.addItems(self.summons_list)
        self.comboBox_5.addItems(self.summons_list)


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
        #configuration.enableDelayBetweenRuns
        self.checkBox_3.setChecked(False)
        self.checkBox_3.clicked.connect(self.onStateChanged)
        self.spinBox_4.setEnabled(False)
        #configuration.enableRefreshDuringCombat
        self.checkBox_7.setChecked(True)
        #configuration.enableAutoQuickSummon
        self.checkBox_8.setChecked(False)
        #configuration.enableBypassResetSummon
        self.checkBox.setChecked(False)
        #configuration.staticWindow
        self.checkBox_9.setChecked(True)
        #configuration.enableMouseSecurityAttemptBypass
        self.checkBox_10.setChecked(True)
        #configuration.alternativeCombatScriptSelector
        self.checkBox_11.setChecked(False)
        #raid.enableAutoExitRaid
        self.checkBox_5.setChecked(False)
        self.checkBox_5.clicked.connect(self.onStateChanged)
        #raid.enableNoTimeout
        self.checkBox_6.setChecked(False)
        #game.summonDefault
        self.checkBox_12.setChecked(False)
        #nightmare.enableNightmare
        self.checkBox_14.setChecked(False)
        self.checkBox_14.clicked.connect(self.onStateChanged)
        self.lineEdit_4.setEnabled(False)
        self.spinBox_9.setEnabled(False)
        self.spinBox_10.setEnabled(False)
        self.comboBox_5.setEnabled(False)
        #game.debugMode
        self.checkBox_13.setChecked(False)

        self.lineEdit_3.clicked.connect(self.openFileNameDialog)
        self.lineEdit_4.clicked.connect(self.openFileNameDialog)
        self.pushButton_2.clicked.connect(self.saveFarmList)

        # 战斗脚本内容
        self.mainscript = []
        self.mainscript_name = ''
        self.nmscript = []
        self.nmscript_name = ''

    def saveFarmList(self):
        # 保存战斗队列
        dirs = self.ROOT_PATH+'/farm_queue'
        import shutil
        shutil.rmtree(dirs)
        os.mkdir(dirs)
        self.saveSettings(dirs)

    def getElement(self, summons_list):
        # 返回召唤石属性列表
        elements = []
        for s in summons_list:
            for k,v in self.summons_dict.items():
                if s in v["summons"]:
                    elements.append(k)
                    break
        return elements

    def saveSettings(self,save_path):
        # 保存运行配置
        setting_dict = {}
        setting_dict["game"]["combatScriptName"] = self.mainscript_name
        setting_dict["game"]["combatScript"] = self.mainscript
        setting_dict["game"]["farmingMode"] = self.translate(self.comboBox.currentText())
        setting_dict["game"]["item"] = self.translate(self.comboBox_6.currentText())
        setting_dict["game"]["mission"] = self.translate(self.comboBox_2.currentText())
        setting_dict["game"]["map"] = self.translate(self.comboBox_3.currentText())
        setting_dict["game"]["itemAmount"] = self.spinBox.value()
        setting_dict["game"]["summons"] = self.translate(self.comboBox_4.currentData())
        setting_dict["game"]["summonDefault"] = self.checkBox_12.isChecked()
        setting_dict["game"]["summonElements"] = self.getElement(self.comboBox_4.currentData())
        setting_dict["game"]["groupNumber"] = self.spinBox_3.value()
        setting_dict["game"]["partyNumber"] = self.spinBox_2.value()
        setting_dict["game"]["debugMode"] = self.checkBox_13.isChecked()
        setting_dict["twitter"]["twitterUseVersion2"] = False
        setting_dict["twitter"]["twitterAPIKey"] = ''
        setting_dict["twitter"]["twitterAPIKeySecret"] = ''
        setting_dict["twitter"]["twitterAccessToken"] = ''
        setting_dict["twitter"]["twitterAccessTokenSecret"] = ''
        setting_dict["twitter"]["twitterBearerToken"] = ''
        setting_dict["discord"]["enableDiscordNotifications"] = False
        setting_dict["discord"]["discordToken"] = ''
        setting_dict["discord"]["discordUserID"] = ''
        setting_dict["api"]["enableOptInAPI"] = False
        setting_dict["api"]["username"] = ''
        setting_dict["api"]["password"] = ''
        setting_dict["configuration"]["enableAutoRestore"] = True
        setting_dict["configuration"]["enableFullElixir"] = False
        setting_dict["configuration"]["enableSoulBalm"] = False
        setting_dict["configuration"]["enableBezierCurveMouseMovement"] = self.checkBox_2.isChecked()
        setting_dict["configuration"]["mouseSpeed"] = self.doubleSpinBox.value()
        setting_dict["configuration"]["enableDelayBetweenRuns"] = self.checkBox_3.isChecked()
        setting_dict["configuration"]["delayBetweenRuns"] = self.spinBox_4.value()
        setting_dict["configuration"]["enableRandomizedDelayBetweenRuns"] = self.checkBox_4.isChecked()
        setting_dict["configuration"]["delayBetweenRunsLowerBound"] =  self.spinBox_6.value()
        setting_dict["configuration"]["delayBetweenRunsUpperBound"] =  self.spinBox_7.value()
        setting_dict["configuration"]["enableRefreshDuringCombat"] = self.checkBox_7.isChecked()
        setting_dict["configuration"]["enableAutoQuickSummon"] = self.checkBox_8.isChecked()
        setting_dict["configuration"]["enableBypassResetSummon"] = self.checkBox.isChecked()
        setting_dict["configuration"]["staticWindow"] = self.checkBox_9.isChecked()
        setting_dict["configuration"]["enableMouseSecurityAttemptBypass"] = self.checkBox_10.isChecked()
        setting_dict["misc"]["guiLowPerformanceMode"] = True
        setting_dict["misc"]["alternativeCombatScriptSelector"] = self.checkBox_11.isChecked()
        setting_dict["nightmare"]["enableNightmare"] = self.checkBox_14.isChecked()
        setting_dict["nightmare"]["enableCustomNightmareSettings"] = True
        setting_dict["nightmare"]["nightmareCombatScriptName"] = self.nmscript_name
        setting_dict["nightmare"]["nightmareCombatScript"] = self.nmscript
        setting_dict["nightmare"]["nightmareSummons"] = self.translate(self.comboBox_5.currentData())
        setting_dict["nightmare"]["nightmareSummonElements"] = self.getElement(self.comboBox_5.currentData())
        setting_dict["nightmare"]["nightmareGroupNumber"] = self.spinBox_9.value()
        setting_dict["nightmare"]["nightmarePartyNumber"] = self.spinBox_10.value()
        setting_dict["event"]["enableLocationIncrementByOne"] = False
        setting_dict["event"]["selectBottomCategory"] = False
        setting_dict["raid"]["enableAutoExitRaid"] = self.checkBox_5.isChecked()
        setting_dict["raid"]["timeAllowedUntilAutoExitRaid"] = self.spinBox_8.value()
        setting_dict["raid"]["enableNoTimeout"] = self.checkBox_6.isChecked()
        setting_dict["arcarum"]["enableStopOnArcarumBoss"] = True
        setting_dict["generic"]["enableForceReload"] = False
        setting_dict["xenoClash"]["selectTopOption"] = True
        setting_dict["adjustment"]["enableCalibrationAdjustment"] = False
        setting_dict["adjustment"]["adjustCalibration"] = 5
        setting_dict["adjustment"]["enableGeneralAdjustment"] = False
        setting_dict["adjustment"]["adjustButtonSearchGeneral"] = 5
        setting_dict["adjustment"]["adjustHeaderSearchGeneral"] = 5
        setting_dict["adjustment"]["enablePendingBattleAdjustment"] = False
        setting_dict["adjustment"]["adjustBeforePendingBattle"] = 1
        setting_dict["adjustment"]["adjustPendingBattle"] = 2
        setting_dict["adjustment"]["enableCaptchaAdjustment"] = False
        setting_dict["adjustment"]["adjustCaptcha"] = 5
        setting_dict["adjustment"]["enableSupportSummonSelectionScreenAdjustment"] = False
        setting_dict["adjustment"]["adjustSupportSummonSelectionScreen"] = 30
        setting_dict["adjustment"]["enableCombatModeAdjustment"] = False
        setting_dict["adjustment"]["adjustCombatStart"] = 50
        setting_dict["adjustment"]["adjustDialog"] = 2
        setting_dict["adjustment"]["adjustSkillUsage"] = 5
        setting_dict["adjustment"]["adjustSummonUsage"] = 5
        setting_dict["adjustment"]["adjustWaitingForReload"] = 3
        setting_dict["adjustment"]["adjustWaitingForAttack"] = 100
        setting_dict["adjustment"]["adjustCheckForNoLootScreen"] = 1
        setting_dict["adjustment"]["adjustCheckForBattleConcludedPopup"] = 1
        setting_dict["adjustment"]["adjustCheckForExpGainedPopup"] = 1
        setting_dict["adjustment"]["adjustCheckForLootCollectionScreen"] = 1
        setting_dict["adjustment"]["enableArcarumAdjustment"] = False
        setting_dict["adjustment"]["adjustArcarumAction"] = 3
        setting_dict["adjustment"]["adjustArcarumStageEffect"] = 10
        setting_dict["sandbox"]["enableDefender"] = False
        setting_dict["sandbox"]["enableGoldChest"] = False
        setting_dict["sandbox"]["enableCustomDefenderSettings"] = False
        setting_dict["sandbox"]["numberOfDefenders"] = 1
        setting_dict["sandbox"]["defenderCombatScriptName"] = ""
        setting_dict["sandbox"]["defenderCombatScript"] = []
        setting_dict["sandbox"]["defenderGroupNumber"] = 1
        setting_dict["sandbox"]["defenderPartyNumber"] = 1


    def translate(self,cn_str):
        return en_Str

    def openFileNameDialog(self):
        lineedit = self.sender()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"打开文件", "","TXT Files (*.txt)", options=options)
        if fileName:
            lineedit.setText(fileName)
            self.txtFile = lineedit.text()
            if 'main_script' == lineedit.objectName():
                self.mainscript = open(self.txtFile,encoding='utf-8').readlines()
                self.mainscript_name = os.path.split(fileName)[1]
            else:
                self.nmscript = open(self.txtFile,encoding='utf-8').readlines()
                self.nmscript_name = os.path.split(fileName)[1]



    @QtCore.pyqtSlot(str)
    def onActivatedText(self, text):
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_6.clear()
        self.comboBox_2.addItems(list(self.gamemode_dict[text].keys()))
        if text != "共斗":
            maps = self.gamemode_dict[text][self.comboBox_2.currentText()]['map']
            if type(maps) is not list:
                maps = [maps]
            self.comboBox_3.addItems(maps)
        items = self.gamemode_dict[text][self.comboBox_2.currentText()]['items']
        if type(items) is not list:
            items = [items]
        self.comboBox_6.addItems(items)

    @QtCore.pyqtSlot(str)
    def onActivatedSubText(self, text):
        self.comboBox_3.clear()
        self.comboBox_6.clear()
        if self.comboBox.currentText() != "共斗":
            maps = self.gamemode_dict[self.comboBox.currentText()][text]['map']
            if type(maps) is not list:
                maps = [maps]
            self.comboBox_3.addItems(maps)
        items = self.gamemode_dict[self.comboBox.currentText()][text]['items']
        if type(items) is not list:
            items = [items]
        self.comboBox_6.addItems(items)

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
        if self.checkBox_3.isChecked():
            self.spinBox_4.setEnabled(True)
        else:
            self.spinBox_4.setEnabled(False)
        if self.checkBox_5.isChecked():
            self.spinBox_8.setEnabled(True)
        else:
            self.spinBox_8.setEnabled(False)
        if self.checkBox_14.isChecked():
            self.lineEdit_4.setEnabled(True)
            self.spinBox_9.setEnabled(True)
            self.spinBox_10.setEnabled(True)
            self.comboBox_5.setEnabled(True)
        else:
            self.lineEdit_4.setEnabled(False)
            self.spinBox_9.setEnabled(False)
            self.spinBox_10.setEnabled(False)
            self.comboBox_5.setEnabled(False)


if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    win=GBF_AutoTool()
    win.show()
    sys.exit(app.exec_())