Introduction
==================

Liches wraps the linkchecker_ output into a web interface.
It can generate JSON_ output to integrate it into a website,
e.g: https://github.com/collective/collective.liches


Install
=======

Prerequisites
-------------

It is strongly recommended to install Liches in a virtualenv_

::

    $ mkdir liches
    $ virtualenv --no-site-packages liches/
    $ cd liches/

In this virtualenv you can install liches for production
or development.

Install for production
----------------------

In the virtualenv you created above execute these commands

::

    $ wget http://github.com/downloads/wummel/linkchecker/LinkChecker-8.4.tar.xz
    $ xz -d LinkChecker-8.4.tar.xz
    $ bin/pip install LinkChecker-8.4.tar
    $ bin/pip install liches
    $ wget https://raw.github.com/cleder/liches/master/production.ini
    $ bin/initialize_liches_db production.ini
    $ bin/pserve production.ini




Install for development
------------------------

In the virtualenv you created above execute these commands:


::

    $ wget https://raw.github.com/cleder/liches/master/buildout.cfg
    $ mkdir buildout-cache
    $ mkdir buildout-cache/eggs
    $ mkdir buildout-cache/downloads
    $ bin/easy_install -u setuptools
    $ wget http://python-distribute.org/bootstrap.py
    $ bin/python bootstrap.py
    $ bin/buildout
    $ rm buildout.cfg
    $ ln -s src/liches/buildout.cfg
    $ ln -s src/liches/development.ini
    $ bin/initialize_liches_db development.ini
    $ bin/pserve development.ini


Getting Started
===============

Check a site for bad links with e.g:

::

    $ bin/linkchecker --file-output=csv --pause=3 --no-warnings http://localhost/index.html

Please refer to the linkchecker_ manual for usage.

Import the output produced by linkchecker_ into liches

::

    $ bin/import_liches_csv production.ini


Open `http://localhost:6543/` in your browser to see the results. The
frontpage tells you how many pages with broken urls are in your site.
Click on the link *'You have XYZ pages with broken links'* to view the
pages at `http://localhost:6543/getpages`.

At `http://localhost:6543/getpages?format=json` you can access the data
in JSON_ format.

The links will take you to a page with detailed results for this page e.g.
`http://localhost:6543/checkurl?url=http://localhost/index.html`
which can also be accessed as JSON_
`http://localhost:6543/checkurl?url=http://localhost/index.html&format=json`


.. _linkchecker: http://wummel.github.io/linkchecker/
.. _virtualenv: http://www.virtualenv.org/
.. _JSON: http://www.json.org/
