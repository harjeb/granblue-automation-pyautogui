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
from PyQt5 import QtGui
from io import StringIO
import traceback
import socket
import shutil
import re
import logging
import ctypes
CP_console = f"cp{ctypes.cdll.kernel32.GetConsoleOutputCP()}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists('log'):
    os.makedirs('log')

current_date = time.strftime("%m_%d_%H_%M_%S_", time.localtime())
logname = 'log/' + current_date + 'ga.log'  # 指定输出的日志文件名

fh = logging.FileHandler(logname, encoding='utf-8', mode='a')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
custom_format = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
# formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
formatter = logging.Formatter(custom_format)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


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


def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon


image_base64 = b"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"



class Sleep_Thread(QThread):
    status = QtCore.pyqtSignal()

    def __init__(self, _time):
        super(Sleep_Thread,self).__init__()
        self.sleep_time = _time

    def run(self):
        time.sleep(self.sleep_time)
        self.status.emit()


class GBF_AutoTool(QWidget, Ui_Form):
    def __init__(self,parent=None):
        super(GBF_AutoTool, self).__init__(parent)
        self.setupUi(self)
        # UI初始化
        icon = iconFromBase64(image_base64)
        self.setWindowIcon(icon)
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(__file__)
            self.ROOT_PATH = application_path
            #print(self.ROOT_PATH)
            _file = open(f"{self.ROOT_PATH}/data/data_zhcn.json",encoding='utf-8')
            _summon = open(f"{self.ROOT_PATH}/data/summons_zhcn.json",encoding='utf-8')
            _translate = open(f"{self.ROOT_PATH}/data/translate.json",encoding='utf-8')
        except FileNotFoundError:
            QMessageBox.warning(self,
                                "错误",
                                "没找到资源文件",
                                QMessageBox.Yes)
            sys.exit(1)

        self.gamemode_dict = json.load(_file)
        self.summons_dict = json.load(_summon)
        self.translate_dict = json.load(_translate)

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
        self.checkBox_4.setChecked(False)
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
        self.checkBox_8.setChecked(True)
        #configuration.enableBypassResetSummon
        self.checkBox.setChecked(True)
        #configuration.staticWindow
        self.checkBox_9.setChecked(True)
        #configuration.enableMouseSecurityAttemptBypass
        self.checkBox_10.setChecked(False)
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
        #sandbox.numberOfDefenders
        self.checkBox_18.clicked.connect(self.onStateChanged)
        self.spinBox_5.setEnabled(False)
        self.lineEdit_6.setEnabled(False)
        self.spinBox_11.setEnabled(False)
        self.spinBox_12.setEnabled(False)
        #chaojiying
        self.checkBox_15.clicked.connect(self.onStateChanged)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        #xenoClash.selectTopOption
        self.checkBox_16.setChecked(True)
        #sandbox.enableGoldChest
        self.checkBox_17.setChecked(True)
        #event.enableLocationIncrementByOne
        #Settings.first_event
        self.checkBox_21.setChecked(True)

        self.lineEdit_3.clicked.connect(self.openFileNameDialog)
        self.lineEdit_4.clicked.connect(self.openFileNameDialog)
        self.lineEdit_6.clicked.connect(self.openFileNameDialog)
        self.pushButton_2.clicked.connect(self.saveFarmList)

        # 战斗脚本内容
        self.mainscript = []
        self.mainscript_name = ''
        self.nmscript = []
        self.nmscript_name = ''
        self.defenderscript_name = ''
        self.defenderscript = []

        # 任务队列
        self.action_queue = [0]

        self.pushButton.clicked.connect(self.start)

        dirs = self.ROOT_PATH+'/backend/farm_queue'
        if os.path.exists(dirs):
            shutil.rmtree(dirs)

        # 游戏状态
        self.running = False

        self.process = QtCore.QProcess()
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.process.finished.connect(self.onFinished)
        # self.main_thread = Game_Thread()


    def saveFarmList(self):
        # 判断设置是否正确
        if self.check_settings():
            latest = self.action_queue[-1]
            self.action_queue.append(1+latest)
            # 保存战斗队列
            dirs = self.ROOT_PATH+'/backend/farm_queue'
            try:
                if not os.path.exists(dirs):
                    os.mkdir(dirs)
                filenum = str(self.action_queue[-1])
                self.saveSettings(dirs, 'settings'+filenum)
                self.update_queue("任务"+str(filenum)+",")
            except Exception as e:
                print(e)
                QMessageBox.warning(self,
                        "错误",
                        "错误",
                        QMessageBox.Yes)
        else:
            QMessageBox.warning(self,
                        "错误",
                        "配置不正确",
                        QMessageBox.Yes)

    def update_queue(self,quest):
        tmp = self.lineEdit.text() + quest
        self.lineEdit.setText(tmp)

    def start(self):
        if self.lineEdit.text() == '':
            QMessageBox.warning(self,
                        "错误",
                        "未找到脚本任务",
                        QMessageBox.Yes)
        else:
            if not self.running:
                self.pushButton.setText("停止")
                self.running = True
                queue = self.lineEdit.text()
                self.process.start('python controller.py %s' % queue)
            else:
                reply = QMessageBox.question(self, '', '是否停止Farm?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # 停止Farm
                    self.stop()

    def check_settings(self):
        flag = True
        if self.lineEdit_3.text() == '':
            flag = False
            self.lineEdit_3.setStyleSheet("border: 1px solid red;")
        if self.comboBox_4.currentText() == '' and not self.checkBox_12.isChecked():
            flag = False
            self.comboBox_4.setStyleSheet("border: 1px solid red;")
        if (self.comboBox_5.currentText() == '' or self.lineEdit_4.text() == '') and self.checkBox_14.isChecked():
            flag = False
            if self.comboBox_5.currentText() == '':
                self.comboBox_5.setStyleSheet("border: 1px solid red;")
            if self.lineEdit_4.text() == '':
                self.lineEdit_4.setStyleSheet("border: 1px solid red;")
        return flag



    def stop(self):
        self.process.close()
        self.pushButton.setText("开始")
        self.running = False

    def _update_sleep_status(self):
        self.sleep_over = True

    def getElement(self, summons_list):
        # 返回召唤石属性列表
        elements = []
        for s in summons_list:
            for k,v in self.summons_dict.items():
                if s in v["summons"]:
                    elements.append(k)
                    break
        return elements

    def saveSettings(self,save_path,setname):
        # 保存运行配置
        setting_dict = {"game":{},
                        "twitter":{},
                        "discord":{},
                        "api":{},
                        "configuration":{},
                        "misc":{},
                        "nightmare":{},
                        "event":{},
                        "raid":{},
                        "arcarum":{},
                        "generic":{},
                        "xenoClash":{},
                        "adjustment":{},
                        "sandbox":{},
                        "chaojiying":{}}
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
        setting_dict["event"]["enableLocationIncrementByOne"] = self.checkBox_19.isChecked()
        setting_dict["event"]["selectBottomCategory"] = self.checkBox_20.isChecked()
        setting_dict["raid"]["enableAutoExitRaid"] = self.checkBox_5.isChecked()
        setting_dict["raid"]["timeAllowedUntilAutoExitRaid"] = self.spinBox_8.value()
        setting_dict["raid"]["enableNoTimeout"] = self.checkBox_6.isChecked()
        setting_dict["arcarum"]["enableStopOnArcarumBoss"] = True
        setting_dict["generic"]["enableForceReload"] = False
        setting_dict["xenoClash"]["selectTopOption"] = self.checkBox_16.isChecked()
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
        setting_dict["sandbox"]["enableDefender"] = self.checkBox_18.isChecked()
        setting_dict["sandbox"]["enableGoldChest"] = self.checkBox_17.isChecked()
        setting_dict["sandbox"]["enableCustomDefenderSettings"] = self.checkBox_18.isChecked()
        setting_dict["sandbox"]["numberOfDefenders"] = self.spinBox_5.value()
        setting_dict["sandbox"]["defenderCombatScriptName"] = self.defenderscript_name
        setting_dict["sandbox"]["defenderCombatScript"] = self.defenderscript
        setting_dict["sandbox"]["defenderGroupNumber"] = self.spinBox_11.value()
        setting_dict["sandbox"]["defenderPartyNumber"] = self.spinBox_12.value()
        setting_dict["chaojiying"]["username"] = self.lineEdit_2.text()
        setting_dict["chaojiying"]["password"] = self.lineEdit_5.text()
        setting_dict["event"]["first"] = self.checkBox_21.isChecked()

        json_str = json.dumps(setting_dict, indent=4)
        with open(save_path+'/%s.json' % setname, 'w') as json_file:
            json_file.write(json_str)

    def translate(self, obj):
        tmp = []
        if type(obj) is str:
            if self.is_contain_chinese(obj):
                return self.translate_dict[obj]
            else:
                return obj
        else:
            for o in obj:
                if self.is_contain_chinese(o):
                    tmp.append(self.translate_dict[o])
                else:
                    tmp.append(o)
            return tmp

    def is_contain_chinese(self,check_str):
        """
        判断字符串中是否包含中文
        :param check_str: {str} 需要检测的字符串
        :return: {bool} 包含返回True， 不包含返回False
        """
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    def openFileNameDialog(self):
        lineedit = self.sender()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"打开文件", "","TXT Files (*.txt)", options=options)
        if fileName:
            lineedit.setText(fileName)
            self.txtFile = lineedit.text()
            if 'main_script' == lineedit.objectName():
                lines = open(self.txtFile,encoding='utf-8').readlines()
                self.mainscript = []
                for line in lines:
                    self.mainscript.append(line.strip())
                self.mainscript_name = os.path.split(fileName)[1]
                lineedit.setStyleSheet("")
            elif 'nightmare_script' == lineedit.objectName():
                lines2 = open(self.txtFile,encoding='utf-8').readlines()
                self.nmscript = []
                for line in lines2:
                    self.nmscript.append(line.strip())
                self.nmscript_name = os.path.split(fileName)[1]
                lineedit.setStyleSheet("")
            else:
                lines3 = open(self.txtFile,encoding='utf-8').readlines()
                self.defenderscript = []
                for line in lines3:
                    self.defenderscript.append(line.strip())
                self.defenderscript_name = os.path.split(fileName)[1]
                lineedit.setStyleSheet("")

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
        if self.checkBox_18.isChecked():
            self.spinBox_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.spinBox_11.setEnabled(True)
            self.spinBox_12.setEnabled(True)
        else:
            self.spinBox_5.setEnabled(False)
            self.lineEdit_6.setEnabled(False)
            self.spinBox_11.setEnabled(False)
            self.spinBox_12.setEnabled(False)
        if self.checkBox_15.isChecked():
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_5.setEnabled(True)
        else:
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_5.setEnabled(False)

    def onReadyReadStandardError(self):
        try:
            error = self.process.readAllStandardError().data().decode('GBK')
            self.textBrowser.appendPlainText(error.strip())
            logger.error(error.strip())
        except:
            error = self.process.readAllStandardError().data().decode()
            self.textBrowser.appendPlainText(error.strip())
            logger.error(error.strip())
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def onReadyReadStandardOutput(self):
        try:
            result = self.process.readAllStandardOutput().data().decode('GBK')
            self.textBrowser.appendPlainText(result.strip())
            logger.info(result.strip())
        except:
            error = self.process.readAllStandardError().data().decode()
            self.textBrowser.appendPlainText(error.strip())
            logger.error(error.strip())
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)

    def onFinished(self, exitCode, exitStatus):
        if exitStatus == 0:
            try:
                self.textBrowser.appendPlainText("---------")
                self.textBrowser.appendPlainText("========Farm 结束========")
                self.textBrowser.moveCursor(QtGui.QTextCursor.End)
                logger.info("---------")
                logger.info("========Farm 结束========")
                self.process.close()
                self.running = False
                self.pushButton.setText('开始')
            except:
                logger.info("---------")
                logger.info("========Farm 结束========")
                self.process.close()
                self.textBrowser.moveCursor(QtGui.QTextCursor.End)
                self.running = False
                self.pushButton.setText('开始')


if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    win=GBF_AutoTool()
    win.show()
    sys.exit(app.exec_())