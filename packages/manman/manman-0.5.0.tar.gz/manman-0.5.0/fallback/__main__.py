"""GUI for application deployment and monitoring of servers and 
applications related to specific apparatus.
"""
__version__ = 'v0.4.0 2025-05-21'# 
#TODO: Use QTableView instead of QTableWidget, it is more flexible

import sys, os, time, subprocess, argparse, threading
from functools import partial
from importlib import import_module

from PyQt5 import QtWidgets as QW, QtGui, QtCore

from . import helpers as H
from . import detachable_tabs

Apparatus = H.list_of_apparatus()

ManCmds = ['Check','Start','Stop','Command']
Col = {'Managers':0, 'status':1, 'action':2, 'response':3}
BoldFont = QtGui.QFont("Helvetica", 14, QtGui.QFont.Bold)
LastColumnWidth=400

qApp = QW.QApplication(sys.argv)

class MyTable(QW.QTableWidget):

    def sizeHint(self):
        hh = self.horizontalHeader()
        vh = self.verticalHeader()
        fw = self.frameWidth() * 2
        return QtCore.QSize(
            hh.length() + vh.sizeHint().width() + fw,
            vh.length() + hh.sizeHint().height() + fw)

def currentDaTable():
    return MyWin.tabWidget.currentWidget().mytable

class MyWin(QW.QMainWindow):# it may sense to subclass it from QW.QMainWindow
    tw = None
    tabWidget = None
    tableWidgets = []
    manRow = {}
    startup = None
    timer = QtCore.QTimer()
    firstAction=True

    def __init__(self):
        QW.QWidget.__init__(self)# is it needed?
        MyWin.tabWidget = detachable_tabs.DetachableTabWidget()
        self.setCentralWidget(MyWin.tabWidget)
        print(f'tabWidget created')

        MyWin.tw = self.create_mytable('')

        if pargs.interval != 0.:
            MyWin.timer.timeout.connect(periodicCheck)
            MyWin.timer.setInterval(int(pargs.interval*1000.))
            MyWin.timer.start()
        MyWin.tw.show()

    def create_mytable(self, filename):
        tw =  MyTable()
        tw.setWindowTitle('manman')
        tw.setColumnCount(4)
        tw.setHorizontalHeaderLabels(Col.keys())
        wideRow(tw, 0,'Operational Apps')
        
        sb = QW.QComboBox()
        sb.addItems(['Check All','Start All','Stop All', 'Edit '])
        sb.activated.connect(allManAction)
        sb.setToolTip('Execute selected action for all applications')
        tw.setCellWidget(0, Col['action'], sb)

        operationalManager = True
        for manName in MyWin.startup:
            rowPosition = tw.rowCount()
            if manName.startswith('tst_'):
                if operationalManager:
                    operationalManager = False
                    wideRow(tw, rowPosition,'Test Apps')
                    
                    rowPosition += 1
            insertRow(tw, rowPosition)
            self.manRow[manName] = rowPosition
            item = QW.QTableWidgetItem(manName)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            try:    item.setToolTip(MyWin.startup[manName]['help'])
            except: pass
            tw.setItem(rowPosition, Col['Managers'], item)
            if operationalManager:
                item.setFont(BoldFont)
                item.setBackground(QtGui.QColor('lightCyan'))
            tw.setItem(rowPosition, Col['status'],
              QW.QTableWidgetItem('?'))
            sb = QW.QComboBox()
            sb.addItems(ManCmds)
            sb.activated.connect(partial(manAction,manName))
            try:    sb.setToolTip(MyWin.startup[manName]['help'])
            except: pass
            tw.setCellWidget(rowPosition, Col['action'], sb)
            tw.setItem(rowPosition, Col['response'],
              QW.QTableWidgetItem(''))
        return tw

def wideRow(tw, rowPosition,txt):
    insertRow(tw, rowPosition)
    tw.setSpan(rowPosition,0,1,2)
    item = QW.QTableWidgetItem(txt)
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    item.setBackground(QtGui.QColor('lightGray'))
    item.setFont(BoldFont)
    tw.setItem(rowPosition, Col['Managers'], item)

def insertRow(tw, rowPosition):
    tw.insertRow(rowPosition)
    tw.setRowHeight(rowPosition, 1)  

def allManAction(cmdidx:int):
    H.printv(f'allManAction: {cmdidx}')
    if cmdidx == 3:
        _edit()
        return
    for manName in MyWin.startup:
        #if manName.startswith('tst'):
        #    continue
        manAction(manName, cmdidx)

def _edit():
    subprocess.call(['xdg-open', pargs.configFile])

