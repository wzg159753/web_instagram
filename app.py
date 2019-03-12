import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from handlers import main, auth, chat, service

from utils.verify import hash_md5

define('port', default=8080, help='run port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handler = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<p_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler),
            (r'/login', auth.LoginHandler),
            (r'/signup', auth.SignupHandler),
            (r'/profile', main.PorfileHandler),
            (r'/loginout', main.LoginoutHandler),
            (r'/like', main.LikeHandler),
            (r'/atte', main.AtteHandler),
            (r'/delete', main.DeleteHandler),
            (r'/room', chat.RoomHandler),
            (r'/ws', chat.MessageHandler),
            (r'/async', service.AsyncHandler)
        ]

        settings = dict(
            debug = True,
            template_path = 'templates',
            static_path = 'static',
            login_url = '/login',
            cookie_secret = hash_md5('salt'),
            pycket = {
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 6,
                    'max_connections': 2**10
                },
                'cookies': {
                    'expires_days': 30
                }
            }
        )

        super().__init__(handler, **settings)


if __name__ == '__main__':
    app = Application()
    tornado.options.parse_command_line()
    app.listen(options.port)
    print('tornado server run on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()