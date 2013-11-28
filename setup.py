import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'linkchecker',
    'cryptacular',
    'pyramid_simpleform',
    ]

setup(name='liches',
      version='0.5',
      description='Liches a server for linkchecker results',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        ],
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='https://github.com/cleder/liches',
      keywords='web wsgi bfg pylons pyramid linkchecker',
      license='GPL',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='liches',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = liches:main
      [console_scripts]
      initialize_liches_db = liches.scripts.initializedb:main
      import_liches_csv = liches.scripts.importcsv:main
      empty_link_table = liches.scripts.emptydb:main
      checkpage = liches.scripts.checkpage:main
      liches_linkchecker = liches.scripts.checklinks:main
      """,
      )
