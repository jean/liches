import hashlib
import urlparse
import re
from subprocess import Popen
import sys
import time
try:
    import simplejson as json
except ImportError:
    import json

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.url import resource_url

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    CheckedLink,
    User,
    LinkCheck,
    )

from pyramid.security import (
    authenticated_userid,
    remember,
    forget,
    )

from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    )

import formencode

from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from .utils import invalid_url, API_KEY, linkchecker_options

class SecurePassword(formencode.validators.FancyValidator):

     min = 6
     non_letter = 2
     letter_regex = re.compile(r'[a-zA-Z]')

     messages = {
         'too_few': 'Your password must be longer than %(min)i '
                   'characters long',
         'non_letter': 'You must include at least %(non_letter)i '
                      'characters in your password',
         }

     def _convert_to_python(self, value, state):
         # _convert_to_python gets run before _validate_python.
         # Here we strip whitespace off the password, because leading
         # and trailing whitespace in a password is too elite.
         return value.strip()

     def _validate_python(self, value, state):
         if len(value) < self.min:
             raise Invalid(self.message("too_few", state,
                                        min=self.min),
                           value, state)
         non_letters = self.letter_regex.sub('', value)
         if len(non_letters) < self.non_letter:
             raise Invalid(self.message("non_letter",
                                         non_letter=self.non_letter),
                           value, state)




@view_config(route_name='home', renderer='templates/home.pt', permission='view')
def my_view(request):
    try:
        result = DBSession.query(CheckedLink.parentname).distinct().count()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    logged_in = authenticated_userid(request)
    return {'result': result, 'project': 'liches', 'loggedin': logged_in}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_liches_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='parenturl', renderer='templates/parenturl.pt', permission='view')
def parenturl_view(request):
    parenturl = request.params.get('url')
    error = invalid_url(parenturl)
    if error:
        return Response(error, content_type='text/plain', status_int=500)
    urlobj = urlparse.urlparse(parenturl)
    pagename = urlparse.urlunparse([urlobj.scheme, urlobj.netloc, urlobj.path, None, None, None])
    try:
        results = DBSession.query(CheckedLink).filter_by(parentname=parenturl).distinct().all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    if results is None:
        res = {'num': 0, 'urls': [], 'name': pagename}
    else:
        urls = []
        for url in results:
            urls.append({
                'urlname': url.urlname,
                'parentname': url.parentname,
                'baseref': url.baseref,
                'valid': url.valid,
                'result': url.result,
                'warning': url.warning,
                'info': url.info,
                'url': url.url,
                'line': url.line,
                'col': url.col,
                'name': url.name,
                'checktime': url.checktime,
                'dltime': url.dltime,
                'dlsize': url.dlsize,
                'cached': url.cached,
                'level': url.level,
                'modified': url.modified,})
        res = {'num': len(results), 'urls': urls, 'name':pagename}
    if request.params.get('format') == 'json':
        response =  Response(json.dumps(res))
        response.content_type='application/json'
        return response
    else:
        return res


@view_config(route_name='checkpages', renderer='templates/pages.pt', permission='view')
def checked_pages_view(request):
    parenturl = request.params.get('url')
    code = request.params.get('code')
    try:
        filter = []
        if parenturl:
            filter.append(CheckedLink.parentname.like(parenturl +'%'))
        if code:
            filter.append(CheckedLink.result == code)
        if filter:
            results = DBSession.query(CheckedLink.parentname
                ).filter( *filter
                ).distinct().all()
        else:
            results = DBSession.query(CheckedLink.parentname).distinct().all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    codes = DBSession.query(CheckedLink.result).distinct().all()
    if results is None:
        res = {'num': 0, 'urls': [], 'name': pagename, 'codes': codes, 'code': code}
    else:
        urls = []
        for url in results:
            urls.append([url[0],
            resource_url(request.context, request, 'checkurl', query={'url': url[0]})])
        res = {'num': len(results), 'urls': urls, 'name':parenturl, 'codes': codes, 'code':code}
    if request.params.get('format') == 'json':
        response =  Response(json.dumps(res))
        response.content_type='application/json'
        return response
    else:
        return res

