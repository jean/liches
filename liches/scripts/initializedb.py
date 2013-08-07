import os
import sys
import transaction
import string
import random

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    CheckedLink,
    Base,
    User,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        un = raw_input('Username [admin]: ')
        if not un:
            un = 'admin'
        pw = raw_input('Password [generate]: ')
        if not pw:
            pw = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            print( 'password generated: ', pw)
        fn = raw_input('Fullname: ')
        em = raw_input('Email: ')
        user = User(un, pw, fn, em)
        DBSession.add(user)

