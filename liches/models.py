import string
import random

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    Unicode,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    synonym,
    )

from pyramid.security import (
    Everyone,
    Authenticated,
    Allow,
    )


from zope.sqlalchemy import ZopeTransactionExtension

import cryptacular.bcrypt

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


crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
    return unicode(crypt.encode(password))


class User(Base):
    """
    Application's user model.
    """
    __tablename__ = 'users'
    username = Column(Unicode(20), primary_key=True)
    name = Column(Unicode(50))
    email = Column(Unicode(50))
    salt = Column(Unicode(40))
    _password = Column('password', Unicode(60))


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self.salt = ''.join(random.sample(
                (string.ascii_letters + string.digits) * 2,
                16))
        self._password = hash_password(self.salt + password)

    password = synonym('_password', descriptor=password)

    def __init__(self, username, password, name, email):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.get_by_username(username)
        if not user:
            return False
        return crypt.check(user.password, user.salt + password)

class LinkCheck(Base):
    __tablename__ = 'link_checks'
    check_id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    check_css = Column(Boolean)
    check_html = Column(Boolean)
    scan_virus = Column(Boolean)
    warnings = Column(Boolean)
    warning_size= Column(Integer)
    anchors = Column(Boolean)
    cookies = Column(Boolean)
    cookiefile = Column(Unicode(256))
    ignore_url = Column(Unicode(256))
    no_follow_url = Column(Unicode(256))
    timeout = Column(Integer)
    pause = Column(Integer)
    recursion_level = Column(Integer)
    url = Column(Unicode(256))
    root_url = Column(Unicode(256))

    def __init__(self,  active,  check_css, check_html, scan_virus,
                warnings, warning_size, anchors, cookies, cookiefile,
                ignore_url, no_follow_url, timeout, pause, recursion_level,
                url, root_url):
        self.active = active
        self.anchors = anchors
        self.check_css = check_css
        self.check_html = check_html
        self.cookiefile = cookiefile
        self.cookies = cookies
        self.ignore_url = ignore_url
        self.no_follow_url = no_follow_url
        self.pause = pause
        self.recursion_level = recursion_level
        self.scan_virus = scan_virus
        self.timeout = timeout
        self.url = url
        self.warning_size = warning_size
        self.warnings = warnings
        self.root_url = root_url


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit')
    ]

    __name__= ''

    def __init__(self, request):
        pass
