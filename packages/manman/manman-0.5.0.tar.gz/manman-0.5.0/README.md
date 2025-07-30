# manman
GUI for deployment and monitoring of servers and applications related to specific apparatus..<br>
```
usage: python -m manman [-h] [-c CONFIGDIR] [-t INTERVAL] [-v] [apparatus ...]
positional arguments:
  apparatus             Apparatus config files, if not supplied then interactive
                        dialog will open to select files.
options:
  -c CONFIGDIR, --configDir CONFIGDIR
                        Root directory of config files.
  -t INTERVAL, --interval INTERVAL
                        Interval in seconds of periodic checking. If 0 then no
                        checking (default: 10.0)
```
The following actions are defined in combobox, related to a manager:
  - **Check**
  - **Start**
  - **Stop**
  - **Command**: will display the command for starting the manager

Definition of actions, associated with an apparatus, are defined in the 
startup dictionary of the python scripts, code-named as apparatus_NAME.py. See examples in the config directory.

Supported keys are:
  - **'cmd'**: command which will be used to start and stop the manager,
  - **'cd'**:   directory (if needed), from where to run the cmd,
  - **'process'**: used for checking/stopping the manager to identify 
     the manager's process. If cmd properly identifies the 
     manager, then this key is not necessary,
  - **'shell'**: some managers require shell=True option for subprocess.Popen()
  - **'help'**: it will be used as a tooltip,

## Demo
  python -m manman -c config apparatus_test.py apparatus_TST.py<br>
![manman](docs/manman.png)

