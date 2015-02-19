ROOT=/home/abid/www/bitcoin

.PHONY: sync

sync:
	rsync -av --progress *.py sbox:${ROOT}/
	rsync -av --progress uwsgi/*.py sbox:${ROOT}/uwsgi/
	rsync -av --progress config/* sbox:${ROOT}/config/
	rsync -av --progress templates/* sbox:${ROOT}/uwsgi/templates/
	rsync -av -r --progress static/* sbox:${ROOT}/static/

	ssh sbox "touch ${ROOT}/uwsgi/app.py"
