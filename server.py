import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.options import define, options


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("templates/index.html")

application = tornado.web.Application([
    (r"/", MainHandler),
])


def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
