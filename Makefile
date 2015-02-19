ROOT=/home/abid/www/bitcoin
DEST=sbox:$(ROOT)

.PHONY: sync

# Our goal is for sync to copy files only when they have been altered and not have to copy all files all the time since that required mutiple invocations of rsync.
# The way 'make' works this requires that the targets be NOT phony i.e. they be actual files.
# To that end create a .sync folder and the Makefile will create targets within it which will be empty files you can safely ignore.
# Every time a target is run the corresponding file is 'touch'ed which updates its timestamp and ensures that it won't run again unless its dependencies change.
#
# So when we run 'make' it is equivalent to 'make sync' since that is the first target.
# 'sync' has no commands but it does have a dependency '.sync/py'
# The target '.sync/py' in turn uses 'wildcard' to declare all .py files in the local folder as its dependencies.
# So when we run 'make sync' it moves to the '.sync/py' target and checks its dependencies. If these have changed the commands defined below are run.
# The final command that is run updates the timestamp of '.sync/py'. If this is not done we end up with the file's timestamp being unchanged and so every time we run 'make sync' the utility will think that '.sync/py' is out of date and needs to be updated.
sync: .sync/py

.sync/py: $(wildcard ./*.py)
	rsync -av --progress *.py $(DEST)/  
	@touch .sync/py