def manAction(manName, cmdObj):
    # if called on click, then cmdObj is index in ManCmds, otherwise it is a string
    if MyWin.firstAction:
        MyWin.tw.setColumnWidth(3, LastColumnWidth)
        MyWin.firstAction = False
    cmd = cmdObj if isinstance(cmdObj,str) else ManCmds[cmdObj]
    rowPosition = MyWin.manRow[manName]
    H.printv(f'manAction: {manName, cmd}')
    cmdstart = MyWin.startup[manName]['cmd']    
    process = MyWin.startup[manName].get('process', f'{cmdstart}')

    if cmd == 'Check':
        H.printv(f'checking process {process} ')
        status = ['not running','is started'][H.is_process_running(process)]
        item = MyWin.tw.item(rowPosition,Col['status'])
        if not 'tst_' in manName:
            color = 'lightGreen' if 'started' in status else 'pink'
            item.setBackground(QtGui.QColor(color))
        item.setText(status)
            
    elif cmd == 'Start':
        MyWin.tw.item(rowPosition, Col['response']).setText('')
        if H.is_process_running(process):
            txt = f'Is already running manager {manName}'
            #print(txt)
            MyWin.tw.item(rowPosition, Col['response']).setText(txt)
            return
        H.printv(f'starting {manName}')
        item = MyWin.tw.item(rowPosition, Col['status'])
        if not 'tst_' in manName:
            item.setBackground(QtGui.QColor('lightYellow'))
        item.setText('starting...')
        path = MyWin.startup[manName].get('cd')
        H.printi('Executing commands:')
        if path:
            path = path.strip()
            expandedPath = os.path.expanduser(path)
            try:
                os.chdir(expandedPath)
            except Exception as e:
                txt = f'ERR: in chdir: {e}'
                MyWin.tw.item(rowPosition, Col['response']).setText(txt)
                return
            print(f'cd {os.getcwd()}')
        print(cmdstart)
        expandedCmd = os.path.expanduser(cmdstart)
        cmdlist = expandedCmd.split()
        shell = MyWin.startup[manName].get('shell',False)
        H.printv(f'popen: {cmdlist}, shell:{shell}')
        try:
            proc = subprocess.Popen(cmdlist, shell=shell, #close_fds=True,# env=my_env,
              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            H.printv(f'Exception: {e}') 
            MyWin.tw.item(rowPosition, Col['response']).setText(str(e))
            return
        MyWin.timer.singleShot(5000,partial(deferredCheck,(manName,rowPosition)))

    elif cmd == 'Stop':
        MyWin.tw.item(rowPosition, Col['response']).setText('')
        H.printv(f'stopping {manName}')
        cmd = f'pkill -f "{process}"'
        H.printi(f'Executing:\n{cmd}')
        os.system(cmd)
        time.sleep(0.1)
        manAction(manName, 'Check')

    elif cmd == 'Command':
        try:
            cd = MyWin.startup[manName]['cd']
            cmd = f'cd {cd}; {cmdstart}'
        except Exception as e:
            cmd = cmdstart
        print(f'Command:\n{cmd}')
        MyWin.tw.item(rowPosition, Col['response']).setText(cmd)
        return
    # Action was completed successfully, cleanup the status cell

def deferredCheck(args):
    manName,rowPosition = args
    manAction(manName, 'Check')
    if 'start' not in MyWin.tw.item(rowPosition, Col['status']).text():
        MyWin.tw.item(rowPosition, Col['response']).setText('Failed to start')

def periodicCheck():
    allManAction('Check')

def main():
    global pargs
    parser = argparse.ArgumentParser('python -m manman',
      description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
      epilog=f'Version {__version__}')
    parser.add_argument('-c', '--configDir', default=H.ConfigDir, help=\
      'Directory, containing apparatus configuration scripts')
    parser.add_argument('-t', '--interval', default=10., help=\
      'Interval in seconds of periodic checking. If 0 then no checking')
    parser.add_argument('-v', '--verbose', action='count', default=0, help=\
      'Show more log messages (-vv: show even more).')
    parser.add_argument('apparatus', help=\
      'Apparatus', nargs='?', choices=Apparatus, default='TST')
    pargs = parser.parse_args()
    #pargs.log = None# disable logging fo now
    H.Constant.verbose = pargs.verbose

    mname = 'apparatus_'+pargs.apparatus
    pargs.configFile = f'{pargs.configDir}/{mname}.py'
    print(f'Config file: {pargs.configFile}')
    module = import_module(mname)
    #print(f'imported {mname} {module.__version__}')
    MyWin.startup = module.startup

    MyWin()
    allManAction('Check')

    # arrange keyboard interrupt to kill the program
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    #start GUI
    try:
        qApp.instance().exec_()
        #sys.exit(qApp.exec_())
    except Exception as e:#KeyboardInterrupt:
        # This exception never happens
        print('keyboard interrupt: exiting')
    print('Application exit')

if __name__ == '__main__':
    main()

