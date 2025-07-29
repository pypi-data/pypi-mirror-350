'''Definition of the second test apparatus.
'''
import os
homeDir = os.environ['HOME']

__version__ = 'v0.0.1 2025-05-21'#

# abbreviations:
help,cmd,process,cd = ['help','cmd','process','cd']

startup = {
#       Operational managers
'xclock':{help:'Digital xclock', 
  cmd:'xclock -digital'
  },
'htop':{help:'Process viewer in separate xterm',
  cmd:'xterm htop',
  },
'sleep30':{help:'Sleep for 30 seconds', 
  cmd:'sleep 30', process:'sleep 30'
  },
}
