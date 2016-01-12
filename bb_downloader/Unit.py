import os

from bb_downloader.utils import parse_rss, fetch_rss, parse_item
from bb_downloader.Lecture import Lecture
from bb_downloader.WebPage import WebPage
from bb_downloader.utils import clean_url


class Unit():
    """ A unit represents all the information required by the crawler. This class
    hands off downloading tasks to the respective object.
    """
    def __init__(self,
                 name,
                 code,
                 bb_url,
                 echo_url,
                 assessment_dir,
                 recordings_dir,
                 resources_dir,
                 year,
                 semester):

        self.name = name
        self.code = code
        self.bb_url = bb_url
        self.echo_url = echo_url
        self.assessment_dir = assessment_dir
        self.recordings_dir = recordings_dir
        self.resources_dir = resources_dir
        self.year = year
        self.semester = semester
        self.session = None
        self.lectures = []
        self.assessment = []
        self.resources = []

        return

    def authenticated_session(self, session):
        self.session = session

    def refresh_rss(self):

        # Get fresh RSS feed and parse details
        for item in parse_rss(fetch_rss(self.echo_url)):
            i = parse_item(item)
            self.lectures.append(
                Lecture(
                    i['url'],
                    i['title'],
                    self,
                    i['date'],
                    i['size'],
                    i['guid'])
                )
        return

    def crawl_learning_resources(self):
        WebPage(self.bb_url)
        return

    def crawl_assessment(self):
        WebPage(self.assessment_url)
        return

    def download_lectures(self, all=False):
        if all:
            for lecture in self.lectures:
                lecture.download_lecture()
        else:
            for lecture in self.lectures:
                if not lecture.is_downloaded():
                    lecture.download_lecture()
        return

    def print_downloaded_lectures(self):
        for lecture in self.lectures:
            if lecture.downloaded:
                print('{}: {}'.format(self.code, lecture.title))
        return

    def print_undownloaded_lectures(self):
        for lecture in self.lectures:
            print(lecture.downloaded)
            if not lecture.downloaded:
                print('{}: {}'.format(self.code, lecture.title))
        return

    def print_lectures(self):
        for lecture in self.lectures:
            if lecture.is_downloaded:
                print('[X]{}: {}'.format(self.code, lecture.title))
            else:
                print('[ ]{}: {}'.format(self.code, lecture.title))
        return

    def download_resources(self, all=False):

        pass

    def print_downloaded_resources(self):

        pass

    def print_undownloaded_resources(self):

        pass

    def download_assessment(self, all=False):

        pass

    def print_downloaded_assessment(self):

        pass

    def print_undownloaded_assessment(self):

        pass

    def download_file(unitcode, url, session):
        tmp = os.path.join(unitcode, 'partdownload')
        os.makedirs(unitcode, exist_ok=True)
        name = clean_url(session.head(url, allow_redirects=True).
                         url.split('/')[-1])

        print('Downloading {} to {}'.format())
        with open(tmp, 'wb') as f:
            for block in session.get(url).iter_content(2042):
                f.write(block)
        file_ = os.path.join(unitcode, name)
        os.rename(tmp, file_)

        return


def main():
    pass

if __name__ == '__main__':
    import sys
    sys.exit(main())
