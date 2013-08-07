import sys
import ConfigParser
import urlparse
import string
import random
import logging

logger = logging.getLogger(__name__)

config = ConfigParser.SafeConfigParser()
config.read(sys.argv[1])
try:
    API_KEY = config.get('liches','api_key')
except:
    API_KEY = None
if not API_KEY:
    API_KEY = ''.join(random.sample(string.ascii_letters + string.digits,
                16))
    logger.warn('API Key: %s' % API_KEY)


def invalid_url(url):
    if not url:
        return 'Required parameter url is missing'
    urlobj = urlparse.urlparse(url)
    if urlobj.scheme not in ['http', 'https']:
        return 'url must start with http:// or https://'
    if not urlobj.hostname:
        return 'Required hostname is missing'
    return False

def linkchecker_options(linkcheck):
    options = []
    if not linkcheck.active:
        return options
    else:
        options.append('bin/linkchecker')
    if linkcheck.anchors:
        options.append('--anchors')
    if linkcheck.check_css:
        options.append('--check-css')
    if linkcheck.check_html:
        options.append('--check-html')
    if linkcheck.cookies:
        options.append(' --cookies')
    if linkcheck.scan_virus:
        options.append('--scan-virus')
    if not linkcheck.warnings:
        options.append('--no-warnings')
    if linkcheck.ignore_url:
        for line in linkcheck.ignore_url.splitlines():
            options.append('--ignore-url=%s' % line )
    if linkcheck.no_follow_url:
        for line in linkcheck.no_follow_url.splitlines():
            options.append('--no-follow-url=%s' % line )
    if linkcheck.recursion_level:
        options.append('--recursion-level=%i' % linkcheck.recursion_level)
    if linkcheck.pause:
        options.append('--pause=%i' % linkcheck.pause)
    if linkcheck.warning_size:
        options.append('--warning-size-bytes=%i' % linkcheck.warning_size)
    if linkcheck.timeout:
        options.append('--timeout=%i' % linkcheck.timeout)
    return options


