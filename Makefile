.PHONY: sync

sync:
	rsync -av --progress *.py sbox:/home/abid/www/bitcoin/
	rsync -av --progress uwsgi/*.py sbox:/home/abid/www/bitcoin/uwsgi/
