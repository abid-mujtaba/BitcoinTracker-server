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

Install ``uwsgi`` using the ``pip`` script that comes with the virtualenv: ``bin/pip install uwsgi``. (This version has python support built in).

Confirm installation by running: ``bin/uwsgi --version``.


### Integrating uwsgi with nginx

The next hurdle was integrating our userspace uwsgi with our userspace nginx. We included ``config/bitcoin-nginx.conf`` inside our userspace ``nginx.conf`` using an ``include`` statement but it then started complaining about a missing uwsgi_params file.

Such a file may be present in ``/etc/nginx`` but I don't have even read-access to that location. So I simply searched for it online and it turns out it is a really small config file which you can just copy and paste inside the userspace nginx config folder. A copy is included in the ``config`` folder of the repo.

Now when you restart nginx it will read the additional configuration, find ``uwsgi_params`` and start correctly passing information back and forth to the uwsgi process.


### How to stop nginx and uwsgi

``killall nginx``

and

``killall -s INT uwsgi``

Uwsgi takes more effort since a simple ``killall`` results in the uwsgi processes respawning.
