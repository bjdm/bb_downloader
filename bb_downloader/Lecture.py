import os

import requests


class Lecture():

    def __init__(self, url, title, unit, date, size, guid=None):
        self.url = url
        self.title = title
        self.unit = unit
        self.size = int(size)
        self.date = date
        self.guid = guid
        self.downloaded = self.is_downloaded()
        return

    def __repr__(self):
        return '{}: {}'.format(self.unit.code, self.title)

    """ Returns true if there exists file with same size in
    directory. Isn't affected by different naming schemes
    """
    def is_downloaded(self):
        if not os.path.exists(self.unit.echo_directory):
            print('The directory %s does not exist' % self.unit.echo_directory)
            return None
        else:
            for f in os.listdir(self.unit.echo_directory):
                if os.path.getsize(os.path.join(self.unit.echo_directory, f)) == \
                        int(self.size):
                    self.downloaded = True
                    return True
                else:
                    self.downloaded = False
                    return False

    def download_lecture(self, session=None, reporting_hook=None):
        """ Generator that provides progress hook
        """
        blocksize = 8092
        blocknum = 0

        percent = float(blocknum) / (self.size / blocksize) * 100.0

        r = requests.get(self.url, stream=True)
        print('Downloading %s to %s' % (self.title, self.unit.directory))
        with open(os.path.join(self.unit.directory, self.title), 'wb') as f:
            for block in r.iter_content(blocksize):
                f.write(block)
                blocknum = blocknum + 1
                if reporting_hook is not None:
                    reporting_hook(percent)
        return

    def print_if_undownloaded(self):
        if not self.downloaded:
            print(self)
        return


def main():
    pass

if __name__ == '__main__':
    import sys
    sys.exit(main())
