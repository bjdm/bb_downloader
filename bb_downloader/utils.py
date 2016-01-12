from bs4 import BeautifulSoup as bs
from xml.sax.saxutils import unescape
import requests
import re


def clean_url(url):
    url = url.replace('%20', '_')
    url = url.replace('%28', '(')
    url = url.replace('%29', ')')
    url = url.replace('%26', '&')
    url = url.replace('%40', '@')
    url = url.replace('%27', "'")

    return url


def parse_config():
    soup = bs(open('config.xml').read(), 'lxml')

    for u in (soup.find_all('unit')):
        yield {'name': clean_tags(u.unitname),
               'code': clean_tags(u.unitcode),
               'directory': clean_tags(u.directory),
               'url': unescape(clean_tags(u.url)),
               'semester': clean_tags(u.semester),
               'year': clean_tags(u.year)}


# TODO change print to debug statements
def fetch_rss(url, debug=False):
    try:
        r = requests.get(url)
        if debug:
            print(r.headers)
    except requests.ConnectionError as e:
        print('A network error occured.')
        if debug:
            print(e)
    except requests.HTTPError as e:
        print('A HTTP error occured. The status code was %s' % e.code)
        if debug:
            print(e)
    except requests.URLRequired as e:
        print('The URL you entered was invalid. Please check the URL and try '
              'again')
        if debug:
            print(e)
    except requests.TooManyRedirects as e:
        print('There were too many redirects fetching your data. Please try '
              'later. If the problem persists, this may be a problem on the '
              'server side.')
        if debug:
            print(e)
    except requests.ConnectionTimeout as e:
        print('The connection timed out. Please try again. If the problem '
              ' persists, please try later.')
        if debug:
            print(e)
    except requests.ReadTimeout as e:
        print('You have timed out reading the response. Please try again')
        if debug:
            print(e)
    except requests.Timeout as e:
        print('The requests timed out. Please try again.')
        if debug:
            print(e)
    except requests.exceptions as e:
        print('There was an unkown error with fetching your request. Please '
              ' check all inputs for sanity, and try again.')
        if debug:
            print(e)
    except:
        print("An unknown error occured... I'm freaking out man!!")
    else:
        if debug:
            print(r.content)
        return(r.content)


def parse_rss(rss):
    soup = bs(rss, 'lxml')
    items = soup.find_all('item')

    return items


def parse_item(item):
    return {'title': clean_tags(item.title),
            'date': clean_tags(item.pubdate),
            'guid': clean_tags(item.guid),
            'url': get_url(item.enclosure),
            'size': get_size(item.enclosure)
            }


def clean_tags(text):
    return re.sub('<[^<]+?>', '', str(text))


def get_url(text):
    return unescape(re.findall('url="(.*?)"', str(text))[0])


def get_size(text):
    return re.findall('length="(.*?)"', str(text))[0]


def main():
    pass

if __name__ == '__main__':
    import sys
    sys.exit(main())
