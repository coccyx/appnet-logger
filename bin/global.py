import sys
sys.path.append('lib')

from config import Config
import logging, logging.handlers
import json
import urllib2, urllib
import time

c = Config()
logger = logging.getLogger('appnet')

out = logging.getLogger('appnet_global')
formatter = logging.Formatter('%(message)s')
handler = logging.handlers.RotatingFileHandler(filename=c.file_name, maxBytes=c.max_bytes,
                                                backupCount=c.backup_files)
handler.setFormatter(formatter)
out.addHandler(handler)
out.setLevel(logging.DEBUG)
logger.debug("Configured to log to '%s' with maxBytes '%s' with backupCount '%s'" % \
                (c.file_name, c.max_bytes, c.backup_files))


while True:
    url = c.global_stream_url
    query_string = { 'min_id': c.min_id }
    url = url + '?' + urllib.urlencode(query_string)
    headers = { 'Authorization': 'Bearer '+c.access_token }
    req = urllib2.Request(url, None, headers)
    gotresults = False
    while not gotresults:
        try:
            response = urllib2.urlopen(req)
            page = response.read()
            results = json.loads(page)
            gotresults = True
        except urllib2.HTTPError:
            pass

    i = 0
    for item in results:
        # logger.debug('Item ID: %s Min ID: %s' % (item['id'], c.min_id))
        if long(item['id']) > long(c.min_id):
            i += 1
            out.debug(json.dumps(item))

    logger.debug("Retrieved %s results from app.net.  Last ID: %s.  Wrote %s results." 
                % (len(results), results[0]['id'], i))

    # If we pass a greater min ID to App.Net than exists, it'll give us back the last 20 results
    # better to send it the current max id and always ignore it
    if long(results[0]['id']) > long(c.min_id):
        c.set_min_id(long(results[0]['id']))

    time.sleep(c.sleep_time)
