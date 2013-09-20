import tornado.ioloop
import tornado.web
from tornado import gen
import json
import os

from search import searchTorrents

PATH = '.'

class SearchHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_json(self, response):
        output = json.dumps(response)
        self.set_default_headers()
        self.write(output)

    @gen.coroutine
    def get(self):
        query = self.get_argument('query')
        response = yield searchTorrents(query)
        self.write_json(response)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html")

settings = {}

application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/api/search", SearchHandler),
    ],
    template_path=os.path.join(PATH, 'templates'),
    static_path=os.path.join(PATH, 'static'),
    settings=settings,
)


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
