"""GUI for application deployment and monitoring of servers and 
applications related to specific apparatus.
"""
__version__ = 'v0.4.1 2025-05-23'# 

import sys, argparse
from qtpy.QtWidgets import QApplication

from . import manman, helpers

#``````````````````Main```````````````````````````````````````````````````````
def main():
    global pargs
    parser = argparse.ArgumentParser('python -m manman',
      description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter,
      epilog=f'Version {manman.__version__}')
    parser.add_argument('-c', '--configDir', help=\
      'Root directory of config files')
    parser.add_argument('-t', '--interval', default=10., help=\
      'Interval in seconds of periodic checking. If 0 then no checking')
    parser.add_argument('-v', '--verbose', action='count', default=0, help=\
      'Show more log messages (-vv: show even more).')
    parser.add_argument('apparatus', help=\
      'Apparatus config files', nargs='*')
    pargs = parser.parse_args()
    helpers.Verbose = pargs.verbose
    if pargs.configDir is None and len(pargs.apparatus) == 0:
        helpers.printe('Either apparatus or configDir should be specified')
        sys.exit()
    manman.Window.pargs = pargs# transfer pargs to manman module

    # arrange keyboard interrupt to kill the program
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    #start GUI
    app = QApplication(sys.argv)
    window = manman.Window()
    window.show()
    app.exec_()
    print('Application exit')

if __name__ == '__main__':
    main()

