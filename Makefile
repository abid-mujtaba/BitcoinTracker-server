.PHONY: sync

sync:
	rsync -av --progress *.py sbox:/home/abid/www/bitcoin/
	rsync -av --progress uwsgi/*.py sbox:/home/abid/www/bitcoin/uwsgi/
	rsync -av --progress config/* sbox:/home/abid/www/bitcoin/config/
	rsync -av --progress templates/* sbox:/home/abid/www/bitcoin/uwsgi/templates/
