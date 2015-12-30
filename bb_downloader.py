import os
import logging

import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from util import bb_auth
from util import config

# For testing purposes/private use, declare username and password here
# un = 'n#######'
# pw = 'password'


ignore_list = ['https://blackboard.qut.edu.au',
               'https://www.qut.edu.au',
               'http://www.qut.edu.au',
               'https://www.student.qut.edu.au',
               'http://www.student.qut.edu.au',
               'https://qutvirtual4.qut.edu.au/group/staff/home',
               'http://www.library.qut.edu.au/services/jsp'
               'https://www.library.qut.edu.au/services/jsp'
               'https://blackboard.qut.edu.au/webapps/login/?action=logout',
               'https://qutvirtual3.qut.edu.au/qv/sp_maint_p.show_menu',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_3_1',
               '/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_3_1',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_4_1',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_5_1',
               'https://blackboard.qut.edu.au/webapps/login',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_242_1'
               ]


class WebPage():
    def __init__(self,
                 url,
                 text,
                 unit,
                 session,
                 parent=None,
                 depth=0):

        # append correct schema to url if missing
        if url[0] != 'h':
            self.url = 'https://blackboard.qut.edu.au' + url
        else:
            self.url = url

        self.text = text
        self.unit = unit
        self.session = session
        self.depth = depth
        self.downloaded = False
        self.to_download = False
        self.crawled = False
        self.parent = parent
        self.children = []

        self.crawl()

        return

    def crawl(self):
        if self.depth > 4:
            logging.info('Reached crawl depth of 5. No longer crawling %s' %
                         self.text)
            return

        # Crawl blackboard page for links. Add files to to_download and make a
        # new object for other redirects
        header = self.session.head(self.url).headers
        if self.is_file(header):
            self.add_to_download_list()
        else:
            soup = bs(self.session.get(self.url).content, 'lxml')
            body = soup.find(class_='contentBox')
            if body is None:
                return
            try:
                for link in body.find_all('a'):
                    if link in ignore_list:
                        continue
                    elif link.text.lower() == 'stimulate':
                        continue
                    elif link.text.lower() == 'course materials':
                        continue
                    self.children.append(WebPage(link.get('href'), link.text,
                                     self.unit, self.session,
                                     depth=(self.depth + 1),
                                     parent=self))
            except AttributeError:
                logging.INFO(self.url + ' : ' + header['Content-Type'] + ' : ' + body)
                return
        return

    def is_downloaded(self):
        # Test to see if file has already been downloaded
        return True

    def is_file(self, header):
        """ confirms that url is a file, not a link """
        try:
            return header['Content-Type'].split(';')[0] != 'text/html'
        except KeyError:
            return False

    def add_to_download_list(self):
        """ adds file to the unit's download queue """
        self.unit['to_download'].append(self.url)
        self.to_download = True
        return


def download_file(unitcode, url, session):
    tmp = os.path.join(unitcode, 'partdownload')
    os.makedirs(unitcode, exist_ok=True)
    name = clean_url(session.head(url, allow_redirects=True).
                     url.split('/')[-1])

    print('Downloading %s to %s' % (name, file_))
    with open(tmp, 'wb') as f:
        for block in tqdm(session.get(url).iter_content(2042)):
            f.write(block)
    file_ = os.path.join(unitcode, name)
    os.rename(tmp, file_)

    return


def clean_url(url):
    url = url.replace('%20', '_')
    url = url.replace('%28', '(')
    url = url.replace('%29', ')')
    url = url.replace('%26', '&')
    url = url.replace('%40', '@')
    url = url.replace('%27', "'")

    return url


def main():
    """docstring for main"""
    logging.basicConfig(level=logging.WARN)
    # Uncomment these two lines if declaring username and password globally
    un = input('Enter your username: ')
    pw = input('Enter your password:')

    # Parse config.xml to retrieve user's units
    logging.info('Parsing configuration.')
    units = config.parse_config()

    logging.info('Authenticating session.')
    s = requests.Session()
    s = bb_auth.authenticate(un, pw, s)
    logging.info('Successfully authenticated')

    unit_pages = []

    for unit in units:
        unit['to_download'] = []
        unit_pages.append(WebPage(unit['url'], unit['unitcode'], unit, s))

    for unit in units:
        for url in unit['to_download']:
            download_file(unit['unitcode'], url, s)


if __name__ == '__main__':
    main()
