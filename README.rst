Liches README
==================

Liches wraps the linkchecker_ output into a web interface.
It can generate JSON ouput to integrate it into a website,
e.g: https://github.com/collective/collective.liches




Getting Started
---------------

TBD

Install
=======

Install for Production
----------------------

TBD

Install for development
------------------------

::

    $mkdir liches
    $virtualenv --no-site-packages liches/
    $cd liches/
    $wget https://raw.github.com/cleder/liches/master/buildout.cfg
    $mkdir buildout-cache
    $mkdir buildout-cache/eggs
    $mkdir buildout-cache/downloads
    $bin/easy_install -u setuptools
    $wget http://python-distribute.org/bootstrap.py
    $bin/python bootstrap.py
    $bin/buildout
    $rm buildout.cfg
    $ln -s src/liches/buildout.cfg
    $ln -s src/liches/development.ini
    $bin/initialize_liches_db development.ini
    $bin/pserve development.ini


.. _linkchecker: http://wummel.github.io/linkchecker/
