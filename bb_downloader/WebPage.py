import os
import logging

from bs4 import BeautifulSoup as bs

from bb_downloader.utils import clean_url

IGNORE_LIST = ['https://blackboard.qut.edu.au',
               'https://www.qut.edu.au',
               'http://www.qut.edu.au',
               'https://www.student.qut.edu.au',
               'http://www.student.qut.edu.au',
               'https://qutvirtual4.qut.edu.au/group/staff/home',
               'http://www.library.qut.edu.au/services/jsp'
               'https://www.library.qut.edu.au/services/jsp'
               'https://blackboard.qut.edu.au/webapps/login/?action=logout',
               'https://qutvirtual3.qut.edu.au/qv/sp_maint_p.show_menu',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/'
               'tabAction?tab_tab_group_id=_3_1',
               '/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_3_1',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/'
               'tabAction?tab_tab_group_id=_4_1',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/'
               'tabAction?tab_tab_group_id=_5_1',
               'https://blackboard.qut.edu.au/webapps/login',
               'https://blackboard.qut.edu.au/webapps/portal/execute/tabs/'
               'tabAction?tab_tab_group_id=_242_1'
               ]


class WebPage():
    def __init__(self,
                 url,
                 text,
                 unit,
                 category,
                 session,
                 parent=None,
                 depth=0):

        # append correct schema to url if missing
        if not url.startswith('https'):
            self.url = 'https://blackboard.qut.edu.au' + url
        else:
            self.url = url

        self.text = text
        self.unit = unit
        self.category = category
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

        if self.crawled:
            return

        # Crawl blackboard page for links. Add files to to_download and make a
        # new object for other redirects
        header = self.session.head(self.url).headers
        if self.is_file(header):
            if self.category is 'assessment':
                self.unit.assessment.append(self)
            else:
                self.unit.resources.append(self)
        else:
            soup = bs(self.session.get(self.url).content, 'lxml')
            body = soup.find(class_='contentBox')
            if body is None:
                return
            try:
                for link in body.find_all('a'):
                    if link in IGNORE_LIST:
                        continue
                    elif link.text.lower() == 'stimulate':
                        continue
                    elif link.text.lower() == 'course materials':
                        continue
                    self.children.append(WebPage(link.get('href'),
                                                 self.unit,
                                                 self.session,
                                                 depth=(self.depth + 1),
                                                 parent=self))
            except AttributeError:
                logging.INFO('{}: {}: {}'.format(
                    self.url, header['Content-Type'], body))
                return
        self.crawled = True
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

    def download_file(self, directory):
        tmp = os.path.join(directory, 'partdownload')

        filename = clean_url(self.session.head(self.url, allow_redirects=True).
                             self.url.split('/')[-1])
        filename = os.path.join(os.path.split(tmp)[0], filename)

        print('Downloading {} to {}'.format())
        with open(tmp, 'wb') as f:
            for block in self.session.get(self.url).iter_content(2042):
                f.write(block)
        os.rename(tmp, filename)
        return


def main():
    pass

if __name__ == '__main__':
    import sys
    sys.exit(main())
