"""GUI for application deployment and monitoring of servers and 
applications related to specific apparatus.
"""
__version__ = 'v0.5.0 2025-05-27'# main() is separated to __main__.py, qtpy, 

import sys, os, time, subprocess, argparse, threading
from functools import partial
from importlib import import_module

from qtpy import QtWidgets as QW, QtGui, QtCore

from . import helpers as H
from . import detachable_tabs

#``````````````````Constants``````````````````````````````````````````````````
ManCmds = ['Check','Start','Stop','Command']
Col = {'Applications':0, 'status':1, 'action':2, 'response':3}
BoldFont = QtGui.QFont("Helvetica", 14, QtGui.QFont.Bold)
LastColumnWidth=400

#``````````````````Helpers````````````````````````````````````````````````````
def select_files_interactively(directory, title='Select apparatus_* files'):
    dialog = QW.QFileDialog()
    dialog.setFileMode( QW.QFileDialog.FileMode() )
    ffilter = 'pypet (apparatus_*)'
    files = dialog.getOpenFileNames( None, title, directory, ffilter)[0]
    return files

def create_folderMap():
    # create map of {folder1: [file1,...], folder2...}
    #print(f'c,a: {Window.pargs.configDir, Window.pargs.apparatus}')
    folders = {}
    if Window.pargs.configDir is None:
        files = [os.path.abspath(i) for i in Window.pargs.apparatus]
    else:
        absfolder = os.path.abspath(Window.pargs.configDir)
        if len(Window.pargs.apparatus) == 0:
            files = select_files_interactively(absfolder)
        else:
            files = [absfolder+'/'+i for i in Window.pargs.apparatus]
    for f in files:
        folder,tail = os.path.split(f)
        if not (tail.startswith('apparatus_') and tail.endswith('.py')):
            H.printe('Config file should have prefix "apparatus_" and suffix ".py"')
            sys.exit(1)
        if folder not in folders:
            folders[folder] = []
        folders[folder].append(tail)
    return folders

def launch_default_editor(configFile):
    subprocess.call(['xdg-open', configFile])

def is_process_running(cmdstart):
    try:
        subprocess.check_output(["pgrep", '-f', cmdstart])
        return True
    except subprocess.CalledProcessError:
        return False
#``````````````````Table Widget```````````````````````````````````````````````
def current_mytable():
    return Window.tabWidget.currentWidget()
class MyTable(QW.QTableWidget):
    def __init__(self, startup, configFile):
        super().__init__()
        self.startup = startup
        self.configFile = configFile

    """ Help windows to adjust geometry
    def sizeHint(self):
        hh = self.horizontalHeader()
        vh = self.verticalHeader()
        fw = self.frameWidth() * 2
        return QtCore.QSize(
            hh.length() + vh.sizeHint().width() + fw,
            vh.length() + hh.sizeHint().height() + fw)
    """

#``````````````````Main Window````````````````````````````````````````````````
class Window(QW.QMainWindow):# it may sense to subclass it from QW.QMainWindow
    pargs = None
    tableWidgets = []
    manRow = {}
    #startup = None
    timer = QtCore.QTimer()
    firstAction=True

    def __init__(self):
        super().__init__()
        H.Verbose = Window.pargs.verbose
        folders = create_folderMap()
        H.printi(f'Configuration files: {folders}')

        # create tabWidget
        Window.tabWidget = detachable_tabs.DetachableTabWidget()
        Window.tabWidget.currentChanged.connect(periodicCheck)
        self.setCentralWidget(Window.tabWidget)
        H.printv(f'tabWidget created')

        for folder,files in folders.items():
            sys.path.append(folder)
            for fname in files:
                mytable = self.create_mytable(folder, fname)
                Window.tableWidgets.append(mytable)
                #print(f'Adding tab: {fname}')
                Window.tabWidget.addTab(mytable, fname[:-3])

        self.setWindowTitle('manman')
        #self.show()

        periodicCheck()
        if Window.pargs.interval != 0.:
            Window.timer.timeout.connect(periodicCheck)
            Window.timer.setInterval(int(Window.pargs.interval*1000.))
            Window.timer.start()

    def create_mytable(self, folder, fname):
        mname = fname[:-3]
        H.printv(f'importing {mname}')
        module = import_module(mname)
        H.printv(f'imported {mname} {module.__version__}')
        startup = module.startup

        mytable =  MyTable(startup, folder+'/'+fname)
        #mytable.setWindowTitle('manman')
        mytable.setColumnCount(4)
        mytable.setHorizontalHeaderLabels(Col.keys())
        wideRow(mytable, 0,'Operational Apps')
        
        sb = QW.QComboBox()
        sb.addItems(['Check All','Start All','Stop All', 'Edit '])
        sb.activated.connect(allManAction)
        sb.setToolTip('Execute selected action for all applications')
        mytable.setCellWidget(0, Col['action'], sb)
        #return mytable

        operationalManager = True
        for manName in startup:
            rowPosition = mytable.rowCount()
            if manName.startswith('tst_'):
                if operationalManager:
                    operationalManager = False
                    wideRow(mytable, rowPosition,'Test Apps')
                    rowPosition += 1
            insertRow(mytable, rowPosition)
            self.manRow[manName] = rowPosition
            item = QW.QTableWidgetItem(manName)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            try:    item.setToolTip(startup[manName]['help'])
            except: pass
            mytable.setItem(rowPosition, Col['Applications'], item)
            if operationalManager:
                item.setFont(BoldFont)
                item.setBackground(QtGui.QColor('lightCyan'))
            mytable.setItem(rowPosition, Col['status'],
              QW.QTableWidgetItem('?'))
            sb = QW.QComboBox()
            sb.addItems(ManCmds)
            sb.activated.connect(partial(manAction,manName))
            try:    sb.setToolTip(startup[manName]['help'])
            except: pass
            mytable.setCellWidget(rowPosition, Col['action'], sb)
            mytable.setItem(rowPosition, Col['response'],
              QW.QTableWidgetItem(''))
        return mytable

