liches README
==================

Getting Started
---------------

- cd <directory containing this file>

- $venv/bin/python setup.py develop

- $venv/bin/initialize_liches_db development.ini

- $venv/bin/pserve development.ini

Install
-------

    $mkdir liches
    $virtualenv --no-site-packages liches/
    $cd liches/
    $wget https://raw.github.com/cleder/liches/master/buildout.cfg
    $mkdir buildout-cache
    $mkdir buildout-cache/eggs
    $mkdir buildout-cache/downloads
    $bin/easy_install -u setuptools
    $bin/python bootstrap.py
    $bin/buildout
    $rm buildout.cfg
    $ln -s src/liches/buildout.cfg
    $ln -s src/liches/development.ini
    $bin/pserve development.ini
