from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    Unicode,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


CSV_HEADER =['urlname', 'parentname', 'baseref', 'result', 'warningstring',
    'infostring', 'valid', 'url', 'line', 'column', 'name', 'dltime',
    'dlsize', 'checktime', 'cached', 'level', 'modified']

class CheckedLink(Base):
    __tablename__ = 'checked_links'
    urlid = Column(Integer, primary_key=True)
    urlname = Column(Unicode(512), nullable=False) #varchar(256) not null,
    parentname = Column(Unicode(512))               #varchar(256),
    baseref = Column(Unicode(80))                   #varchar(256),
    result = Column(Unicode(256))                   #varchar(256),
    warning = Column(Unicode(512))                  #varchar(512),
    info = Column(Unicode(512))                     #varchar(512),
    valid = Column(Unicode(80))                     #int,
    url = Column(Unicode(512))                      #varchar(256),
    line = Column(Integer)                          #int,
    col = Column(Integer)                           #int,
    name = Column(Unicode(256))                     #varchar(256),
    dltime = Column(Float)                        #int,
    dlsize = Column(Integer)                        #int,
    checktime = Column(Float)                     #int,
    cached = Column(Integer)                        #int,
    level = Column(Integer, nullable=False)        #int not null,
    modified = Column(Unicode(256))                 #varchar(256)

    def __init__(self, urlname, parentname, baseref,  result,
                warning, info, valid, url, line, col, name, dltime,
                dlsize, checktime, cached, level, modified=None):
        self.urlname = urlname
        self.parentname = parentname
        self.baseref = baseref
        self.valid = valid
        self.result = result
        self.warning = warning
        self.info = info
        self.url = url
        self.line = line
        self.col = col
        self.name = name
        self.checktime = checktime
        self.dltime = dltime
        self.dlsize = dlsize
        self.cached = cached
        self.level = level
        self.modified = modified

