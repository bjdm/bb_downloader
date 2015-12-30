import re

from bs4 import BeautifulSoup as bs
from xml.sax.saxutils import unescape


def parse_config():
    soup = bs(open('config.xml').read(), 'lxml')
    units = []

    for u in (soup.find_all('unit')):
        unit = {}
        unit['unitname'] = re.sub('<[^<]+?>', '', str(u.unitname))
        unit['unitcode'] = re.sub('<[^<]+?>', '', str(u.unitcode))
        unit['directory'] = re.sub('<[^<]+?>', '', str(u.directory))
        unit['url'] = unescape(re.sub('<[^<]+?>', '', str(u.url)))
        unit['semester'] = re.sub('<[^<]+?>', '', str(u.semester))
        unit['year'] = re.sub('<[^<]+?>', '', str(u.year))
   
        units.append(unit)

    return units
