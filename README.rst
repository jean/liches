Introduction
==================

Liches wraps the linkchecker_ output into a web interface.
You can run Liches as a stand-alone service for use with your websites
regardless of the language they're written in. While Liches itself is
written in Python, it interacts with your website purely via HTTP and
JSON_. You can even integrate it with pure javascript without the need of
server side programming or use it as a stand alone service.
An example how to integrate it into a website can be found at
https://github.com/collective/collective.liches

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
    Username [admin]:
    Password [generate]:
    ('password generated: ', 'whmgfi6r')
    Fullname: Administrator
    Email: root@localhost
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
    Username [admin]:
    Password [generate]:
    ('password generated: ', 'whmgfi6r')
    Fullname: Administrator
    Email: root@localhost
    $ bin/pserve development.ini

Configuration
--------------

You configure you liches server in you production.ini or development.ini
file.

Database
+++++++++

In the `[app:main]` section of you configuration file change the sqlalchemy.url_
to point to your database (or leave it like it is if you want to use sqllite)

.. _sqlalchemy.url: http://docs.sqlalchemy.org/en/rel_0_8/core/engines.html#database-urls

API Key
++++++++

To enable a website to request a linkcheck of a particular page you have
to provide an `api_key` in the `[liches]` section of your ini file. If this
parameter is not set liches will generate a random key every time it is
started. The generated key will be displayed during startup.

::

    2013-08-05 17:16:01,085 WARNI [liches.utils][MainThread] API Key: w4NhYBHSVGzfmpiK

As the generated key is reasonably unique and complicated you may copy
it into your ini file.

Getting Started
===============

Define your linkchecks in the web GUI or alternatively import linkchecks
from the commandline.

Web GUI
--------

Open your Liches server in your webbrowser.

.. image:: https://raw.github.com/cleder/liches/master/docs/liches-home-loggedout.png

Log into your liches server.

.. image:: https://raw.github.com/cleder/liches/master/docs/liches-home-loggedin.png

Goto linkchecks.

.. image:: https://raw.github.com/cleder/liches/master/docs/liches-linkchecks.png

and add a new linkcheck.

.. image:: https://raw.github.com/cleder/liches/master/docs/liches-add-linkcheck.png

On the commandline you can then call:

::

    $ bin/liches_linkchecker development.ini

This command will call linkchecker_ for all the checks you have enabled
and import the results into the database. For regular linkchecks you can
call this command as a cron job.

Manual Import
--------------
Check a site for bad links with e.g:

::

    $ bin/linkchecker --file-output=csv --pause=3 --no-warnings http://localhost/index.html

Please refer to the linkchecker_ manual for usage.

Import the output produced by linkchecker_ into liches

::

    $ bin/import_liches_csv production.ini

View the results
-----------------

Open `http://localhost:6543/` in your browser to see the results. The
frontpage tells you how many pages with broken urls are in your site.
Click on the link *'You have XYZ pages with broken links'* to view the
pages at `http://localhost:6543/getpages`.

At `http://localhost:6543/getpages?format=json` you can access the data
in JSON_ format.

.. image:: https://raw.github.com/cleder/liches/master/docs/liches-brokenpages.png

The links will take you to a page with detailed results for this page e.g.
`http://localhost:6543/checkurl?url=http://localhost/index.html`
which can also be accessed as JSON_
`http://localhost:6543/checkurl?url=http://localhost/index.html&format=json`

.. image:: https://raw.github.com/cleder/liches/master/docs/liches-brokenlinks.png

.. _linkchecker: http://wummel.github.io/linkchecker/
.. _virtualenv: http://www.virtualenv.org/
.. _JSON: http://www.json.org/
