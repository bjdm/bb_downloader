import sys
import logging

from bb_downloader.bb_auth import authenticate
from bb_downloader.config import parse_config
from bb_downloader.Unit import Unit

# For testing purposes/private use, declare username and password here
# un = 'n#######'
# pw = 'password'


def main(argv=None):
    """docstring for main"""
    logging.basicConfig(level=logging.WARN)

    # Set argv here. Allows to be run from interactive interpreter where
    # optional argument would default to whatever interpreter is called with
    if argv is None:
        argv = sys.argv

    # Uncomment these two lines if declaring username and password globally
    # ie. outside of main for your own personal script
    un = input('Enter your username: ')
    pw = input('Enter your password:')

    # Parse config.xml to retrieve user's units
    logging.info('Parsing configuration.')
    cfg = parse_config()

    logging.info('Authenticating session.')
    s = authenticate(un, pw)
    logging.info('Successfully authenticated')

    units = [Unit(u.name, u.code, u.bb_url, u.echo_url, u.assessment_dir,
                  u.recordings_dir, u.resources_dir, u.year, u.semester, s)
             for u in cfg]

    for unit in units:
        unit.refresh_rss()

if __name__ == '__main__':
    sys.exit(main())
