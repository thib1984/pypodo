## Changelog

:warning: In the case of an update from 4.x version, with this version the location of the todo file, the config file and default backup folder change! Play ``pypodo --info`` to see the new location and move you actual config file.

### 5.3.1

- [x] --info should not test pypdo file
- [x] multiline management
- [x] clean todofile with -o

### 5.3.0

- [x] fix Readme (config file)
- [x] fix autosort with delete
- [x] remove old python versions , add new versions

### 5.2.0

- [x] add --Day/--Week/--Month

### 5.1.1

- [x] --alert to --warning

### 5.1.0

- [x] add -a/--alert to display only later items
### 5.0.1

- [x] fix missing doc
### 5.0.0


- [x] improve and condensate help message
- [x] remove -u -t for --untag --tag and use -u for update
- [x] condensate mode in config file
- [x] nocolor mode in config file
- [x] move todorc file in .config/pypodo/backup
- [x] move backup file in .config/pypodo/config
- [x] move todo file in .config/pypodo/config
- [x] fix color alert
- [x] add minimal test multi os
- [x] exclude filter
### 4.1.1

- [x] Publish tweet on release 

### 4.1.0 

- [x] Reorder help message
- [x] Use columnar

### 4.0.1

- Fix readme from pypi
### 4.0.0

- [x] Add argparse
- [x] Remove crypt/uncrypt support
- [x] Remove docker support
- [x] Modify launch arguments
- [x] Move test in github action
### 3.0.3

- [x] Add new parameter formatlist for index : "1-3" for example

### 3.0.2

- [x] Optimize docker image size
- [x] Correction if incorrect path todofile
- [x] Correction if permission errors
- [x] For dev only : Clean test classe
- [x] For dev only : Add clear_workspace script
- [x] For dev only : Use of  ubuntu 20.04 for Github Actions

### 3.0.1

- [x] Improve debug messages
- [x] Correction of minor bugs in docker test
- [x] the '#' character can be place in the task if it not preceded of an empty space

### 3.0.0

- [x] Debug level
- [x] Crypt/Decrypt todofile

### 2.3.2

- [x] Code cleanup
- [x] Increased test coverage
- [x] Adding formatdate in configuration file
- [x] Documentation corrections
