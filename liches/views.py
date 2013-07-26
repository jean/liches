import urlparse
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    CheckedLink,
    )


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one') #.first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'liches'}

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


@view_config(route_name='parenturl', renderer='templates/parenturl.pt')
def parenturl_view(request):
    parenturl = request.params.get('url')
    if not parenturl:
        return Response('Required parameter url is missing', content_type='text/plain', status_int=500)
    urlobj = urlparse.urlparse(parenturl)
    if urlobj.scheme not in ['http', 'https']:
        return Response('url must start with http:// or https://', content_type='text/plain', status_int=500)
    if not urlobj.hostname:
        return Response('Required hostname is missing', content_type='text/plain', status_int=500)
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
    return res