def wideRow(mytable, rowPosition,txt):
    insertRow(mytable, rowPosition)
    mytable.setSpan(rowPosition,0,1,2)
    item = QW.QTableWidgetItem(txt)
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    item.setBackground(QtGui.QColor('lightGray'))
    item.setFont(BoldFont)
    mytable.setItem(rowPosition, Col['Applications'], item)

def insertRow(mytable, rowPosition):
    mytable.insertRow(rowPosition)
    mytable.setRowHeight(rowPosition, 1)  

def allManAction(cmdidx:int):
    #print(f'allManAction: {cmdidx}')
    mytable = current_mytable()
    if cmdidx == 3:
        launch_default_editor(mytable.configFile)
        return
    for manName in mytable.startup:
        #if manName.startswith('tst'):
        #    continue
        manAction(manName, cmdidx)

def manAction(manName, cmdObj):
    # if called on click, then cmdObj is index in ManCmds, otherwise it is a string
    mytable = current_mytable()
    if Window.firstAction:
        mytable.setColumnWidth(3, LastColumnWidth)
        Window.firstAction = False
    cmd = cmdObj if isinstance(cmdObj,str) else ManCmds[cmdObj]
    rowPosition = Window.manRow[manName]
    H.printv(f'manAction: {manName, cmd}')
    startup = current_mytable().startup
    cmdstart = startup[manName]['cmd']    
    process = startup[manName].get('process', f'{cmdstart}')

    if cmd == 'Check':
        H.printv(f'checking process {process} ')
        status = ['not running','is started'][is_process_running(process)]
        item = mytable.item(rowPosition,Col['status'])
        if not 'tst_' in manName:
            color = 'lightGreen' if 'started' in status else 'pink'
            item.setBackground(QtGui.QColor(color))
        item.setText(status)
            
    elif cmd == 'Start':
        mytable.item(rowPosition, Col['response']).setText('')
        if is_process_running(process):
            txt = f'Is already running manager {manName}'
            #print(txt)
            mytable.item(rowPosition, Col['response']).setText(txt)
            return
        H.printv(f'starting {manName}')
        item = mytable.item(rowPosition, Col['status'])
        if not 'tst_' in manName:
            item.setBackground(QtGui.QColor('lightYellow'))
        item.setText('starting...')
        path = startup[manName].get('cd')
        H.printi('Executing commands:')
        if path:
            path = path.strip()
            expandedPath = os.path.expanduser(path)
            try:
                os.chdir(expandedPath)
            except Exception as e:
                txt = f'ERR: in chdir: {e}'
                mytable.item(rowPosition, Col['response']).setText(txt)
                return
            print(f'cd {os.getcwd()}')
        print(cmdstart)
        expandedCmd = os.path.expanduser(cmdstart)
        cmdlist = expandedCmd.split()
        shell = startup[manName].get('shell',False)
        H.printv(f'popen: {cmdlist}, shell:{shell}')
        try:
            proc = subprocess.Popen(cmdlist, shell=shell, #close_fds=True,# env=my_env,
              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            H.printv(f'Exception: {e}') 
            mytable.item(rowPosition, Col['response']).setText(str(e))
            return
        Window.timer.singleShot(5000,partial(deferredCheck,(manName,rowPosition)))

    elif cmd == 'Stop':
        mytable.item(rowPosition, Col['response']).setText('')
        H.printv(f'stopping {manName}')
        cmd = f'pkill -f "{process}"'
        H.printi(f'Executing:\n{cmd}')
        os.system(cmd)
        time.sleep(0.1)
        manAction(manName, 'Check')

    elif cmd == 'Command':
        try:
            cd = startup[manName]['cd']
            cmd = f'cd {cd}; {cmdstart}'
        except Exception as e:
            cmd = cmdstart
        print(f'Command:\n{cmd}')
        mytable.item(rowPosition, Col['response']).setText(cmd)
        return
    # Action was completed successfully, cleanup the status cell

def deferredCheck(args):
    manName,rowPosition = args
    manAction(manName, 'Check')
    mytable = current_mytable()
    if 'start' not in mytable.item(rowPosition, Col['status']).text():
        mytable.item(rowPosition, Col['response']).setText('Failed to start')

def periodicCheck():
    allManAction('Check')

