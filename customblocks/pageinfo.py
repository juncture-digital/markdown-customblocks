from yamlns import namespace as ns
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunsplit

class PageInfo:

    def __init__(self, html, url=None):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')
        self._url = urlparse(url)
        self._fullurl = url

    def _tag(self, name):
        tag = self._soup.find(name)
        if tag: return tag.text

    def _meta(self, name):
        meta = self._soup.find('meta', property=name)
        if meta: return meta.get('content')

    def _rel(self, name):
        rel = self._soup.find('link', rel=name)
        if not rel: return
        return rel.get('href')

    @property
    def sitename(self):
        return self._meta('og:site_name') or self._url.hostname

    @property
    def siteurl(self):
        return urlunsplit((self._url.scheme, self._url.netloc,'','','')) or None

    @property
    def siteicon(self):
        icon = self._rel('icon') or '/favicon.ico' 
        if self._fullurl:
            return urljoin(self._fullurl, icon)
        return icon

    @property
    def title(self):
        return (
            self._meta('og:title') or
            self._tag('title') or
            self.sitename
        )

    @property
    def description(self):
        return (
            self._meta('og:description') or
            self._meta('twitter:description') or
            self._meta('description') or
            ''
        )



# vim: et ts=4 sw=4