@view_config(route_name='linkcheck', renderer='templates/checklink.pt', permission='view')
def check_url(request):
    url = request.params.get('url')
    key = request.params.get('key')
    error = invalid_url(url)
    if error:
        return Response(error, content_type='text/plain', status_int=500)
    t = int(time.time()/100)
    valid = False
    for i in range(-1,2):
        if hashlib.md5(str(t+i) +API_KEY + url).hexdigest() == key:
            valid = True
            break
    if valid:
        process = Popen(['bin/checkpage', sys.argv[1], url])
        result = {'status': 'linkcheck initialized', 'name': url}
    else:
        return Response('illegal or missing key', content_type='text/plain', status_int=403)
    if request.params.get('format') == 'json':
        response =  Response(json.dumps(result))
        response.content_type='application/json'
        return response
    else:
        return result


@view_config(permission='view', route_name='login')
def login_view(request):
    main_view = request.route_url('home')
    came_from = request.params.get('came_from', main_view)

    post_data = request.POST
    if 'submit' in post_data:
        login = post_data['login']
        password = post_data['password']

        if User.check_password(login, password):
            headers = remember(request, login)
            request.session.flash(u'Logged in successfully.')
            return HTTPFound(location=came_from, headers=headers)

    request.session.flash(u'Failed to login.')
    return HTTPFound(location=came_from)

@view_config(permission='edit', route_name='logout')
def logout_view(request):
    request.session.invalidate()
    request.session.flash(u'Logged out successfully.')
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)



class RegistrationSchema(formencode.Schema):
    allow_extra_fields = True
    username = formencode.validators.PlainText(not_empty=True)
    #password = formencode.validators.PlainText(not_empty=True)
    email = formencode.validators.Email(resolve_domain=False)
    name = formencode.validators.String(not_empty=True)
    password = SecurePassword()
    confirm_password = formencode.validators.String(not_empty=True)
    chained_validators = [
        formencode.validators.FieldsMatch('password', 'confirm_password')
    ]


@view_config(permission='edit', route_name='register',
             renderer='templates/user_add.pt')
def user_add(request):
    form = Form(request, schema=RegistrationSchema)
    redirect_url = request.route_url('home')
    if 'form.submitted' in request.POST and form.validate():
        session = DBSession()
        username = form.data['username']
        user = User(
            username=username,
            password=form.data['password'],
            name=form.data['name'],
            email=form.data['email']
        )
        session.add(user)
        headers = remember(request, username)
        return HTTPFound(location=redirect_url, headers=headers)
    elif 'form.canceled' in request.POST:
        return HTTPFound(location=redirect_url)
    return {
        'form': FormRenderer(form),
    }

class UserPreferencesSchema(formencode.Schema):
    allow_extra_fields = True
    old_password = formencode.validators.PlainText()
    email = formencode.validators.Email(resolve_domain=False)
    name = formencode.validators.String(not_empty=True)
    new_password = SecurePassword()
    confirm_password = formencode.validators.String()
    chained_validators = [
        formencode.validators.FieldsMatch('new_password', 'confirm_password')
    ]

@view_config(permission='edit', route_name='preferences',
             renderer='templates/user_edit.pt')
def user_preferences(request):
    logged_in = authenticated_userid(request)
    redirect_url = request.route_url('home')
    try:
        user = DBSession.query(User).filter_by(username=logged_in).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    form = Form(request, schema=UserPreferencesSchema)
    if 'form.submitted' in request.POST and form.validate():
        if form.data.get('new_password'):
            if User.check_password(logged_in, form.data['old_password']):
                user.password = form.data['new_password']
        user.email = form.data.get('email')
        user.name = form.data.get('name')
        DBSession.add(user)
        return HTTPFound(location=redirect_url)
    elif 'form.canceled' in request.POST:
        return HTTPFound(location=redirect_url)
    else:
        return {'user': user, 'form': FormRenderer(form)}


