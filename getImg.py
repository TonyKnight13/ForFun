# -- coding: UTF-8 --
import ssl
import urllib

ssl._create_default_https_context = ssl._create_unverified_context

def getHtml(url):
    page = urllib.request.urlopen(url)
    html=page.read()
    html=html.decode('utf-8')
    return html

