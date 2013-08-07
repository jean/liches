import string
import random
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    RootFactory,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    secret = ''.join(random.sample(string.ascii_letters + string.digits,
                16))
    session_factory = UnencryptedCookieSessionFactoryConfig(secret)
    authn_policy = SessionAuthenticationPolicy()
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        root_factory=RootFactory,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        session_factory=session_factory
        )
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('parenturl', '/checkurl')
    config.add_route('checkpages', '/getpages')
    config.add_route('linkcheck', '/linkcheckurl')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('preferences', '/preferences')
    config.add_route('linkchecks', '/linkcheck')
    config.add_route('addlinkcheck', '/linkcheck/add')
    config.add_route('editlinkcheck', '/linkcheck/{check_id}')
    config.scan()
    return config.make_wsgi_app()
