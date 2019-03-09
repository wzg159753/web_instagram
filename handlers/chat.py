import uuid
from datetime import datetime
from tornado.escape import json_decode
import tornado.escape
from .main import BaseHandler
from tornado.websocket import WebSocketHandler
from pycket.session import SessionMixin


class RoomHandler(BaseHandler):
    """
    聊天室
    """
    def get(self, *args, **kwargs):
        self.render('room.html', messages=MessageHandler.historys)


class MessageHandler(WebSocketHandler, SessionMixin):
    """
    聊天室后端逻辑
    """
    users = set()
    historys = []
    history_size = 5

    def get_current_user(self):
        return self.session.get('user_id', None)

    def open(self, *args, **kwargs):
        MessageHandler.users.add(self)

    def on_close(self):
        MessageHandler.users.remove(self)

    def on_message(self, message):
        parsed = json_decode(message)

        chat = {
            'id': uuid.uuid4(),
            'body': parsed['body'],
            'username': self.current_user,
            'create_time': datetime.now(),
        }

        msg = {
            'html': tornado.escape.to_basestring(
                self.render_string('message.html', chat = chat)
            )
        }
        MessageHandler.historys.append(msg)
        if len(MessageHandler.historys) > MessageHandler.history_size:
            MessageHandler.historys = MessageHandler.historys[-5:]

        for user in MessageHandler.users:
            user.write_message(msg)

