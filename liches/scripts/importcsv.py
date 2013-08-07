import os
import sys
import transaction
import csv

from sqlalchemy import engine_from_config



from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    CheckedLink,
    Base,
    CSV_HEADER,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [filename] \n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    if len(argv) < 3:
        fo = open('linkchecker-out.csv', 'rU')
    else:
        fo = open(argv[2], 'rU')
    reader=csv.reader(fo, delimiter=';')
    line = reader.next()
    while line[0].startswith('#'):
        line = reader.next()
    assert(line[:16] == CSV_HEADER[:16])
    with transaction.manager:
        try:
            for line in reader:
                if line[0].startswith('#'):
                    continue
                else:
                    line[10] = line[10].decode('UTF-8')
                i=0
                for l in line:
                    print i,CSV_HEADER[i],l
                    i+=1
                checked_link = CheckedLink( *line)
                DBSession.add(checked_link)
        except:
            print "Error in line: ", line
