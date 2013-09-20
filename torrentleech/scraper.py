#!/usr/bin/python

import argparse
import sys
from pprint import pprint
import logging
from bs4 import BeautifulSoup
import datetime
from urlparse import urljoin

SIZE_UNITS = {
    'kb': 1024,
    'mb': 1024**2,
    'gb': 1024**3,
    'tb': 1024**4,
}

TL_BASEURL = "http://www.torrentleech.org/"

def human_size_to_bytes(human):
    human = human.lower().strip()
    bytes = float(human.split(' ')[0])
    for u in SIZE_UNITS:
        if u in human:
            bytes *= SIZE_UNITS[u]
            break
    return bytes

def scrape_results(soup):
    trows = soup.find(id='torrenttable').find('tbody').findAll('tr')
    def find_class(elem, cl):
        return elem.find(attrs={'class': cl})

    results = []
    for tr in trows:
        print(tr)
        name_col = find_class(tr, 'name')
        namelink = name_col.find('a')
        cat_text = name_col.find('b').text
        added_text = name_col.getText()[-19:]
        children = list(tr.children)
        size_text = children[9].text
        info = namelink['href']
        id = info.split('/')[2]
        info = urljoin(TL_BASEURL, info)
        torrent_href = find_class(tr, 'quickdownload').find('a')['href']
        torrent_href = urljoin(TL_BASEURL, torrent_href)
        r = {
            'id': id,
            'title': namelink.text,
            'info': info,
            'seeders': int(find_class(tr, 'seeders').text),
            'leechers': int(find_class(tr, 'leechers').text),
            'torrent': torrent_href,
            'categories': [cat_text.split(' :: ')],
            'add_date': datetime.datetime.strptime(added_text, '%Y-%m-%d %H:%M:%S'),
            'comments_count': int(children[7].find('a').text),
            'size': human_size_to_bytes(size_text) / SIZE_UNITS['mb'],
            'downloaded_count': int(children[11].text.replace('times', '')),
        }
        results.append(r)
    return results


def soup_from_file(infile_path, url=None):
    if url is None:
        url = 'http://www.torrentleech.org/torrents/browse/'
    with open(infile_path, 'r') as html_file:
        html = html_file.read()
        html_file.close()
    return BeautifulSoup(html, "lxml")

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', dest='loglevel', default='critical', help='log level to output to stdout')
    parser.add_argument('infile', nargs=1, type=str, help='path to HTML file to parse')
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    soup = soup_from_file(args.infile[0])
    results = scrape_results(soup)
    pprint(results)


if __name__ == "__main__":
    main(sys.argv[1:])
