import sys
import ConfigParser
import urlparse
import string
import random

config = ConfigParser.SafeConfigParser()
config.read(sys.argv[1])
try:
    API_KEY = config.get('liches','api_key')
except:
    API_KEY = None
if not API_KEY:
    API_KEY = ''.join(random.sample(string.ascii_letters + string.digits,
                16))



def invalid_url(url):
    if not url:
        return 'Required parameter url is missing'
    urlobj = urlparse.urlparse(url)
    if urlobj.scheme not in ['http', 'https']:
        return 'url must start with http:// or https://'
    if not urlobj.hostname:
        return 'Required hostname is missing'
    return False
