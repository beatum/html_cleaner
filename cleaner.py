#!usr/bin/python

"""
Created on 30.03.17.
(c) Ivan Semernyakov <direct@beatum-group.ru>
"""

import sys
import urllib
from lxml.html.clean import Cleaner
from lxml.html import fromstring
from lxml.html import tostring
from lxml.html import HTMLParser

cleaner = Cleaner(style=True, page_structure=False)

"""
The 'cleaner' can accept
the following parameters:

scripts = True
javascript = True
comments = True
style = False
links = True
meta = True
page_structure = True
processing_instructions = True
embedded = True
frames = True
forms = True
annoying_tags = True
remove_tags = None
allow_tags = None
kill_tags = None
remove_unknown_tags = True
safe_attrs_only = True
safe_attrs = defs.safe_attrs
add_nofollow = False
host_whitelist = ()
whitelist_tags = set(['iframe', 'embed'])
"""

whitespacer = HTMLParser(encoding='utf-8', remove_blank_text=True)


def app(env, start_response):
    """
    App - function for parsing and cleaning html content,
    accept one system argument: http or https url.
    :param env: default system environment
    :param start_response: status, headers
    :return: html_content with clean data (without attribute style)
    """

    url = '%s' % sys.argv[1]
    response = urllib.urlopen(url)
    html_content = cleaner.clean_html(response.read())
    from_string = fromstring(html_content, parser=whitespacer)
    html_results = tostring(from_string, pretty_print=True)
    start_response("200 OK", [('Content-Type', 'text/html;charset=utf-8')])
    return [html_results]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Run this script like this: python clean.py http://example.com")
        sys.exit(2)
    try:
        from wsgiref.simple_server import make_server
        httpd = make_server('', 8000, app)
        soc = httpd.socket.getsockname()
        print('Serving HTTP on %s:%s' % (soc[0], soc[1]))
        import webbrowser
        webbrowser.open('http://localhost:8000/')
        httpd.handle_request()  # serve one request, then exit
    except KeyboardInterrupt:
        print('Goodbye!')
        httpd.server_close()
