# BitcoinTracker-server

A remote python uwsgi server that serves bitcoin price information.

This repo is where the server is developed. The Makefile specifies how this code is deployed remotely. Its remote layout will not match the code layout in this repo.

## Setup / Configuration

This bitcoin tracking server is meant to be deployed and run on a Whatbox seedbox. The seedbox is a shared Gentoo server on which I only have user-level (NOT admin) access.

Thankfully Whatbox has installed and provides access to an nginx utility so I can run nginx in userspace, as follows:

/usr/sbin/nginx -c <path to config> &> /dev/null

(the nginx config file is included in this repo).


uwsgi on the other hand does come pre-installed (like nginx) but it doesn't have python support compiled in to it. This means I had to roll out my own version of uwsgi in userspace. This was made remarkably easy thanks to virtualenv.

### Installing uwsgi in userspace

#### Install virtualenv

Download the latest tar-ball for virtualenv from [link](https://github.com/pypa/virtualenv/releases).

Un-tar it, cd in to the folder and then run: ``python virtualenv.py <path>`` (where <path> is the location you want to create your virtualenv).

#### Install uwsgi

cd in to the virtualenv folder.

Activiate the virtualenv by running: ``source bin/activate``

Install ``uwsgi`` using the ``pip`` script that comes with the virtualenv: ``bin/pip --install uwsgi``. (This version has python support built in).

Confirm installation by running: ``bin/uwsgi --version``.