class LinkCheckSchema(formencode.Schema):
    allow_extra_fields = True
    url = formencode.validators.URL(not_empty=True)
    root_url = formencode.validators.URL(not_empty=True)
    recursion_level = formencode.validators.Int()
    active = formencode.validators.Bool()
    check_css = formencode.validators.Bool()
    check_html = formencode.validators.Bool()
    scan_virus = formencode.validators.Bool()
    warnings = formencode.validators.Bool()
    anchors = formencode.validators.Bool()
    cookies = formencode.validators.Bool()
    timeout = formencode.validators.Int()
    pause = formencode.validators.Int()

@view_config(permission='edit', route_name='addlinkcheck',
             renderer='templates/linkcheck_add.pt')
def linkcheck_add(request):
    form = Form(request, schema=LinkCheckSchema)
    redirect_url = request.route_url('linkchecks')
    if 'form.submitted' in request.POST and form.validate():
        session = DBSession()
        url = form.data['url']
        linkcheck = LinkCheck(
            url=url,
            root_url=form.data['root_url'],
            recursion_level=form.data.get('recursion_level'),
            active=form.data.get('active'),
            check_css=form.data.get('check_css'),
            check_html=form.data.get('check_html'),
            scan_virus=form.data.get('scan_virus'),
            warnings=form.data.get('warnings'),
            warning_size=form.data.get('warning_size'),
            anchors=form.data.get('anchors'),
            cookies=form.data.get('coockies'),
            cookiefile=form.data.get('cookiefile'),
            ignore_url=form.data.get('ignore_url'),
            no_follow_url=form.data.get('no_follow_url'),
            timeout=form.data.get('timeout'),
            pause=form.data.get('pause'),
        )
        session.add(linkcheck)
        return HTTPFound(location=redirect_url)
    elif 'form.canceled' in request.POST:
        return HTTPFound(location=redirect_url)
    return {
        'form': FormRenderer(form),
    }

@view_config(permission='edit', route_name='editlinkcheck',
             renderer='templates/linkcheck_edit.pt')
def linkcheck_edit(request):
    check_id = request.matchdict['check_id']
    page = DBSession.query(LinkCheck).filter_by(check_id=check_id).first()
    if page is None:
        return HTTPNotFound('No such page')

    form = Form(request, schema=LinkCheckSchema)
    redirect_url = request.route_url('linkchecks')
    if 'form.submitted' in request.POST and form.validate():
        page.url=form.data['url']
        page.root_url=form.data['root_url']
        page.recursion_level=form.data.get('recursion_level')
        page.active=form.data.get('active')
        page.check_css=form.data.get('check_css')
        page.check_html=form.data.get('check_html')
        page.scan_virus=form.data.get('scan_virus')
        page.warnings=form.data.get('warnings')
        page.warning_size=form.data.get('warning_size')
        page.anchors=form.data.get('anchors')
        page.cookies=form.data.get('coockies')
        page.cookiefile=form.data.get('cookiefile')
        page.ignore_url=form.data.get('ignore_url')
        page.no_follow_url=form.data.get('no_follow_url')
        page.timeout=form.data.get('timeout')
        page.pause=form.data.get('pause')
        return HTTPFound(location=redirect_url)
    elif 'form.canceled' in request.POST:
        return HTTPFound(location=redirect_url)
    elif 'form.deleted' in request.POST:
        DBSession.delete(page)
        return HTTPFound(location=redirect_url)
    else:
        return {
            'form': FormRenderer(form), 'data': page,
        }



@view_config(permission='edit', route_name='linkchecks',
             renderer='templates/linkchecks.pt')
def linkchecks_view(request):
    try:
        results = DBSession.query(LinkCheck).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    if results is None:
        res = {'urls': []}
    else:
        urls = []
        for linkcheck in results:
            if linkcheck.active:
                start_url = linkcheck.url
            else:
                start_url = 'inactive'
            urls.append({
                'name': linkcheck.root_url,
                'start': start_url,
                'options': ' '.join(linkchecker_options(linkcheck)),
                'url': request.route_url('editlinkcheck', check_id=linkcheck.check_id),
                })
        res ={'urls': urls}
    if request.params.get('format') == 'json':
        response =  Response(json.dumps(res))
        response.content_type='application/json'
        return response
    else:
        return res
