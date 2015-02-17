.PHONY: sync

sync:
	rsync -av --progress *.py sbox:/home/abid/www/bitcoin/
