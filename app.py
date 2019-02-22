import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from handlers import main


define('port', default=8080, help='run port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handler = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<p_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler)
        ]

        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static'
        )

        super().__init__(handler, **settings)


if __name__ == '__main__':
    app = Application()
    tornado.options.parse_command_line()
    app.listen(options.port)
    print('tornado server run on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()