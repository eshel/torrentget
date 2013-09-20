__author__ = 'Amir'

from tornado import gen

from torrent_providers.torrentleech import search as tl_search

@gen.coroutine
def searchTorrents(query):
    results = tl_search(query)
    ret = {
        'query': query,
        'results': results,
    }
    raise gen.Return(ret)

